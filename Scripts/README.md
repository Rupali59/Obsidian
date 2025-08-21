# 📁 Obsidian Scripts Collection

This directory contains automation scripts for managing your Obsidian vault efficiently.

## 🗂️ Directory Structure

```
Scripts/
├── 📁 calendar_scripts/     # Calendar and daily note management
├── 📁 automation/           # Content synchronization and automation
├── 📁 utilities/            # General utilities and maintenance
└── 📖 README.md            # This documentation
```

## 🚀 Quick Start

### **Content Synchronization**
```bash
# Sync daily notes from Quartz to Obsidian
python Scripts/automation/sync_quartz_to_obsidian.py --all-months

# Clean up daily notes
.\Scripts\utilities\cleanup_daily_notes.ps1 -AllMonths
```

### **Vault Management**
```bash
# Clean up daily notes
.\Scripts\utilities\cleanup_daily_notes.ps1 -AllMonths

# Backup vault
Scripts\utilities\backup_obsidian_vault.bat
```

## 🔧 Script Details

### **Calendar Scripts**
- **`update_github_activity.ps1`**: Updates GitHub activity sections in daily notes
  - **Usage**: `.\Scripts\calendar_scripts\update_github_activity.ps1 -AllMonths`
  - **Features**: Fetches exact commits from git log, updates daily notes

### **Automation Scripts**
- **`sync_quartz_to_obsidian.py`**: Syncs daily note content from Quartz calendar
  - **Usage**: `python Scripts/automation/sync_quartz_to_obsidian.py --all-months`
  - **Features**: Content extraction, logging, statistics, error handling

### **Utility Scripts**
- **`cleanup_daily_notes.ps1`**: Cleans up daily note formatting
  - **Usage**: `.\Scripts\utilities\cleanup_daily_notes.ps1 -AllMonths`
  - **Features**: Format cleanup, location removal, corrupted content fix

- **`backup_obsidian_vault.bat`**: Creates timestamped vault backups
  - **Usage**: Double-click or run from command line
  - **Features**: Smart exclusions, backup rotation, size calculation

- **`script_manager.ps1`**: Menu-driven script launcher
  - **Usage**: `.\Scripts\utilities\script_manager.ps1`
  - **Features**: Interactive menu, script categorization, easy execution

## 📋 Script Updates

### **Recent Changes**
- **Removed Sync Scripts**: Sync functionality has been removed
- **Enhanced Content Sync**: Better error handling and logging
- **Streamlined Utilities**: Focused on core vault management

## ⚠️ Important Notes

- **Scripts folder is excluded** from Obsidian via `.obsidianignore`
- **Sync functionality removed** - scripts focus on vault management
- **Use descriptive commit messages** for better tracking when using git manually
- **Keep backups** before running automation scripts

## 🆘 Troubleshooting

### **Common Issues**
1. **Permission denied**: Run PowerShell as Administrator
2. **Python not found**: Install Python from https://python.org/
3. **Script errors**: Check script help with no parameters

### **Getting Help**
- Check script help: `.\script_name.ps1` (no parameters)
- Review script documentation in this README

## 🎯 Best Practices

1. **Test First**: Always test scripts on sample data
2. **Backup Strategy**: Use backup script before major changes
3. **Script Management**: Use script manager for easy access
4. **Documentation**: Keep scripts well-documented

---

**💡 Tip**: Focus on vault management and content synchronization!
