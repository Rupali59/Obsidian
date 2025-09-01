#!/bin/bash

# Run parallel GitHub metrics capture for July 2025
# This script processes only the repositories marked with 'X' in repos_to_track.env

echo "🚀 July 2025 GitHub Capture (Parallel)"
echo "========================================"

# Get the Obsidian vault path (parent directory of Scripts)
OBSIDIAN_PATH="$(cd "$(dirname "$0")/../.." && pwd)"

# Run the parallel repository runner
python3 "$(dirname "$0")/runner.py" "$OBSIDIAN_PATH" "configs/july_2025.json"

echo "✅ July 2025 parallel capture completed!"
