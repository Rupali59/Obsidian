#!/bin/bash

# Daily Data Collection Script
# Runs automatically to collect GitHub data for the current day
# Designed to run at 10 PM every day via cron/launchd

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OBSIDIAN_PATH="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_PATH="$SCRIPT_DIR/config/unified_data_config.json"
COLLECTOR_PATH="$SCRIPT_DIR/data_collectors/main.py"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/daily_auto_collect.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Start logging
log_message "=========================================="
log_message "Starting daily data collection"
log_message "Obsidian path: $OBSIDIAN_PATH"
log_message "=========================================="

# Check if config file exists
if [ ! -f "$CONFIG_PATH" ]; then
    log_message "ERROR: Config file not found: $CONFIG_PATH"
    exit 1
fi

# Get today's date
TODAY=$(date '+%Y-%m-%d')
log_message "Collecting data for: $TODAY"

# Run the data collector for today
cd "$OBSIDIAN_PATH"
python3 "$COLLECTOR_PATH" --config "$CONFIG_PATH" --date "$TODAY" >> "$LOG_FILE" 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    log_message "✅ Daily data collection completed successfully!"
    EXIT_CODE=0
else
    log_message "❌ Daily data collection failed!"
    EXIT_CODE=1
fi

log_message "=========================================="
log_message "Daily data collection finished"
log_message "=========================================="
echo "" >> "$LOG_FILE"

exit $EXIT_CODE

