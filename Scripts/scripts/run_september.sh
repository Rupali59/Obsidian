#!/bin/bash

# Run parallel GitHub metrics capture for September 2025
# This script processes only the repositories marked with 'X' in repos_to_track.env

echo "🚀 September 2025 GitHub Capture (Parallel)"
echo "=========================================="

# Get the Obsidian vault path (parent directory of Scripts)
OBSIDIAN_PATH="$(cd "$(dirname "$0")/../.." && pwd)"

# Run the parallel repository runner
python3 "$(dirname "$0")/runner.py" "$OBSIDIAN_PATH" "$(dirname "$0")/../parallel/configs/september_2025.json"

echo "✅ September 2025 parallel capture completed!"
