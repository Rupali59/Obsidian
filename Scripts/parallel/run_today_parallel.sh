#!/bin/bash

# Run parallel repository processing for today
# This script processes only the repositories marked with 'X' in repos_to_track.env

echo "🚀 Starting parallel repository processing for today"
echo "=" * 60

# Get the Obsidian vault path (parent directory of Scripts)
OBSIDIAN_PATH="$(cd "$(dirname "$0")/../.." && pwd)"

# Run the parallel repository runner for today
python3 "$(dirname "$0")/parallel_repo_runner.py" "$OBSIDIAN_PATH"

echo "✅ Parallel repository processing completed!"
