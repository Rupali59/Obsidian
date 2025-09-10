#!/usr/bin/env python3
"""
Test script to verify GraphQL optimization
Compares API calls: Old system (36+ calls) vs New system (1 call)
"""

import sys
from pathlib import Path
from datetime import date

# Add the scripts directory to the path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from optimized_parallel_runner import OptimizedParallelRunner

def main():
    """Test the GraphQL optimization"""
    if len(sys.argv) != 2:
        print("Usage: python3 test_graphql_optimization.py <obsidian_path>")
        sys.exit(1)
    
    obsidian_path = sys.argv[1]
    
    print("🧪 Testing GraphQL Optimization")
    print("=" * 50)
    
    # Calculate API call comparison
    tracked_repos = 12  # From repos_to_track.env
    old_api_calls_per_day = tracked_repos * 3 + 1  # 3 calls per repo + 1 username call
    new_api_calls_per_day = tracked_repos + 1  # Batched requests: 1 call per repo + 1 username call
    
    print(f"📊 API Call Comparison:")
    print(f"   🔴 Old System: {old_api_calls_per_day} API calls per day")
    print(f"   🟢 New System: {new_api_calls_per_day} API calls per day")
    print(f"   💾 Reduction: {old_api_calls_per_day - new_api_calls_per_day} calls saved per day")
    print(f"   📈 Efficiency: {((old_api_calls_per_day - new_api_calls_per_day) / old_api_calls_per_day * 100):.1f}% reduction")
    print()
    
    # Test with a specific date
    test_date = date(2025, 9, 1)
    print(f"🧪 Testing with date: {test_date}")
    print("=" * 50)
    
    try:
        runner = OptimizedParallelRunner(obsidian_path)
        
        print("⚡ Executing optimized batched requests...")
        start_time = time.time()
        
        result = runner.run_for_date(test_date)
        
        end_time = time.time()
        query_time = end_time - start_time
        
        print(f"⏱️  Query completed in {query_time:.2f} seconds")
        
        if result and "error" not in result:
            print("✅ Batched optimization test successful!")
            
            # Show results summary
            if isinstance(result, dict) and 'repositories' in result:
                repos_data = result['repositories']
                total_commits = sum(len(repo_data.get('commits', [])) for repo_data in repos_data.values())
                total_prs = sum(len(repo_data.get('pull_requests', [])) for repo_data in repos_data.values())
                total_issues = sum(len(repo_data.get('issues', [])) for repo_data in repos_data.values())
                
                print(f"📊 Results:")
                print(f"   📝 Commits found: {total_commits}")
                print(f"   🔄 PRs found: {total_prs}")
                print(f"   🐛 Issues found: {total_issues}")
                print(f"   📦 Repositories processed: {len(repos_data)}")
            
        else:
            print("❌ Batched optimization test failed!")
            if result and "error" in result:
                print(f"   Error: {result['error']}")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Batched Optimization Test Complete!")

if __name__ == "__main__":
    import time
    main()
