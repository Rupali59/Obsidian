#!/bin/bash

# Main Data Collection Launcher
# Unified system for GitHub data collection

echo "🚀 Data Collection System"
echo "========================="
echo ""

# Get the Obsidian vault path
OBSIDIAN_PATH="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_PATH="$OBSIDIAN_PATH/Scripts/config/unified_data_config.json"
COLLECTOR_PATH="$OBSIDIAN_PATH/Scripts/data_collectors/main.py"

echo "📁 Obsidian path: $OBSIDIAN_PATH"
echo "⚙️  Config file: $CONFIG_PATH"
echo ""

# Check if config file exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo "❌ Config file not found: $CONFIG_PATH"
    echo "💡 Please create config file from template"
    exit 1
fi

# Function to backfill date range (parallelized)
backfill_range() {
    local start_date=$1
    local end_date=$2
    local parallel_jobs=${3:-8}  # Default to 8 parallel jobs for better performance
    
    echo "📅 Backfilling from $start_date to $end_date (${parallel_jobs} parallel jobs)"
    echo ""
    
    python3 - <<PY
import datetime, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

start = datetime.datetime.strptime("$start_date", "%Y-%m-%d").date()
end = datetime.datetime.strptime("$end_date", "%Y-%m-%d").date()

# Generate all dates to process
dates = []
cur = start
while cur <= end:
    dates.append(cur)
    cur += datetime.timedelta(days=1)

print(f"📊 Processing {len(dates)} dates with ${parallel_jobs} parallel workers")
print("")

def process_date(target_date):
    """Process a single date"""
    try:
        print(f"📆 Processing {target_date}")
        result = subprocess.run([
            "python3",
            "-m", "data_collectors.main",
            "--config", "$CONFIG_PATH",
            "--date", target_date.isoformat()
        ], cwd="$OBSIDIAN_PATH/Scripts", check=False, capture_output=True, text=True)
        
        if result.returncode != 0:
            return (target_date, False, result.stderr)
        return (target_date, True, None)
    except Exception as e:
        return (target_date, False, str(e))

# Process dates in parallel
with ThreadPoolExecutor(max_workers=$parallel_jobs) as executor:
    futures = {executor.submit(process_date, date): date for date in dates}
    
    completed = 0
    failed = []
    
    for future in as_completed(futures):
        target_date, success, error = future.result()
        completed += 1
        
        if success:
            print(f"✅ Completed {target_date} ({completed}/{len(dates)})")
        else:
            print(f"❌ Failed {target_date}: {error}")
            failed.append(target_date)

print("")
print(f"✅ Completed: {len(dates) - len(failed)}/{len(dates)}")
if failed:
    print(f"❌ Failed: {len(failed)} dates")
    for date in failed:
        print(f"   - {date}")
PY
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    echo "📅 Processing today (default)"
    (cd "$OBSIDIAN_PATH/Scripts" && python3 -m data_collectors.main --config "$CONFIG_PATH" --today)
    
elif [ "$1" = "yesterday" ]; then
    echo "📅 Processing yesterday"
    YESTERDAY=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d')
    (cd "$OBSIDIAN_PATH/Scripts" && python3 -m data_collectors.main --config "$CONFIG_PATH" --date "$YESTERDAY")
    
elif [ "$1" = "today" ]; then
    echo "📅 Processing today"
    (cd "$OBSIDIAN_PATH/Scripts" && python3 -m data_collectors.main --config "$CONFIG_PATH" --today)
    
elif [ "$1" = "october" ]; then
    echo "📅 Backfilling October 2025"
    PARALLEL_JOBS=${2:-8}
    backfill_range "2025-10-01" "2025-10-31" "$PARALLEL_JOBS"
    
elif [ "$1" = "november" ]; then
    echo "📅 Backfilling November 2025"
    YESTERDAY=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d')
    PARALLEL_JOBS=${2:-8}
    backfill_range "2025-11-01" "$YESTERDAY" "$PARALLEL_JOBS"
    
elif [ "$1" = "oct-nov" ] || [ "$1" = "backfill" ]; then
    echo "📅 Backfilling October and November 2025"
    YESTERDAY=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d')
    PARALLEL_JOBS=${2:-8}
    backfill_range "2025-10-01" "$YESTERDAY" "$PARALLEL_JOBS"
    
elif [ "$1" = "range" ]; then
    if [ $# -eq 3 ]; then
        echo "📅 Backfilling custom range with 8 parallel jobs (default)"
        backfill_range "$2" "$3" 8
    elif [ $# -eq 4 ]; then
        echo "📅 Backfilling custom range with $4 parallel jobs"
        backfill_range "$2" "$3" "$4"
    else
        echo "❌ Usage: $0 range START_DATE END_DATE [PARALLEL_JOBS]"
        echo "   Default: 8 parallel jobs"
        exit 1
    fi
    
else
    echo "📅 Processing specific date: $1"
    (cd "$OBSIDIAN_PATH/Scripts" && python3 -m data_collectors.main --config "$CONFIG_PATH" --date "$1")
fi

echo ""
echo "✅ Data collection completed!"
