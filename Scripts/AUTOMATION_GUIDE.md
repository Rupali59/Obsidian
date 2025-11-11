# Daily Data Collection Automation Guide

This guide explains how to set up automatic daily data collection that runs at 10 PM every day.

## 📋 Overview

The automation system collects GitHub activity data daily and updates your Obsidian calendar files automatically. No manual intervention needed!

### What Gets Collected Daily:
- ✅ Commits from all branches
- ✅ Pull Requests
- ✅ Issues
- ✅ Repository activity summaries

### When It Runs:
- **Time**: 10:00 PM every day
- **Duration**: ~30 seconds (with 20 repos)
- **Auto-retry**: If fails, will try again next day

---

## 🚀 Quick Setup (3 steps)

### Step 1: Install the Automation

```bash
cd /Users/rupali.b/Documents/GitHub/Obsidian
bash Scripts/setup_automation.sh install
```

### Step 2: Verify It's Running

```bash
bash Scripts/setup_automation.sh status
```

You should see: ✅ **Status: Running**

### Step 3: Test It (Optional)

```bash
bash Scripts/setup_automation.sh test
```

This runs data collection immediately to verify everything works.

---

## 📚 Available Commands

### Install/Uninstall
```bash
# Install automation (set up to run at 10 PM daily)
bash Scripts/setup_automation.sh install

# Uninstall automation (remove completely)
bash Scripts/setup_automation.sh uninstall
```

### Control
```bash
# Start automation
bash Scripts/setup_automation.sh start

# Stop automation
bash Scripts/setup_automation.sh stop

# Restart automation
bash Scripts/setup_automation.sh restart
```

### Monitor
```bash
# Check if automation is running
bash Scripts/setup_automation.sh status

# View recent logs
bash Scripts/setup_automation.sh logs

# Run data collection manually (test)
bash Scripts/setup_automation.sh test
```

---

## 📂 File Structure

```
Scripts/
├── daily_auto_collect.sh           # Main automation script
├── setup_automation.sh             # Setup/management tool
├── com.obsidian.dailycollect.plist # macOS launch agent config
├── run_data_collection.sh          # Manual collection tool
├── data_collectors/
│   └── unified_data_collector.py   # Python collector
├── config/
│   └── unified_data_config.json    # Configuration
└── logs/
    ├── daily_auto_collect.log      # Automation logs
    ├── launchd_stdout.log          # System stdout
    └── launchd_stderr.log          # System errors
```

---

## 🔍 Troubleshooting

### Check if Automation is Running
```bash
launchctl list | grep obsidian
```
Should show: `com.obsidian.dailycollect`

### View Live Logs
```bash
tail -f Scripts/logs/daily_auto_collect.log
```

### Common Issues

#### 1. **"Not installed" error**
**Solution**: Run the install command first:
```bash
bash Scripts/setup_automation.sh install
```

#### 2. **GitHub API Rate Limit**
**Problem**: Too many API requests
**Solution**: The daily automation makes fewer requests than manual backfills. If you hit the limit:
- Wait 1 hour for rate limit reset
- Or use a different GitHub token

#### 3. **No data collected**
**Check**:
```bash
# Verify config file exists
ls Scripts/config/unified_data_config.json

# Test manual collection
bash Scripts/setup_automation.sh test
```

#### 4. **Permission denied**
**Solution**: Make scripts executable:
```bash
chmod +x Scripts/*.sh
```

---

## 🔧 Customization

### Change Collection Time

Edit the plist file: `Scripts/com.obsidian.dailycollect.plist`

Change the hour (0-23):
```xml
<key>Hour</key>
<integer>22</integer>  <!-- 22 = 10 PM -->
<key>Minute</key>
<integer>0</integer>
```

Then restart:
```bash
bash Scripts/setup_automation.sh restart
```

### Change What Gets Collected

Edit: `Scripts/config/unified_data_config.json`

Modify the `repositories` array to add/remove repos.

---

## 📊 Log Files

### Automation Log
**Location**: `Scripts/logs/daily_auto_collect.log`
**Contains**: Detailed collection results, timestamps, errors

### System Logs
**Location**: 
- `Scripts/logs/launchd_stdout.log` - Standard output
- `Scripts/logs/launchd_stderr.log` - Error output

### View Logs
```bash
# View automation log
bash Scripts/setup_automation.sh logs

# Or directly
tail -50 Scripts/logs/daily_auto_collect.log
```

---

## 🔐 Security Notes

1. **GitHub Token**: Stored in `Scripts/config/unified_data_config.json`
   - Make sure this file is in `.gitignore`
   - Don't commit your token to git

2. **Logs**: May contain API responses
   - Added to `.gitignore` automatically
   - Safe to delete old logs

---

## 💡 Tips

### Backfill Historical Data
The automation only collects TODAY's data. To backfill past dates:

```bash
# Backfill October
bash Scripts/run_data_collection.sh october 4

# Backfill specific date range
bash Scripts/run_data_collection.sh range 2025-09-01 2025-09-30 4
```

### Monitor API Usage
Check your GitHub API rate limit:
```bash
curl -H "Authorization: token YOUR_TOKEN" \
  "https://api.github.com/rate_limit" | python3 -m json.tool
```

### Disable for Vacation
```bash
# Stop automation
bash Scripts/setup_automation.sh stop

# Resume when back
bash Scripts/setup_automation.sh start
```

---

## 📝 What Happens Daily

1. **10:00 PM**: macOS launches the automation script
2. **Collect Data**: Fetches today's GitHub activity from all repos
3. **Update Calendar**: Creates/updates today's markdown file in `Calendar/YYYY/Month/`
4. **Log Results**: Saves success/failure to log file
5. **Exit**: Waits until next day

**Total Time**: ~30 seconds  
**System Impact**: Minimal (only runs once per day)

---

## 🆘 Support

If something isn't working:

1. Check status: `bash Scripts/setup_automation.sh status`
2. View logs: `bash Scripts/setup_automation.sh logs`
3. Test manually: `bash Scripts/setup_automation.sh test`
4. Restart: `bash Scripts/setup_automation.sh restart`

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Status shows "Running"
- [ ] Test run completes successfully
- [ ] Today's calendar file gets updated
- [ ] Logs show no errors
- [ ] API rate limit is not exceeded

Done! Your daily data collection is now automated! 🎉

