#!/usr/bin/env python3
"""
Trim github.repositories in unified_data_config.json to repos that still exist on GitHub
and had a push within the last N days (default 365). Skips archived repos.

Auth: GITHUB_TOKEN or GITHUB_API_TOKEN, or `gh auth token` if available.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import requests

# tools/ -> parents[1] == Scripts/
_SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCRIPTS / "python"))
from data_collectors.utils.helpers import normalize_repo_identifier  # noqa: E402


def _token() -> str:
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_API_TOKEN")
    if t:
        return t.strip()
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception:
        return ""


def fetch_repo_meta(session: requests.Session, owner_repo: str) -> Optional[dict]:
    r = session.get(f"https://api.github.com/repos/{owner_repo}", timeout=30)
    if r.status_code != 200:
        return None
    return r.json()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--config",
        type=Path,
        default=_SCRIPTS / "config" / "unified_data_config.json",
        help="Path to unified_data_config.json",
    )
    p.add_argument("--days", type=int, default=365, help="Keep repos pushed within this many days")
    p.add_argument("--dry-run", action="store_true", help="Print plan only; do not write")
    args = p.parse_args()

    token = _token()
    if not token:
        print("No token: set GITHUB_TOKEN or GITHUB_API_TOKEN, or run `gh auth login`", file=sys.stderr)
        return 1

    with open(args.config) as f:
        cfg = json.load(f)

    gh = cfg.get("github", {})
    username = gh.get("username", "")
    raw = gh.get("repositories", [])

    seen: set[str] = set()
    repos: list[str] = []
    for entry in raw:
        n = normalize_repo_identifier(entry, username)
        if not n or n in seen:
            continue
        seen.add(n)
        repos.append(n)

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
    )

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    kept: list[tuple[str, datetime]] = []
    dropped: list[tuple[str, str]] = []

    for owner_repo in repos:
        data = fetch_repo_meta(session, owner_repo)
        if not data:
            dropped.append((owner_repo, "not found or API error"))
            continue
        pushed = data.get("pushed_at")
        if not pushed:
            dropped.append((owner_repo, "no pushed_at"))
            continue
        pushed_dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
        if data.get("archived"):
            dropped.append((owner_repo, "archived"))
            continue
        if pushed_dt < cutoff:
            dropped.append((owner_repo, f"last push {pushed_dt.date()} (before cutoff)"))
            continue
        kept.append((data["full_name"], pushed_dt))

    kept.sort(key=lambda x: x[1], reverse=True)
    names = [k[0] for k in kept]

    print(f"Cutoff: pushes on or after {cutoff.date()} ({args.days} days)")
    print(f"Input unique repos: {len(repos)}")
    print(f"Keeping: {len(names)}")
    print(f"Dropping: {len(dropped)}")
    for repo, reason in dropped:
        print(f"  - {repo}: {reason}")

    if args.dry_run:
        print("\nDry run; not writing.")
        return 0

    cfg["github"]["repositories"] = names
    meta = cfg.setdefault("metadata", {})
    meta["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    with open(args.config, "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")

    print(f"\nWrote {len(names)} repos to {args.config}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
