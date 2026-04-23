# How This Journal Works

#system/journal #system/architecture

This vault is a self-writing journal. Every night, a Python script wakes up, queries
your GitHub activity, and writes a daily summary into `Calendar/YYYY/MonthName/DD-MM-YYYY.md`.
You open the vault in the morning and the day before is already documented.

This note explains how it works, where it is today, and where it's going.

*Last verified: April 22, 2026*

> [!private]
> Vault-only test marker. If you can read this on rupali59.github.io/WorkTracker,
> the StripPrivateCallouts plugin is broken. Reachable in Obsidian as a styled
> callout block.

---

## What it does right now

The nightly job runs via macOS **launchd** at 10 PM. It calls one script:

```
bash Scripts/bash/daily_auto_collect.sh
```

That script activates the Python venv and runs:

```
cd Scripts/python && python3 -m data_collectors.main --today
```

The Python package does three things:

1. **Collect** — `collectors/github.py` fetches your commits from every tracked repo
   via the GitHub REST API. It reads which repos to track from `Scripts/config/unified_data_config.json`.

2. **Format** — `obsidian_calendar/formatter.py` transforms the raw commit data into
   a Markdown calendar entry. Today it uses keyword matching to generate section headers
   and "insights" like "feature development." This is the part that will be replaced.

3. **Write** — `obsidian_calendar/updater.py` writes the Markdown to the correct
   calendar file path, creating the month directory if needed.

If a date already has an entry, the updater leaves it alone. To overwrite (e.g. backfilling April with better output), delete the target file first, then re-run.

---

## The data flow

```
launchd (10 PM)
  → daily_auto_collect.sh
    → python3 -m data_collectors.main --today
      → GitHubCollector.collect(date)
          → GitHub REST API → raw commits
      → formatter.py → Markdown
      → updater.py → Calendar/YYYY/Month/DD-MM-YYYY.md
```

---

## Where it's going (target architecture)

The formatter will be replaced with an **LLM synthesizer** that calls the Claude API
to write a narrative entry — the same quality as the December 2025 entries, every day.

Two new components:

### BaseCollector (`collectors/base.py`)
An abstract interface that every data source implements:
- `collect(date)` → structured dict
- `is_available()` → True/False (graceful degradation if source is unavailable)

### BrowserHistoryCollector (`collectors/browser.py`)
Reads Chrome (or Safari) history for the day — how many visits to which domains,
which pages were meaningful. Adds context beyond code: "I spent 45 minutes reading
Anthropic docs, 20 minutes on GitHub."

### JournalSynthesizer (`synthesizer.py`)

**Input:** dict of collector results, keyed by collector name. Each value is a structured dict (e.g., `{"github": {...repos, commits, languages}, "browser": {...domains, notable_pages}}`).

**Output:** A Markdown string. `updater.py` is responsible for writing it to disk — the synthesizer never touches the filesystem.

**Failure modes:**
- API timeout (>30s) → fall back to `formatter.py` keyword logic
- Malformed response (not valid Markdown / missing required sections) → fall back to `formatter.py`
- API refusal / safety filter trigger → fall back to `formatter.py`, log the trigger reason

**Key injection:** Set `ANTHROPIC_API_KEY` in your shell environment (`export ANTHROPIC_API_KEY=sk-ant-...`) or in `unified_data_config.json` under `anthropic.api_key`. The env var takes precedence.

**Model:** `claude-3-5-haiku-20241022` (~$0.001/day for typical journal length). Note the `3-5` (number-first) format — `claude-haiku-3-5-...` is wrong and will 404.

**Target data flow:**

```
launchd (10 PM)
  → daily_auto_collect.sh
    → python3 -m data_collectors.main --today
      → GitHubCollector.collect(date)      → { repos, commits, languages }
      → BrowserHistoryCollector.collect(date) → { domains, notable_pages }
      → JournalSynthesizer.synthesize(date, results)
          → Claude API (claude-3-5-haiku-20241022)
          → full Markdown narrative (or fallback to formatter.py)
      → updater.py → Calendar/YYYY/Month/DD-MM-YYYY.md
```

---

## Consolidation roadmap

These are the phases, in order:

**Phase 1: Optimize the architecture**
- Add `collectors/base.py` (BaseCollector interface)
- Replace `formatter.py` keyword matching with `synthesizer.py` (Claude API)
- Update `main.py` to use the plugin registration pattern: collectors are instantiated in a list and iterated — `[GitHubCollector(...), BrowserHistoryCollector(...)]` — rather than being hardcoded in sequence
- Update `unified_data_config.json.template` with `anthropic` and `browser` config blocks

**Phase 2: Fix April entries**
- Pre-condition: run `bash Scripts/bash/setup_automation.sh status` and check `Scripts/logs/unified_data_collector.log` — confirm whether the job is firing and what error it's producing. This diagnosis must happen before backfilling.
- Backfill April entries using the new synthesizer: delete existing broken entries, then run `--commits-range`. The `--commits-range` end date is exclusive (e.g. `2026-04-01 2026-04-23` to include April 22).

**Phase 3: Browser history**
- Pre-condition: grant **Full Disk Access** to the Python binary (`/usr/bin/python3`) in System Settings → Privacy & Security → Full Disk Access. Granting it to Terminal alone is not sufficient for launchd-triggered runs — the background agent runs Python directly.
- Add `collectors/browser.py` (BrowserHistoryCollector for Chrome/Safari)
- Add `browser.enabled` config, noise filter for junk URLs — filter spec belongs in the Phase 3 design doc
- Entries now reflect research + reading, not just code

**Phase 4: Searchable view** (deferred — approach TBD once Phase 3 is done)

---

## Files that matter

| File | What it does |
|------|-------------|
| `Scripts/config/unified_data_config.json` | Runtime config — repo list, GitHub token path, vault path |
| `Scripts/config/unified_data_config.json.template` | Template for new installs — safe to commit |
| `Scripts/config/com.obsidian.dailycollect.plist` | launchd job definition — schedules the 10 PM run |
| `Scripts/bash/setup_automation.sh` | Install/uninstall/check the launchd job |
| `Scripts/bash/daily_auto_collect.sh` | Called by launchd — activates venv + runs main.py |
| `Scripts/python/data_collectors/main.py` | Orchestrator — registers collectors, runs pipeline |
| `Scripts/python/data_collectors/collectors/github.py` | GitHub API integration |
| `Scripts/python/data_collectors/obsidian_calendar/formatter.py` | Markdown formatter (will be replaced by synthesizer) |
| `Scripts/python/data_collectors/obsidian_calendar/updater.py` | Writes/updates calendar files |
| `Scripts/tools/prune_github_repos.py` | Removes stale repos from config (365-day inactivity threshold) |
| `Scripts/logs/unified_data_collector.log` | Daily run log — check here if entries are missing |
| `Scripts/logs/launchd_stderr.log` | launchd error output — check here if the job isn't firing |

---

## Quick reference

```bash
# Check if the daily job is scheduled
bash Scripts/bash/setup_automation.sh status

# Run manually for today
cd Scripts/python && /usr/bin/python3 -m data_collectors.main --today

# Run for a specific date
cd Scripts/python && /usr/bin/python3 -m data_collectors.main --date 2026-04-15

# Backfill a range (end date is exclusive — use Apr 23 to include Apr 22)
cd Scripts/python && /usr/bin/python3 -m data_collectors.main --commits-range 2026-04-01 2026-04-23

# Trim stale repos from config
/usr/bin/python3 Scripts/tools/prune_github_repos.py

# Install launchd job
bash Scripts/bash/setup_automation.sh install
```

**Python note:** use `/usr/bin/python3` directly. The `.venv` at repo root is empty (never populated) — running `source activate_venv.sh` does nothing harmful but is not required.
`requests` is at `~/Library/Python/3.9`. If that path breaks after a Python upgrade, run `pip3 install requests` to reinstall it.

---

## Why this exists

The canonical quality reference is `Calendar/2025/December/04-12-2025.md`. Every
decision about entry format, narrative style, and section structure should be
checked against that file. The goal is entries that look like that one, every day,
automatically.
