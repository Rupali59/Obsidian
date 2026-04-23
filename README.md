# 📓 Obsidian Vault - Personal Knowledge Management System

An automated Obsidian vault for personal knowledge management, daily activity tracking, and GitHub activity integration. This repository serves as both a digital garden and a comprehensive work tracking system with automated calendar entries.

## 🌟 Features

- **📅 Automated Daily Calendar Entries**: Automatic collection and formatting of GitHub activity into daily calendar notes
- **🚀 GitHub Activity Integration**: Collects commits, pull requests, and issues across multiple repositories
- **📊 Development Analytics**: Track development patterns, work summaries, and technical insights
- **🔄 Automated Data Collection**: Daily automated collection via launchd (macOS) or cron
- **📝 Structured Note Taking**: Organized calendar structure with formatted entries by year and month
- **🏷️ Tag-based Organization**: Project and concept tagging for easy navigation and filtering

## 📁 Repository Structure

```
Obsidian/
├── Calendar/              # Daily calendar entries organized by year/month
│   ├── 2024/             # 2024 calendar entries
│   ├── 2025/             # 2025 calendar entries
│   └── 2026/             # 2026 calendar entries
├── Notes/                # General notes and knowledge base
├── Scripts/              # Automation (see Scripts/LAYOUT.txt)
│   ├── bash/             # Shell entrypoints (launchers, automation)
│   ├── config/           # JSON + launchd plist
│   ├── logs/             # Execution logs
│   ├── python/           # Python package (`data_collectors`)
│   └── tools/            # One-off maintenance scripts
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- GitHub Personal Access Token
- macOS (for launchd automation) or Unix-like system (for cron)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rupali59/Obsidian.git
   cd Obsidian
   ```

2. **Configure your settings**
   ```bash
   cp Scripts/config/unified_data_config.json.template Scripts/config/unified_data_config.json
   # Edit Scripts/config/unified_data_config.json with your GitHub token and repositories
   ```

3. **Set up automation (macOS)**
   ```bash
   bash Scripts/bash/setup_automation.sh install
   ```

### Configuration

Edit `Scripts/config/unified_data_config.json`:

- **GitHub Token**: Add your GitHub Personal Access Token
- **Username**: Set your GitHub username
- **Repositories**: List all repositories to track
- **Obsidian Path**: Update vault path if needed (auto-detected on install)

## 📖 Usage

### Manual Data Collection

Collect data for a specific date (from vault root; default config path is resolved automatically):
```bash
cd Scripts/python && python3 -m data_collectors.main --date 2026-01-10
```

Or use the launcher:
```bash
bash Scripts/bash/run_data_collection.sh 2026-01-10
```

Collect data for today:
```bash
cd Scripts/python && python3 -m data_collectors.main --today
```

Fetch commits in a date range:
```bash
cd Scripts/python && python3 -m data_collectors.main --commits-range 2026-01-01 2026-01-10
```

### Automated Collection

The system can be configured to run automatically:

- **macOS**: Uses launchd (configured via `Scripts/bash/setup_automation.sh`)
- **Linux/Unix**: Use cron with `Scripts/bash/daily_auto_collect.sh`

### Calendar Entry Format

Each daily entry includes:
- Daily Overview with activity summary
- GitHub Activity with detailed project work
- Development Analytics with metrics and insights
- Tags for project and concept organization

Example entry format:
```markdown
# January 10, 2026

**#project/ProjectName #concept/ConceptType**

## 📊 Daily Overview
**Total Activity:** X commits across Y repositories

## 🚀 GitHub Activity
### Development Summary
[Detailed project work summaries]

## 📈 Development Analytics
[Metrics and technical insights]
```

## 🛠️ Scripts

See `Scripts/LAYOUT.txt` for the folder map. Short list:

- **`python/data_collectors/main.py`**: Collector entry (run via `python3 -m data_collectors.main` from `Scripts/python/`)
- **`bash/daily_auto_collect.sh`**: Daily automated collection (LaunchAgent target)
- **`bash/setup_automation.sh`**: Automation setup and management
- **`bash/run_data_collection.sh`**: Manual collection launcher

## 🔧 Automation Management

```bash
# Install automation
bash Scripts/bash/setup_automation.sh install

# Check status
bash Scripts/bash/setup_automation.sh status

# Stop automation
bash Scripts/bash/setup_automation.sh stop

# Start automation
bash Scripts/bash/setup_automation.sh start

# View logs
bash Scripts/bash/setup_automation.sh logs
```

## 📝 Calendar Structure

- **Year Folders**: `Calendar/YYYY/`
- **Month Folders**: `Calendar/YYYY/MonthName/`
- **Daily Files**: `Calendar/YYYY/MonthName/DD-MM-YYYY.md`
- **Month Index**: `Calendar/YYYY/MonthName/MonthName YYYY.md`

## 🔐 Security

- Prefer `GITHUB_API_TOKEN` or `GITHUB_TOKEN` in the environment; optional fallback in `Scripts/config/unified_data_config.json`
- **Never commit** your actual config file with tokens
- Use `.gitignore` to exclude sensitive files
- The template file (`unified_data_config.json.template`) is safe to commit

## 📊 Data Collection

The system tracks:
- **Commits**: Number of commits per repository
- **Pull Requests**: PR creation and activity
- **Issues**: Issue tracking and updates
- **Repository Details**: Per-repository activity breakdowns
- **Commit Messages**: Links to actual commits with descriptions

## 🏷️ Tagging System

Entries use Obsidian tags for organization:
- **Projects**: `#project/ProjectName`
- **Concepts**: `#concept/ConceptType` (e.g., `#concept/Maintenance`, `#concept/Feature-Development`)

## 📚 Related Projects

- [WorkTracker](https://github.com/Rupali59/WorkTracker): Public-facing work tracking visualization
- [Rupali59](https://github.com/Rupali59/Rupali59): Personal profile repository

## 🤝 Contributing

This is a personal knowledge management system, but suggestions and improvements are welcome!

## 📄 License

This repository is for personal use. Feel free to fork and adapt for your own use.

## 👤 Author

**Rupali Bhatnagar**
- GitHub: [@Rupali59](https://github.com/Rupali59)
- Website: [tathya.dev](https://tathya.dev)

## 🙏 Acknowledgments

- Built with [Obsidian](https://obsidian.md/) - A powerful knowledge base
- Automated with Python and shell scripts
- Integrated with GitHub API for activity tracking

---

**Note**: This vault is automatically synced and updated with daily development activity. Calendar entries are generated automatically and formatted consistently for easy browsing and analysis.
