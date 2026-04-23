## Learned User Preferences

- Prefer structured planning flows such as `/autoplan` when auditing or refactoring vault automation (e.g. Scripts layout, redundancy cleanup).
- Calendar day notes that include GitHub or dev activity should follow the human-readable narrative style (e.g. `Calendar/2025/December/04-12-2025.md`): Daily Overview, Projects Worked On, readable Work Details; avoid raw imported commit logs and long lists of commit-hash links.
- When refactoring Obsidian automation scripts, prefer removing backward-compatibility shims and keeping one supported code path.

## Learned Workspace Facts

- `Scripts/` layout: `python/` holds `data_collectors` (run `cd Scripts/python && python3 -m data_collectors.main`); shell entrypoints live only in `bash/` (invoke as `bash Scripts/bash/…`); `config/`, `logs/`, `tools/` (e.g. `prune_github_repos.py`). See `Scripts/LAYOUT.txt`.
- GitHub unified collector uses default-branch commits by default; set `GITHUB_COMMITS_ALL_BRANCHES` only when multi-branch scans are required. Tune parallel repo fetches with `GITHUB_FETCH_MAX_WORKERS` (default 8, clamped 1–10). Collection should include AI-authored commits and match personal-account scope where the API and config allow; keep `Scripts/config/unified_data_config.json` aligned with that intent.
- Prefer `GITHUB_TOKEN` or `GITHUB_API_TOKEN` for API auth; avoid committing tokens in `Scripts/config/unified_data_config.json`.
- Trim the tracked repo list with `Scripts/tools/prune_github_repos.py` (uses GitHub `pushed_at`, default 365 days, skips archived repos).
- After scheduled `launchd` runs, check `Scripts/logs/launchd_stderr.log` and `Scripts/logs/unified_data_collector.log` for errors and to confirm fresh run output.
