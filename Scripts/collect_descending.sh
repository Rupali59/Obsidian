#!/bin/bash

# Collect data in descending order from Feb 13, 2026 backwards
# Stops when it encounters existing markdown files

OBSIDIAN_PATH="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_PATH="$OBSIDIAN_PATH/Scripts/config/unified_data_config.json"
COLLECTOR_PATH="$OBSIDIAN_PATH/Scripts/data_collectors/main.py"

echo "🚀 Descending Data Collection"
echo "============================="
echo "Starting from Feb 13, 2026 going backwards"
echo ""

# Check if config file exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ Config file not found: $CONFIG_PATH"
    exit 1
fi

python3 - <<PY
import datetime
import subprocess
import os
from pathlib import Path

obsidian_path = Path("$OBSIDIAN_PATH")
start_date = datetime.date(2026, 2, 13)  # Feb 13, 2026
current_date = start_date

def file_exists_for_date(target_date):
    """Check if markdown file exists for a given date"""
    month_name = target_date.strftime("%B")
    day_str = target_date.strftime("%d-%m-%Y")
    file_path = obsidian_path / "Calendar" / str(target_date.year) / month_name / f"{day_str}.md"
    return file_path.exists()

def collect_for_date(target_date):
    """Collect data for a single date"""
    try:
        print(f"📆 Collecting data for {target_date}")
        # Change to the Scripts directory to run as module
        collector_dir = obsidian_path / "Scripts" / "data_collectors"
        result = subprocess.run([
            "python3", "-m", "data_collectors.main",
            "--config", str(obsidian_path / "Scripts" / "config" / "unified_data_config.json"),
            "--date", target_date.isoformat()
        ], cwd=str(obsidian_path / "Scripts"), check=False, capture_output=True, text=True)
        
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else result.stdout
            print(f"❌ Failed {target_date}: {error_msg[:300]}")
            return False
        print(f"✅ Completed {target_date}")
        return True
    except Exception as e:
        print(f"❌ Error processing {target_date}: {e}")
        return False

# Go backwards day by day
collected = 0
skipped = 0
failed = []

print(f"Starting from {start_date}, going backwards...")
print("")

while True:
    # Check if file already exists
    if file_exists_for_date(current_date):
        print(f"⏭️  Skipping {current_date} - file already exists")
        skipped += 1
        
        # If we've skipped 3 consecutive dates, we've probably reached the existing range
        # But let's continue a bit more to be safe - check if next few dates also exist
        next_date = current_date - datetime.timedelta(days=1)
        if file_exists_for_date(next_date):
            next_next = next_date - datetime.timedelta(days=1)
            if file_exists_for_date(next_next):
                print(f"")
                print(f"✅ Reached existing date range. Stopping collection.")
                break
    else:
        # File doesn't exist, collect data
        success = collect_for_date(current_date)
        if success:
            collected += 1
        else:
            failed.append(current_date)
    
    # Move to previous day
    current_date -= datetime.timedelta(days=1)
    
    # Safety check: don't go before Jan 1, 2026
    if current_date < datetime.date(2026, 1, 1):
        print(f"")
        print(f"✅ Reached Jan 1, 2026. Stopping collection.")
        break

print("")
print("=" * 50)
print(f"📊 Summary:")
print(f"   ✅ Collected: {collected} dates")
print(f"   ⏭️  Skipped: {skipped} dates (already exist)")
if failed:
    print(f"   ❌ Failed: {len(failed)} dates")
    for date in failed:
        print(f"      - {date}")
print("=" * 50)
PY

echo ""
echo "✅ Descending collection completed!"
