"""
Calendar formatter - formats GitHub data and analytics for calendar entries

NOTE: This formatter generates human-readable markdown format.
For manual edits, update files directly - the formatter will preserve manual sections.
The generated format matches the reference format in Calendar/2026/January/01-01-2026.md
"""

import json
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def get_project_description(repo_name: str) -> str:
    """Generate a human-readable project description from repository name"""
    descriptions = {
        'Rupali59': 'Personal profile repository',
        'Jira_tracker': 'Multi-repository Jira synchronization tool',
        'Motherboard-server': 'Backend server for Motherboard application',
        'MotherBoard': 'Main Motherboard application',
        'Motherboard-billing-service': 'Billing service with multi-provider support',
        'tathya-portfolio': 'Portfolio website',
        'Obsidian': 'Personal knowledge management vault',
        'WorkTracker': 'Development activity tracking and visualization platform',
        'Email-Plugin': 'Email plugin for Motherboard platform',
        'SMS-Plugin': 'SMS plugin for Motherboard platform',
        'WhatsApp-Plugin': 'WhatsApp plugin for Motherboard platform',
        'VipinKaushik': 'Vipin Kaushik project repository',
        'Utility-mb': 'Utility service with Motherboard integration',
    }
    
    # Check for exact match
    if repo_name in descriptions:
        return descriptions[repo_name]
    
    # Check for -mb suffix (Motherboard integration projects)
    if repo_name.endswith('-mb'):
        client_name = repo_name[:-3].replace('-', ' ')
        return f'Motherboard integration for {client_name}'
    
    # Default: capitalize and add "project"
    return f'{repo_name.replace("-", " ").title()} project'


def infer_focus_from_commits(commits: List[Dict]) -> str:
    """Infer focus area from commit messages"""
    if not commits:
        return 'Development'
    
    # Analyze commit messages for common patterns
    messages = [c.get('message', '').lower() for c in commits]
    all_text = ' '.join(messages)
    
    focus_keywords = {
        'infrastructure': ['infrastructure', 'deployment', 'config', 'setup', 'scaffold', 'environment'],
        'feature development': ['feat', 'feature', 'implement', 'add', 'create'],
        'design': ['design', 'theme', 'ui', 'ux', 'visual', 'aesthetic'],
        'bug fixes': ['fix', 'bug', 'error', 'issue', 'resolve'],
        'refactoring': ['refactor', 'restructure', 'cleanup', 'standardize'],
        'maintenance': ['chore', 'update', 'maintain', 'dependencies'],
        'documentation': ['docs', 'documentation', 'readme'],
    }
    
    for focus, keywords in focus_keywords.items():
        if any(keyword in all_text for keyword in keywords):
            return focus.title()
    
    return 'Development'


def format_commit_as_work_detail(commit: Dict) -> str:
    """Convert a commit message to a human-readable work detail"""
    message = commit.get('message', 'No message')
    
    # Remove common prefixes (feat:, fix:, chore:, etc.)
    message = re.sub(r'^(feat|fix|chore|refactor|docs|style|test|perf|ci|build|revert):\s*', '', message, flags=re.IGNORECASE)
    message = message.strip()
    
    # Capitalize first letter
    if message:
        message = message[0].upper() + message[1:]
    
    return message


def generate_work_details(commits: List[Dict]) -> List[str]:
    """Generate work details from commits, grouping similar ones"""
    if not commits:
        return []
    
    work_details = []
    
    # Group commits by type/pattern
    grouped = {}
    individual_commits = []
    
    for commit in commits:
        message = commit.get('message', '').lower()
        detail = format_commit_as_work_detail(commit)
        
        # Try to group similar commits
        key = None
        description = None
        
        if 'gitignore' in message or ('environment' in message and 'management' in message):
            key = 'Environment Configuration'
            description = 'Updated gitignore for environment management'
        elif 'scaffold' in message or 'initial commit' in message:
            key = 'Project Scaffolding'
            if 'motherboard' in message:
                description = 'Initialized project with Motherboard integration scaffold'
            else:
                description = 'Created initial project structure'
        elif 'dependencies' in message or 'install' in message:
            key = 'Dependency Management'
            description = 'Installed and configured project dependencies'
        elif 'merge' in message and 'branch' in message:
            key = 'Branch Management'
            branch = re.search(r"branch ['\"]?(\w+)['\"]?", message)
            branch_name = branch.group(1) if branch else 'development'
            description = f'Merged {branch_name} branch to integrate latest changes'
        elif 'update' in message and ('config' in message or 'assets' in message):
            key = 'Configuration Updates'
            description = 'Updated assets and configurations for improved management'
        elif 'refactor' in message or 'standardize' in message:
            key = 'Structure Standardization'
            if 'architecture' in message:
                description = 'Refactored project structure to feature-based architecture'
            else:
                description = 'Standardized project structure and organization'
        elif 'feat' in message or 'implement' in message:
            # Extract feature name from commit message
            feat_match = re.search(r'(?:feat|implement)[\s:]+(.+?)(?:$|\.|,|\(|\[)', message, re.IGNORECASE)
            if feat_match:
                feat_desc = feat_match.group(1).strip()
                key = 'Feature Implementation'
                description = f'Implemented {feat_desc}'
            else:
                individual_commits.append(commit)
                continue
        elif 'fix' in message:
            fix_match = re.search(r'fix[\s:]+(.+?)(?:$|\.|,|\(|\[)', message, re.IGNORECASE)
            if fix_match:
                fix_desc = fix_match.group(1).strip()
                key = 'Bug Fixes'
                description = f'Fixed {fix_desc}'
            else:
                individual_commits.append(commit)
                continue
        else:
            individual_commits.append(commit)
            continue
        
        if key:
            if key not in grouped:
                grouped[key] = {'description': description, 'count': 0}
            grouped[key]['count'] += 1
    
    # Add grouped work details
    for key, info in grouped.items():
        if info['count'] == 1:
            work_details.append(f"- **{key}**: {info['description']}")
        else:
            work_details.append(f"- **{key}**: {info['description']} ({info['count']} commits)")
    
    # Add individual commits (limit to most important ones)
    for commit in individual_commits[:5]:
        detail = format_commit_as_work_detail(commit)
        # Extract meaningful key from detail
        if ':' in detail:
            key, desc = detail.split(':', 1)
            key = key.strip()
            desc = desc.strip()
        else:
            words = detail.split()
            key = words[0] if words else 'Work'
            desc = detail
        
        work_details.append(f"- **{key}**: {desc}")
    
    return work_details[:10]  # Limit to 10 work details


class CalendarFormatter:
    """Formats GitHub data and analytics for calendar entries"""
    
    def format_github_content(self, github_data: Dict) -> str:
        """Format GitHub data for calendar entry"""
        if not github_data:
            return ""
        
        content = []
        content.append("## 🚀 GitHub Activity")
        content.append("")
        
        # Development Summary
        content.append("### Development Summary")
        content.append("")
        content.append("**🔧 Projects Worked On:**")
        content.append("")
        
        # Process repositories and group commits by time blocks
        repo_stats = {}
        
        # Collect all commits with repository info and store in temp file
        # Exclude Rupali59 repository (profile maintenance only)
        all_commits_data = []
        for repo_name, repo_metrics in github_data.get('repository_details', {}).items():
            # Skip Rupali59 repository
            if repo_name == 'Rupali59':
                continue
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
        
        # Format each repository with numbered projects
        project_number = 1
        for repo_name in repo_order:
            if repo_name not in repo_stats:
                continue
            stats = repo_stats[repo_name]
            commits = repos_with_commits.get(repo_name, [])
            
            # Get project description and focus
            project_desc = get_project_description(repo_name)
            focus = infer_focus_from_commits(commits)
            
            # Format project header
            content.append(f"#### **{project_number}. {repo_name}**")
            content.append(f"*{project_desc}*")
            content.append("")
            content.append(f"- **Commits**: {stats['commits']}")
            if stats['prs'] > 0:
                content.append(f"- **Pull Requests**: {stats['prs']}")
            if stats['issues'] > 0:
                content.append(f"- **Issues**: {stats['issues']}")
            content.append(f"- **Focus**: {focus}")
            content.append("")
            
            # Generate work details from commits
            if commits:
                content.append("**Work Details:**")
                work_details = generate_work_details(commits)
                for detail in work_details:
                    content.append(detail)
                content.append("")
            
            project_number += 1
        
        return "\n".join(content)
    
    def create_datatable_content(self, github_data: Dict) -> str:
        """Create comprehensive datatable content"""
        content = []
        content.append("---")
        content.append("")
        content.append("## 📈 Development Analytics")
        content.append("")
        
        # Summary table
        content.append("### Daily Summary")
        content.append("")
        content.append("| Metric | GitHub |")
        content.append("|--------|--------|")
        
        github_commits = github_data.get('commits', 0) if github_data else 0
        
        content.append(f"| **Commits** | {github_commits} |")
        content.append(f"| **Pull Requests** | {github_data.get('prs', 0) if github_data else 0} |")
        content.append(f"| **Issues** | {github_data.get('issues', 0) if github_data else 0} |")
        content.append("")
        
        # Generate Technical Insights
        content.append("### Technical Insights")
        content.append("")
        
        # Analyze work patterns
        work_patterns = []
        highlights = []
        
        repo_details = github_data.get('repository_details', {})
        all_commits = []
        for repo_name, repo_metrics in repo_details.items():
            # Exclude Rupali59 repository from analysis
            if repo_name == 'Rupali59':
                continue
            all_commits.extend(repo_metrics.get('commit_details', []))
        
        # Analyze commit messages for patterns
        if all_commits:
            messages = [c.get('message', '').lower() for c in all_commits]
            all_text = ' '.join(messages)
            
            # Detect work patterns
            if any(kw in all_text for kw in ['scaffold', 'initial commit', 'setup']):
                work_patterns.append("Project initialization and scaffolding activities")
            if any(kw in all_text for kw in ['feat', 'feature', 'implement']):
                work_patterns.append("Feature development and implementation")
            if any(kw in all_text for kw in ['refactor', 'restructure', 'standardize']):
                work_patterns.append("Code refactoring and structure improvements")
            if any(kw in all_text for kw in ['config', 'environment', 'gitignore']):
                work_patterns.append("Configuration and environment management")
            if any(kw in all_text for kw in ['fix', 'bug', 'error', 'resolve']):
                work_patterns.append("Bug fixes and issue resolution")
            
            # Generate highlights
            repo_count = len([r for r in repo_details.keys() if r != 'Rupali59' and repo_details[r].get('commits', 0) > 0])
            if repo_count > 1:
                highlights.append(f"Active development across {repo_count} repositories")
            if github_data.get('prs', 0) > 0:
                highlights.append(f"{github_data.get('prs', 0)} pull request{'s' if github_data.get('prs', 0) != 1 else ''} merged")
            if github_data.get('commits', 0) > 10:
                highlights.append("High commit activity indicating productive development session")
        
        # Default patterns if none detected
        if not work_patterns:
            work_patterns.append("Development activity across multiple projects")
        
        if not highlights:
            highlights.append("Continued development and project maintenance")
        
        content.append("**🔍 Work Patterns:**")
        for pattern in work_patterns[:3]:  # Limit to 3 patterns
            content.append(f"- {pattern}")
        content.append("")
        
        content.append("**🛠️ Highlights:**")
        for highlight in highlights[:4]:  # Limit to 4 highlights
            content.append(f"- {highlight}")
        content.append("")
        
        content.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d')}*")
        
        return "\n".join(content)
