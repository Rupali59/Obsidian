#!/bin/bash

# Unified Parallel Runner - Single script for all GitHub metrics capture
# Uses configuration files and optimized GraphQL batching

echo "🚀 Unified Parallel Repository Runner"
echo "====================================="
echo "⚡ Single script with config-based processing"
echo ""

# Get the Obsidian vault path (parent directory of Scripts)
OBSIDIAN_PATH="$(cd "$(dirname "$0")/../.." && pwd)"

# Default to today if no arguments provided
if [ $# -eq 0 ]; then
    echo "📅 Processing today (default)"
    python3 "$(dirname "$0")/unified_parallel_runner.py" "$OBSIDIAN_PATH" --today
elif [ "$1" = "yesterday" ]; then
    echo "📅 Processing yesterday"
    python3 "$(dirname "$0")/unified_parallel_runner.py" "$OBSIDIAN_PATH" --yesterday
elif [ "$1" = "today" ]; then
    echo "📅 Processing today"
    python3 "$(dirname "$0")/unified_parallel_runner.py" "$OBSIDIAN_PATH" --today
else
    echo "📅 Processing specific date: $1"
    python3 "$(dirname "$0")/unified_parallel_runner.py" "$OBSIDIAN_PATH" --date "$1"
fi

echo ""
echo "✅ Unified processing completed!"
