# Unified Parallel Runner

## Overview
Single script for all GitHub metrics capture using configuration files and optimized GraphQL batching.

## Features
- **Single Script**: One script handles all GitHub metrics capture
- **Configuration-Based**: Uses JSON config files from `Scripts/parallel/configs/`
- **Optimized API Usage**: Reduces API calls from 36+ to ~4-6 per day
- **Parallel Processing**: Processes multiple repositories simultaneously
- **Flexible Date Handling**: Supports today, yesterday, or specific dates
- **Calendar Integration**: Automatically updates Obsidian calendar entries

## Usage

### Basic Commands
```bash
# Process today (default)
./run_unified.sh

# Process yesterday
./run_unified.sh yesterday

# Process today explicitly
./run_unified.sh today

# Process specific date
./run_unified.sh 2025-09-10
```

### Advanced Usage
```bash
# Process today without updating calendar
python3 unified_parallel_runner.py . --today --no-calendar

# Process yesterday with custom config
python3 unified_parallel_runner.py . --yesterday --config september_2025

# Process specific date
python3 unified_parallel_runner.py . --date 2025-09-10
```

## Configuration
The script uses configuration files from `Scripts/parallel/configs/`:
- `september_2025.json` - September 2025 configuration
- `august_2025.json` - August 2025 configuration
- `year_2025.json` - Full year 2025 configuration

### Config File Format
```json
{
  "name": "September 2025 Capture",
  "description": "Capture GitHub metrics for September 2025",
  "start_date": "2025-09-01",
  "end_date": "2025-09-03",
  "parallel_workers": 3,
  "rate_limit_delay": 0.3,
  "progress_interval": 5
}
```

## Output
- **Console**: Real-time progress and summary
- **Calendar Files**: Updated markdown files in `Calendar/YYYY/Month/DD-MM-YYYY.md`
- **Logs**: Detailed logs in `github_batched_metrics.log`

## Benefits
1. **Consolidation**: Single script instead of multiple scripts
2. **Efficiency**: Optimized API usage with GraphQL batching
3. **Configuration**: Easy to modify behavior via JSON configs
4. **Flexibility**: Supports various date ranges and options
5. **Maintenance**: Easier to maintain and update

## Migration from Old Scripts
Replace these scripts with the unified runner:
- `capture_today.py` → `unified_parallel_runner.py --today`
- `run_optimized_today.sh` → `run_unified.sh today`
- `run_today_parallel.sh` → `run_unified.sh today`
- `parallel_repo_runner.py` → `unified_parallel_runner.py`

## Requirements
- Python 3.9+
- GitHub API token configured in `Scripts/config/github_config.env`
- Repository list in `Scripts/config/repos_to_track.env`
