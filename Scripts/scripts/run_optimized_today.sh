#!/bin/bash

# Run optimized GitHub metrics capture for today using GraphQL
# This reduces API calls from 36+ to just 1 per day!

echo "🚀 Optimized GitHub Metrics Capture (GraphQL)"
echo "=============================================="
echo "⚡ API calls reduced from 36+ to 1 per day!"
echo ""

# Get the Obsidian vault path (parent directory of Scripts)
OBSIDIAN_PATH="$(cd "$(dirname "$0")/../.." && pwd)"

echo "📁 Obsidian path: $OBSIDIAN_PATH"
echo ""

# Run the optimized parallel runner
python3 "$(dirname "$0")/optimized_parallel_runner.py" "$OBSIDIAN_PATH"

echo ""
echo "✅ Optimized capture completed!"
echo "💾 API calls saved: 35+ per day"
