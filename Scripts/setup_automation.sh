#!/bin/bash

# Automation Setup Script
# Sets up daily data collection to run at 10 PM every day

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.obsidian.dailycollect"
PLIST_FILE="$SCRIPT_DIR/$PLIST_NAME.plist"
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

# Function to install automation
install_automation() {
    echo "📦 Installing daily automation..."
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

