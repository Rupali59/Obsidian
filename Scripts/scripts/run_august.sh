#!/bin/bash
# Run August 2025 GitHub Capture
# Uses parallel processing for faster execution

OBSIDIAN_PATH="/Users/rupali.b/Documents/GitHub/Obsidian"
CONFIG_FILE="configs/august_2025.json"

cd "$(dirname "$0")" || exit 1

echo "🚀 August 2025 GitHub Capture (Parallel)"
echo "========================================"
echo ""

python3 runner.py "$OBSIDIAN_PATH" "$CONFIG_FILE"
