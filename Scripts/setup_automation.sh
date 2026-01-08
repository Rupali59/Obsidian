#!/bin/bash

# Automation Setup Script
# Sets up daily data collection to run at 10 PM every day

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.obsidian.dailycollect"
PLIST_FILE="$SCRIPT_DIR/config/$PLIST_NAME.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
INSTALLED_PLIST="$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"
DAILY_SCRIPT="$SCRIPT_DIR/daily_auto_collect.sh"

echo "🚀 Obsidian Daily Data Collection - Automation Setup"
echo "======================================================"
echo ""

# Function to show usage
show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install   - Install and start the daily automation"
    echo "  uninstall - Stop and remove the daily automation"
    echo "  start     - Start the automation service"
    echo "  stop      - Stop the automation service"
    echo "  restart   - Restart the automation service"
    echo "  status    - Check if automation is running"
    echo "  test      - Run data collection once manually"
    echo "  logs      - View recent automation logs"
    echo ""
}

# Function to update paths in plist file
update_plist_paths() {
    local obsidian_path="$(cd "$SCRIPT_DIR/.." && pwd)"
    
    # Use Python to update plist XML properly
    python3 <<PYTHON
import xml.etree.ElementTree as ET
import os

obsidian_path = "$obsidian_path"
plist_path = "$PLIST_FILE"

# Parse XML
tree = ET.parse(plist_path)
root = tree.getroot()

# Find the dict element
dict_elem = root.find('.//dict')

# Function to update string value
def update_string_value(key_name, new_value):
    keys = dict_elem.findall('key')
    for i, key in enumerate(keys):
        if key.text == key_name:
            # Next sibling should be the string value
            if i + 1 < len(dict_elem):
                string_elem = dict_elem[i + 1]
                if string_elem.tag == 'string':
                    string_elem.text = new_value
                    return True
    return False

# Update all paths
update_string_value('Program', os.path.join(obsidian_path, "Scripts/daily_auto_collect.sh"))
update_string_value('WorkingDirectory', obsidian_path)
update_string_value('StandardOutPath', os.path.join(obsidian_path, "Scripts/logs/launchd_stdout.log"))
update_string_value('StandardErrorPath', os.path.join(obsidian_path, "Scripts/logs/launchd_stderr.log"))

# Write back
tree.write(plist_path, encoding='utf-8', xml_declaration=True)

print(f"✅ Updated plist paths to: {obsidian_path}")
PYTHON
}

# Function to update config file paths
update_config_paths() {
    local obsidian_path="$(cd "$SCRIPT_DIR/.." && pwd)"
    local config_file="$obsidian_path/Scripts/config/unified_data_config.json"
    
    if [ -f "$config_file" ]; then
        # Use Python to update JSON (more reliable than sed for JSON)
        python3 <<PYTHON
import json
import sys

config_path = "$config_file"
obsidian_path = "$obsidian_path"

try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Update vault_path
    if 'obsidian' in config:
        config['obsidian']['vault_path'] = obsidian_path
    
    # Write back
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Updated config vault_path to: {obsidian_path}")
except Exception as e:
    print(f"❌ Error updating config: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON
    fi
}

# Function to install automation
install_automation() {
    echo "📦 Installing daily automation..."
    echo ""
    
    # Update paths first
    echo "Updating paths to current location..."
    update_plist_paths
    update_config_paths
    echo ""
    
    # Make scripts executable
    echo "Making scripts executable..."
    chmod +x "$DAILY_SCRIPT"
    chmod +x "$SCRIPT_DIR/run_data_collection.sh"
    
    # Create LaunchAgents directory if it doesn't exist
    mkdir -p "$LAUNCH_AGENTS_DIR"
    
    # Create logs directory
    mkdir -p "$SCRIPT_DIR/logs"
    
    # Copy plist file to LaunchAgents
    echo "Installing launch agent..."
    cp "$PLIST_FILE" "$INSTALLED_PLIST"
    
    # Load the launch agent
    echo "Loading launch agent..."
    launchctl load "$INSTALLED_PLIST"
    
    echo ""
    echo "✅ Daily automation installed successfully!"
    echo "📅 Data collection will run automatically at 10:00 PM every day"
    echo ""
    echo "To verify installation, run:"
    echo "  bash $0 status"
    echo ""
}

# Function to uninstall automation
uninstall_automation() {
    echo "🗑️  Uninstalling daily automation..."
    echo ""
    
    # Unload the launch agent if it's loaded
    if launchctl list | grep -q "$PLIST_NAME"; then
        echo "Unloading launch agent..."
        launchctl unload "$INSTALLED_PLIST"
    fi
    
    # Remove the plist file
    if [ -f "$INSTALLED_PLIST" ]; then
        echo "Removing launch agent file..."
        rm "$INSTALLED_PLIST"
    fi
    
    echo ""
    echo "✅ Daily automation uninstalled successfully!"
    echo ""
}

# Function to start automation
start_automation() {
    echo "▶️  Starting daily automation..."
    
    if [ ! -f "$INSTALLED_PLIST" ]; then
        echo "❌ Automation not installed. Run: $0 install"
        exit 1
    fi
    
    launchctl load "$INSTALLED_PLIST"
    echo "✅ Automation started!"
}

# Function to stop automation
stop_automation() {
    echo "⏸️  Stopping daily automation..."
    
    if launchctl list | grep -q "$PLIST_NAME"; then
        launchctl unload "$INSTALLED_PLIST"
        echo "✅ Automation stopped!"
    else
        echo "ℹ️  Automation is not running"
    fi
}

# Function to restart automation
restart_automation() {
    echo "🔄 Restarting daily automation..."
    stop_automation
    sleep 2
    start_automation
}

# Function to check status
check_status() {
    echo "📊 Automation Status"
    echo "===================="
    echo ""
    
    if [ ! -f "$INSTALLED_PLIST" ]; then
        echo "Status: ❌ Not installed"
        echo ""
        echo "To install, run:"
        echo "  bash $0 install"
        return
    fi
    
    if launchctl list | grep -q "$PLIST_NAME"; then
        echo "Status: ✅ Running"
        echo ""
        echo "Next run: Today at 10:00 PM"
        echo "Logs: $SCRIPT_DIR/logs/daily_auto_collect.log"
    else
        echo "Status: ⏸️  Installed but not running"
        echo ""
        echo "To start, run:"
        echo "  bash $0 start"
    fi
    echo ""
}

# Function to test run
test_run() {
    echo "🧪 Running test collection..."
    echo ""
    
    bash "$DAILY_SCRIPT"
    
    echo ""
    echo "Test completed. Check the logs at:"
    echo "  $SCRIPT_DIR/logs/daily_auto_collect.log"
}

# Function to view logs
view_logs() {
    LOG_FILE="$SCRIPT_DIR/logs/daily_auto_collect.log"
    
    if [ ! -f "$LOG_FILE" ]; then
        echo "No logs found yet."
        return
    fi
    
    echo "📋 Recent Logs (last 50 lines)"
    echo "==============================="
    echo ""
    tail -50 "$LOG_FILE"
}

# Parse command
case "$1" in
    install)
        install_automation
        ;;
    uninstall)
        uninstall_automation
        ;;
    start)
        start_automation
        ;;
    stop)
        stop_automation
        ;;
    restart)
        restart_automation
        ;;
    status)
        check_status
        ;;
    test)
        test_run
        ;;
    logs)
        view_logs
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

