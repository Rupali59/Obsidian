"""
Calendar formatter - formats GitHub data and analytics for calendar entries
"""

import json
import tempfile
from datetime import datetime, time
from pathlib import Path
from typing import Dict, List, Tuple

from ..utils.helpers import calculate_project_switches

# Daily schedule time blocks from COMMAND & CONTAINMENT PROTOCOL.md
TIME_BLOCKS = [
    ("6:30-7:00", time(6, 30), time(7, 0), "Wake + Body Priming"),
    ("7:00-8:00", time(7, 0), time(8, 0), "Primary Work Block 1 (Deep, Dry)"),
    ("8:00-8:30", time(8, 0), time(8, 30), "Transition + Fuel"),
    ("8:30-11:30", time(8, 30), time(11, 30), "Primary Work Block 2 (Execution)"),
    ("11:30-12:00", time(11, 30), time(12, 0), "Mechanical Reset"),
    ("12:00-2:00", time(12, 0), time(14, 0), "Office / Obligation Work"),
    ("2:00-2:30", time(14, 0), time(14, 30), "Lunch (Neutral)"),
    ("2:30-4:30", time(14, 30), time(16, 30), "Secondary Work Block (Lower Friction)"),
    ("4:30-5:00", time(16, 30), time(17, 0), "Dead Zone (Intentional Neutrality)"),
    ("5:00-6:00", time(17, 0), time(18, 0), "Optional Creative / Technical Output"),
    ("6:00-7:30", time(18, 0), time(19, 30), "Deep Craft (Bounded)"),
    ("7:30-8:00", time(19, 30), time(20, 0), "Dinner (Silent / Neutral)"),
    ("8:00-8:30", time(20, 0), time(20, 30), "Consolidation + Decompression"),
    ("8:30-9:00", time(20, 30), time(21, 0), "Nightly Truth Audit"),
    ("9:00-10:00", time(21, 0), time(22, 0), "Wind-Down"),
    ("10:00+", time(22, 0), None, "Sleep"),
]


def get_time_block_for_time(commit_time: time) -> Tuple[str, str]:
    """Get the time block label and name for a given time"""
    for block_label, start_time, end_time, block_name in TIME_BLOCKS:
        if end_time is None:  # Last block (10:00+)
            if commit_time >= start_time:
                return block_label, block_name
        else:
            if start_time <= commit_time < end_time:
                return block_label, block_name
    # Fallback for times before 6:30 (before wake time) - assign to first block
    return TIME_BLOCKS[0][0], TIME_BLOCKS[0][3]  # Return first block (6:30-7:00)


class CalendarFormatter:
    """Formats GitHub data and analytics for calendar entries"""
    
    def format_github_content(self, github_data: Dict) -> str:
        """Format GitHub data for calendar entry"""
        if not github_data:
            return ""
        
        # Calculate project switches
        project_switches = calculate_project_switches(github_data)
        
        content = []
        content.append("## 🚀 GitHub Activity")
        content.append("")
        activity_summary = f"**Activity Summary:** {github_data['commits']} commits, {github_data['prs']} PRs, {github_data['issues']} issues"
        if project_switches > 0:
            activity_summary += f", {project_switches} project switch{'es' if project_switches != 1 else ''}"
        content.append(activity_summary)
        content.append("")
        
        # Development Summary
        content.append("### Development Summary")
        content.append("")
        content.append("**🔧 Components Worked On:**")
        content.append("")
        
        # Process repositories and group commits by time blocks
        repo_stats = {}
        
        # Collect all commits with repository info and store in temp file
        all_commits_data = []
        for repo_name, repo_metrics in github_data.get('repository_details', {}).items():
            if repo_metrics.get('commits', 0) > 0 or repo_metrics.get('prs', 0) > 0 or repo_metrics.get('issues', 0) > 0:
                repo_stats[repo_name] = {
                    'commits': repo_metrics.get('commits', 0),
                    'prs': repo_metrics.get('prs', 0),
                    'issues': repo_metrics.get('issues', 0),
                    'commit_details': repo_metrics.get('commit_details', [])
                }
                # Add repo name to each commit for sorting
                for commit in repo_metrics.get('commit_details', []):
                    commit_with_repo = commit.copy()
                    commit_with_repo['repo_name'] = repo_name
                    all_commits_data.append(commit_with_repo)
        
        # Write commits to temporary file, sorted by project (repository)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)
            # Sort by repository name first, then by timestamp
            all_commits_data.sort(key=lambda x: (x.get('repo_name', ''), x.get('timestamp', '')))
            json.dump(all_commits_data, tmp_file, indent=2)
        
        # Read back from temp file (sorted by project)
        with open(tmp_path, 'r') as f:
            sorted_commits_data = json.load(f)
        
        # Clean up temp file
        try:
            tmp_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors
        
        # Group commits by repository (already sorted)
        repos_with_commits = {}
        for commit_data in sorted_commits_data:
            repo_name = commit_data.get('repo_name', 'Unknown')
            if repo_name not in repos_with_commits:
                repos_with_commits[repo_name] = []
            # Remove repo_name from commit data before storing
            commit_copy = {k: v for k, v in commit_data.items() if k != 'repo_name'}
            repos_with_commits[repo_name].append(commit_copy)
        
        # Determine repository display order (by first commit timestamp)
        repo_first_commits = []
        for repo_name, commits in repos_with_commits.items():
            if commits:
                sorted_commits = sorted(commits, key=lambda x: x.get('timestamp', ''))
                first_commit = sorted_commits[0]
                repo_first_commits.append((repo_name, first_commit.get('timestamp', '')))
        
        repo_first_commits.sort(key=lambda x: x[1])
        repo_order = [repo_name for repo_name, _ in repo_first_commits]
        
        # Format each repository
        for repo_name in repo_order:
            if repo_name not in repo_stats:
                continue
            stats = repo_stats[repo_name]
            content.append(f"#### **{repo_name}**")
            content.append(f"- **Commits**: {stats['commits']}")
            content.append(f"- **Pull Requests**: {stats['prs']}")
            content.append(f"- **Issues**: {stats['issues']}")
            
            # Group commits by time blocks (from sorted data)
            commits = repos_with_commits.get(repo_name, [])
            if commits:
                # Parse timestamps and group by time block
                commits_with_time = []
                for commit in commits:
                    timestamp = commit.get('timestamp', '')
                    commit_time_obj = None
                    if timestamp:
                        try:
                            if timestamp.endswith('Z'):
                                timestamp_clean = timestamp.replace('Z', '+00:00')
                            else:
                                timestamp_clean = timestamp
                            dt = datetime.fromisoformat(timestamp_clean)
                            commit_time_obj = dt.time()
                        except (ValueError, AttributeError, TypeError):
                            pass
                    
                    if commit_time_obj:
                        block_label, block_name = get_time_block_for_time(commit_time_obj)
                        commits_with_time.append((block_label, block_name, commit_time_obj, commit))
                    else:
                        commits_with_time.append(("Other", "Other Time", None, commit))
                
                # Sort commits chronologically
                commits_with_time.sort(key=lambda x: (x[2] if x[2] else time(0, 0), x[3].get('timestamp', '')))
                
                # Group by time block
                time_block_groups = {}
                for block_label, block_name, commit_time, commit in commits_with_time:
                    if block_label not in time_block_groups:
                        time_block_groups[block_label] = {
                            'name': block_name,
                            'commits': []
                        }
                    time_block_groups[block_label]['commits'].append(commit)
                
                # Format commits grouped by time blocks (in schedule order)
                if time_block_groups:
                    content.append("")
                    content.append("**📝 Commits by Time Block:**")
                    content.append("")
                    
                    # Display time blocks in schedule order
                    displayed_blocks = set()
                    for block_label, start_time, end_time, block_name in TIME_BLOCKS:
                        if block_label in time_block_groups and block_label not in displayed_blocks:
                            displayed_blocks.add(block_label)
                            group = time_block_groups[block_label]
                            content.append(f"**{block_label}: {group['name']}**")
                            content.append("")
                            
                            for commit in group['commits']:
                                sha = commit.get('sha', 'unknown')
                                message = commit.get('message', 'No message')
                                url = commit.get('url', '')
                                timestamp = commit.get('timestamp', '')
                                
                                # Format timestamp if available
                                time_str = ""
                                if timestamp:
                                    try:
                                        if timestamp.endswith('Z'):
                                            timestamp_clean = timestamp.replace('Z', '+00:00')
                                        else:
                                            timestamp_clean = timestamp
                                        dt = datetime.fromisoformat(timestamp_clean)
                                        time_str = f" *({dt.strftime('%H:%M:%S')})*"
                                    except (ValueError, AttributeError, TypeError):
                                        try:
                                            if 'T' in timestamp:
                                                time_part = timestamp.split('T')[1].split('.')[0].split('+')[0].split('-')[0]
                                                time_str = f" *({time_part})*"
                                        except:
                                            pass
                                
                                if url:
                                    content.append(f"- [`{sha}`]({url}) {message}{time_str}")
                                else:
                                    content.append(f"- `{sha}` {message}{time_str}")
                            
                            content.append("")
                    
                    # Handle any commits in "Other" time block (shouldn't normally happen)
                    if "Other" in time_block_groups and "Other" not in displayed_blocks:
                        group = time_block_groups["Other"]
                        content.append(f"**Other Time: {group['name']}**")
                        content.append("")
                        for commit in group['commits']:
                            sha = commit.get('sha', 'unknown')
                            message = commit.get('message', 'No message')
                            url = commit.get('url', '')
                            timestamp = commit.get('timestamp', '')
                            
                            time_str = ""
                            if timestamp:
                                try:
                                    if timestamp.endswith('Z'):
                                        timestamp_clean = timestamp.replace('Z', '+00:00')
                                    else:
                                        timestamp_clean = timestamp
                                    dt = datetime.fromisoformat(timestamp_clean)
                                    time_str = f" *({dt.strftime('%H:%M:%S')})*"
                                except (ValueError, AttributeError, TypeError):
                                    try:
                                        if 'T' in timestamp:
                                            time_part = timestamp.split('T')[1].split('.')[0].split('+')[0].split('-')[0]
                                            time_str = f" *({time_part})*"
                                    except:
                                        pass
                            
                            if url:
                                content.append(f"- [`{sha}`]({url}) {message}{time_str}")
                            else:
                                content.append(f"- `{sha}` {message}{time_str}")
                        content.append("")
            
            content.append("")
        
        return "\n".join(content)
    
    def create_datatable_content(self, github_data: Dict) -> str:
        """Create comprehensive datatable content"""
        content = []
        content.append("## Development Analytics")
        content.append("")
        
        # Summary table
        content.append("### Daily Summary")
        content.append("")
        content.append("| Metric | GitHub |")
        content.append("|--------|--------|")
        
        github_commits = github_data.get('commits', 0) if github_data else 0
        
        content.append(f"| Commits | {github_commits} |")
        content.append(f"| Pull Requests | {github_data.get('prs', 0) if github_data else 0} |")
        content.append(f"| Issues | {github_data.get('issues', 0) if github_data else 0} |")
        content.append("")
        content.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(content)
