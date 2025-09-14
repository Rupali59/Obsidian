#!/bin/bash

# Main Data Collection Launcher
# Unified system for GitHub and Wakatime data collection

echo "🚀 Data Collection System"
echo "========================="
echo ""

# Get the Obsidian vault path
OBSIDIAN_PATH="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_PATH="$OBSIDIAN_PATH/Scripts/config/unified_data_config.json"

echo "📁 Obsidian path: $OBSIDIAN_PATH"
echo "⚙️  Config file: $CONFIG_PATH"
echo ""

# Check if config file exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ Config file not found: $CONFIG_PATH"
    echo "💡 Please run setup first:"
    echo "   cd data_collectors && python3 setup_config.py"
    exit 1
fi

# Default to today if no arguments provided
if [ $# -eq 0 ]; then
    echo "📅 Processing today (default)"
    cd data_collectors && python3 unified_data_collector.py --config "$CONFIG_PATH" --today
elif [ "$1" = "yesterday" ]; then
    echo "📅 Processing yesterday"
    cd data_collectors && python3 unified_data_collector.py --config "$CONFIG_PATH" --date "$(date -d 'yesterday' '+%Y-%m-%d')"
elif [ "$1" = "today" ]; then
    echo "📅 Processing today"
    cd data_collectors && python3 unified_data_collector.py --config "$CONFIG_PATH" --today
else
    echo "📅 Processing specific date: $1"
    cd data_collectors && python3 unified_data_collector.py --config "$CONFIG_PATH" --date "$1"
fi

echo ""
echo "✅ Data collection completed!"
