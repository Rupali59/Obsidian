#!/bin/bash

# Unified Data Collection Launcher
# Collects GitHub and Wakatime data using configuration file

echo "🚀 Unified Data Collection System"
echo "================================="
echo "📊 Collecting GitHub and Wakatime data with config-based processing"
echo ""

# Get the Obsidian vault path (parent directory of Scripts)
OBSIDIAN_PATH="$(cd "$(dirname "$0")/../../.." && pwd)"
CONFIG_PATH="$OBSIDIAN_PATH/Scripts/config/unified_data_config.json"

echo "📁 Obsidian path: $OBSIDIAN_PATH"
echo "⚙️  Config file: $CONFIG_PATH"
echo ""

# Check if config file exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ Config file not found: $CONFIG_PATH"
    echo "💡 Please create the config file first"
    exit 1
fi

# Default to today if no arguments provided
if [ $# -eq 0 ]; then
    echo "📅 Processing today (default)"
    python3 "$(dirname "$0")/unified_data_collector.py" --config "$CONFIG_PATH" --today
elif [ "$1" = "yesterday" ]; then
    echo "📅 Processing yesterday"
    python3 "$(dirname "$0")/unified_data_collector.py" --config "$CONFIG_PATH" --date "$(date -d 'yesterday' '+%Y-%m-%d')"
elif [ "$1" = "today" ]; then
    echo "📅 Processing today"
    python3 "$(dirname "$0")/unified_data_collector.py" --config "$CONFIG_PATH" --today
else
    echo "📅 Processing specific date: $1"
    python3 "$(dirname "$0")/unified_data_collector.py" --config "$CONFIG_PATH" --date "$1"
fi

echo ""
echo "✅ Unified data collection completed!"
echo ""
echo "📝 Check your calendar entry to see the integrated data:"
echo "   Calendar/2025/September/10-09-2025.md"
echo ""
echo "💡 The data includes:"
echo "   - GitHub Activity (commits, PRs, issues)"
echo "   - Wakatime Activity (coding time, languages, projects)"
echo "   - Development Analytics (datatables)"
