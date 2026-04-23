"""
GitHub data collector module
Fetches commits, PRs, and issues from GitHub repositories
"""

import os
import json
import logging
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import date, datetime
from typing import Dict, List, Optional

from ..utils.config import setup_env, DOTENV_AVAILABLE
from ..utils.helpers import normalize_repo_identifier

if DOTENV_AVAILABLE:
    from dotenv import load_dotenv


def _get_github_fetch_max_workers(num_repos: int) -> int:
    """Cap concurrent repo fetches to reduce secondary rate limits (GitHub abuse detection)."""
    try:
        max_w = int(os.getenv("GITHUB_FETCH_MAX_WORKERS", "8"))
    except ValueError:
        max_w = 8
    max_w = max(1, min(max_w, 10))
    return min(max_w, max(1, num_repos))


def _commits_all_branches_enabled() -> bool:
    """If true, scan every branch (many API calls). Default: default branch only."""
    return os.getenv("GITHUB_COMMITS_ALL_BRANCHES", "").lower() in ("1", "true", "yes")


def _preflight_mode() -> Optional[str]:
    """
    Fast path before scanning every configured repo (Search API vs N parallel repo fetches).

    - None: run full per-repo collection.
    - "repos" (default): committer-date + explicit repo:… OR … (any committer, including AI/bots); same
      repos for issues/PRs created that day. Works for personal accounts (no org: qualifier).
    - "author": only your author identity (cheap; misses AI/bot commits and others' work).
    - "namespace": org:OWNER (single owner); good for orgs; 422 on personal → fall back to full scan.

    Disable: GITHUB_DISABLE_PREFLIGHT=1. Full scan only: GITHUB_PREFLIGHT=off.
    """
    if os.getenv("GITHUB_DISABLE_PREFLIGHT", "").strip().lower() in ("1", "true", "yes"):
        return None
    v = os.getenv("GITHUB_PREFLIGHT", "").strip().lower()
    if v in ("0", "false", "no", "off"):
        return None
    if v in ("", "1", "true", "yes", "repos", "personal"):
        return "repos"
    if v == "author":
        return "author"
    if v == "namespace":
        return "namespace"
    return None


def _rate_limit_is_error(response: requests.Response) -> bool:
    if response.status_code == 429:
        return True
    if response.status_code != 403:
        return False
    remaining = response.headers.get("x-ratelimit-remaining", "")
    if remaining == "0":
        return True
    try:
        error_data = response.json()
        if isinstance(error_data, dict):
            message = error_data.get("message", "").lower()
            if "rate limit" in message or "api rate limit" in message:
                return True
    except Exception:
        pass
    return False


def _rate_limit_wait_seconds(response: requests.Response) -> Optional[int]:
    retry_after = response.headers.get("retry-after")
    if retry_after:
        try:
            return int(retry_after)
        except ValueError:
            pass
    reset_time = response.headers.get("x-ratelimit-reset")
    if reset_time:
        try:
            reset_epoch = int(reset_time)
            return max(0, reset_epoch - int(time.time()))
        except (ValueError, TypeError):
            pass
    return None


def _github_get_with_retry(
    url: str,
    headers: Dict,
    params: Optional[Dict] = None,
    max_retries: int = 3,
    timeout: int = 10,
) -> requests.Response:
    """GET with retries for rate limits and transient errors."""
    retry_count = 0
    last_exception = None

    while retry_count <= max_retries:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)

            if response.status_code == 403 and _rate_limit_is_error(response):
                wait_time = _rate_limit_wait_seconds(response)
                if wait_time is not None and wait_time > 0:
                    reset_time = datetime.fromtimestamp(int(time.time()) + wait_time).strftime("%H:%M:%S")
                    logging.warning(
                        f"Rate limit exceeded. Waiting {wait_time} seconds until reset at {reset_time}..."
                    )
                    time.sleep(wait_time + 1)
                    retry_count += 1
                    continue
                logging.warning("Rate limit exceeded but no reset time available. Waiting 60 seconds...")
                time.sleep(60)
                retry_count += 1
                continue

            if response.status_code == 429:
                wait_time = _rate_limit_wait_seconds(response) or 60
                reset_time = datetime.fromtimestamp(int(time.time()) + wait_time).strftime("%H:%M:%S")
                logging.warning(
                    f"Rate limit exceeded (429). Waiting {wait_time} seconds until reset at {reset_time}..."
                )
                time.sleep(wait_time + 1)
                retry_count += 1
                continue

            if response.status_code in [500, 502, 503, 504]:
                if retry_count < max_retries:
                    wait_time = 2**retry_count
                    logging.warning(
                        f"Server error {response.status_code}. Retrying in {wait_time} seconds... "
                        f"(attempt {retry_count + 1}/{max_retries + 1})"
                    )
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
                response.raise_for_status()

            if response.status_code == 200:
                return response

            if response.status_code in [408, 429]:
                if retry_count < max_retries:
                    wait_time = 2**retry_count
                    logging.warning(f"Status {response.status_code}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue

            return response

        except requests.exceptions.Timeout:
            if retry_count < max_retries:
                wait_time = 2**retry_count
                logging.warning(
                    f"Request timeout. Retrying in {wait_time} seconds... "
                    f"(attempt {retry_count + 1}/{max_retries + 1})"
                )
                time.sleep(wait_time)
                retry_count += 1
                continue
            raise

        except requests.exceptions.ConnectionError as e:
            if retry_count < max_retries:
                wait_time = 2**retry_count
                logging.warning(
                    f"Connection error. Retrying in {wait_time} seconds... "
                    f"(attempt {retry_count + 1}/{max_retries + 1})"
                )
                time.sleep(wait_time)
                retry_count += 1
                last_exception = e
                continue
            raise

        except Exception:
            raise

    if last_exception:
        raise last_exception
    raise Exception(f"Failed after {max_retries + 1} attempts")


def _forbidden_or_ratelimit(response: requests.Response, repo: str, resource: str) -> None:
    """Raise PermissionError on 403 (rate limit or auth). No-op if not 403."""
    if response.status_code != 403:
        return
    if _rate_limit_is_error(response):
        wait_time = _rate_limit_wait_seconds(response) or 3600
        error_msg = (
            f"GitHub API rate limit exceeded for {repo} {resource}. "
            f"Please wait {wait_time} seconds before retrying."
        )
        logging.error(error_msg)
        raise PermissionError(error_msg)
    error_msg = (
        f"GitHub API returned 403 Forbidden for {repo} {resource}. "
        f"Access denied - token may be invalid or expired."
    )
    logging.error(error_msg)
    raise PermissionError(error_msg)


class GitHubCollector:
    """GitHub data collector for commits, PRs, and issues"""

    def __init__(self, token: str, username: str, repositories: List[str]):
        self.token = token
        self.username = username
        self.repositories = repositories
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def _owner_repo(self, repo: str) -> str:
        return normalize_repo_identifier(repo, self.username)

    def _make_request_with_retry(
        self, url: str, params: Optional[Dict] = None, max_retries: int = 3, timeout: int = 10
    ) -> requests.Response:
        return _github_get_with_retry(url, self.headers, params, max_retries, timeout)

    def _search_request(self, path: str, params: Dict) -> requests.Response:
        """GitHub Search API (commits need Cloak preview Accept header)."""
        url = f"{self.api_base}{path}"
        headers = dict(self.headers)
        if path == "/search/commits":
            headers["Accept"] = "application/vnd.github.cloak-preview+json, application/vnd.github+json"
        return _github_get_with_retry(url, headers, params, 3, 10)

    def _unique_repo_owners(self) -> set:
        owners: set = set()
        for repo in self.repositories:
            o = self._owner_repo(repo).split("/")[0]
            if o:
                owners.add(o)
        return owners

    def _search_total_count(self, response: requests.Response) -> Optional[int]:
        if response.status_code != 200:
            return None
        try:
            data = response.json()
            if isinstance(data, dict) and "total_count" in data:
                return int(data["total_count"])
        except (TypeError, ValueError, KeyError):
            pass
        return None

    def _normalized_repo_list(self) -> List[str]:
        """Deduplicated owner/name list from config (order preserved)."""
        seen: set = set()
        out: List[str] = []
        for repo in self.repositories:
            o = self._owner_repo(repo)
            if o and o not in seen:
                seen.add(o)
                out.append(o)
        return out

    def _chunk_repo_search_queries(self, prefix: str) -> List[str]:
        """
        Build GitHub Search `q` strings under the 256-char limit (leave margin).
        Example: committer-date:2026-04-04 (repo:a/b OR repo:a/c)
        """
        repos = self._normalized_repo_list()
        if not repos:
            return []
        try:
            max_len = int(os.getenv("GITHUB_PREFLIGHT_MAX_Q_LEN", "240"))
        except ValueError:
            max_len = 240
        max_len = max(80, min(max_len, 250))
        queries: List[str] = []
        start = 0
        while start < len(repos):
            chunk: List[str] = []
            j = start
            while j < len(repos):
                trial = chunk + [repos[j]]
                if len(trial) == 1:
                    q = f"{prefix} repo:{trial[0]}"
                else:
                    inner = " OR ".join(f"repo:{r}" for r in trial)
                    q = f"{prefix} ({inner})"
                if len(q) > max_len:
                    break
                chunk = trial
                j += 1
            if not chunk:
                logging.warning(
                    "Preflight: cannot fit repo %s in search query (max %s chars); running full scan.",
                    repos[start],
                    max_len,
                )
                return []
            if len(chunk) == 1:
                queries.append(f"{prefix} repo:{chunk[0]}")
            else:
                inner = " OR ".join(f"repo:{r}" for r in chunk)
                queries.append(f"{prefix} ({inner})")
            start = j
        return queries

    def _preflight_should_skip_full_scan(self, date_str: str) -> Optional[bool]:
        """
        Return True to skip per-repo fetches (no activity in preflight scope).
        False = activity found. None = inconclusive; run full scan.
        """
        mode = _preflight_mode()
        if mode is None:
            return None

        if mode == "repos":
            return self._preflight_repo_scoped(date_str)
        if mode == "author":
            return self._preflight_author_scope(date_str)
        if mode == "namespace":
            return self._preflight_namespace_scope(date_str)
        return None

    def _preflight_repo_scoped(self, date_str: str) -> Optional[bool]:
        """
        Personal-account friendly: search commits by committer-date (any author: you, AI, bots)
        and issues/PRs created that day, scoped to configured repos only.
        """
        try:
            max_queries = int(os.getenv("GITHUB_PREFLIGHT_MAX_SEARCH_QUERIES", "24"))
        except ValueError:
            max_queries = 24

        commit_prefix = f"committer-date:{date_str}"
        issue_prefix = f"created:{date_str}"

        commit_qs = self._chunk_repo_search_queries(commit_prefix)
        issue_qs = self._chunk_repo_search_queries(issue_prefix)
        if not commit_qs or not issue_qs:
            logging.info("Preflight repos: no repositories; running full scan.")
            return None

        total_q = len(commit_qs) + len(issue_qs)
        if total_q > max_queries:
            logging.info(
                "Preflight repos: would need %s search queries (max %s); running full scan.",
                total_q,
                max_queries,
            )
            return None

        try:
            for q in commit_qs:
                r = self._search_request("/search/commits", {"q": q, "per_page": 1})
                _forbidden_or_ratelimit(r, "preflight", "commits search")
                if r.status_code == 422:
                    logging.info("Preflight repos: commits search 422 (query rejected); running full scan.")
                    return None
                if r.status_code != 200:
                    logging.info("Preflight repos: commits search HTTP %s; running full scan.", r.status_code)
                    return None
                tc = self._search_total_count(r)
                if tc is None:
                    return None
                if tc > 0:
                    logging.info(
                        "Preflight repos: commit activity in configured repos (hint total_count=%s); full scan.",
                        tc,
                    )
                    return False

            for q in issue_qs:
                r = self._search_request("/search/issues", {"q": q, "per_page": 1})
                _forbidden_or_ratelimit(r, "preflight", "issues search")
                if r.status_code == 422:
                    logging.info("Preflight repos: issues search 422 (query rejected); running full scan.")
                    return None
                if r.status_code != 200:
                    logging.info("Preflight repos: issues search HTTP %s; running full scan.", r.status_code)
                    return None
                tc = self._search_total_count(r)
                if tc is None:
                    return None
                if tc > 0:
                    logging.info(
                        "Preflight repos: issue/PR activity in configured repos (hint total_count=%s); full scan.",
                        tc,
                    )
                    return False
        except PermissionError:
            raise

        logging.info(
            "Preflight repos: no commits (committer-date) and no issues/PRs created on %s in configured repos; "
            "skipping per-repo fetches.",
            date_str,
        )
        return True

    def _preflight_author_scope(self, date_str: str) -> Optional[bool]:
        """Author-scoped Search API: your commits + your issues/PRs created that day."""
        if not self.username:
            logging.info("Preflight author: no username; running full scan.")
            return None

        u = self.username
        q_commits = f"author-date:{date_str} author:{u}"
        q_issues = f"created:{date_str} author:{u}"

        try:
            r1 = self._search_request("/search/commits", {"q": q_commits, "per_page": 1})
            _forbidden_or_ratelimit(r1, "preflight", "commits search")
            if r1.status_code != 200:
                logging.info("Preflight: commits search HTTP %s; running full scan.", r1.status_code)
                return None

            r2 = self._search_request("/search/issues", {"q": q_issues, "per_page": 1})
            _forbidden_or_ratelimit(r2, "preflight", "issues search")
            if r2.status_code != 200:
                logging.info("Preflight: issues search HTTP %s; running full scan.", r2.status_code)
                return None
        except PermissionError:
            raise

        tc1 = self._search_total_count(r1)
        tc2 = self._search_total_count(r2)
        if tc1 is None or tc2 is None:
            return None

        if tc1 == 0 and tc2 == 0:
            logging.info(
                "Preflight (author): no commits and no issues/PRs by %s on %s; skipping per-repo fetches.",
                u,
                date_str,
            )
            return True

        logging.info(
            "Preflight (author): activity hint (commits=%s, issues/prs=%s); running full scan.",
            tc1,
            tc2,
        )
        return False

    def _preflight_namespace_scope(self, date_str: str) -> Optional[bool]:
        """
        org:OWNER searches (best for org-owned repos). Personal accounts may return 0 or 422; then we fall back.
        """
        owners = self._unique_repo_owners()
        if len(owners) != 1:
            logging.info("Preflight namespace: multiple owners %s; running full scan.", owners)
            return None
        owner = next(iter(owners))
        q_commits = f"committer-date:{date_str} org:{owner}"
        q_issues = f"created:{date_str} org:{owner}"

        try:
            r1 = self._search_request("/search/commits", {"q": q_commits, "per_page": 1})
            _forbidden_or_ratelimit(r1, "preflight", "commits search")
            if r1.status_code == 422:
                logging.info("Preflight namespace: commits search not supported for this account; running full scan.")
                return None
            if r1.status_code != 200:
                logging.info("Preflight namespace: commits search HTTP %s; running full scan.", r1.status_code)
                return None

            r2 = self._search_request("/search/issues", {"q": q_issues, "per_page": 1})
            _forbidden_or_ratelimit(r2, "preflight", "issues search")
            if r2.status_code == 422:
                logging.info("Preflight namespace: issues search not supported; running full scan.")
                return None
            if r2.status_code != 200:
                logging.info("Preflight namespace: issues search HTTP %s; running full scan.", r2.status_code)
                return None
        except PermissionError:
            raise

        tc1 = self._search_total_count(r1)
        tc2 = self._search_total_count(r2)
        if tc1 is None or tc2 is None:
            return None

        if tc1 == 0 and tc2 == 0:
            logging.info(
                "Preflight (org:%s): no commits and no issues/PRs on %s; skipping per-repo fetches.",
                owner,
                date_str,
            )
            return True

        logging.info(
            "Preflight (org:%s): activity hint (commits=%s, issues=%s); running full scan.",
            owner,
            tc1,
            tc2,
        )
        return False

    def _commits_list_url(self, owner_repo: str, repo: str) -> str:
        if "/" in owner_repo:
            return f"{self.api_base}/repos/{owner_repo}/commits"
        return f"{self.api_base}/repos/{self.username}/{repo}/commits"

    def _list_branch_names(self, owner_repo: str, repo: str) -> List[str]:
        if "/" in owner_repo:
            branches_url = f"{self.api_base}/repos/{owner_repo}/branches"
        else:
            branches_url = f"{self.api_base}/repos/{self.username}/{repo}/branches"
        names: List[str] = []
        page = 1
        max_pages = 5
        per_page = 100
        while page <= max_pages:
            try:
                response = self._make_request_with_retry(branches_url, params={"per_page": per_page, "page": page})
            except PermissionError:
                raise
            except Exception as e:
                logging.warning(f"Failed to fetch branches page {page} for {repo}: {e}")
                break
            if response.status_code != 200:
                break
            batch = response.json()
            if not batch:
                break
            names.extend(b["name"] for b in batch)
            if len(batch) < per_page:
                break
            page += 1
        return names

    def _process_commits_page(
        self,
        commits_data: List[Dict],
        date_str: str,
        seen_commits: set,
        commit_details: List[Dict],
    ) -> bool:
        for commit in commits_data:
            commit_sha = commit["sha"]
            commit_date = commit["commit"]["committer"]["date"][:10]
            if commit_date == date_str and commit_sha not in seen_commits:
                seen_commits.add(commit_sha)
                commit_msg = commit.get("commit", {}).get("message", "")
                commit_author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
                commit_url = commit.get("html_url", "")
                commit_timestamp = commit.get("commit", {}).get("committer", {}).get("date", "")
                commit_details.append(
                    {
                        "sha": commit_sha[:7],
                        "message": commit_msg.split("\n")[0],
                        "author": commit_author,
                        "url": commit_url,
                        "timestamp": commit_timestamp,
                    }
                )
            elif commit_date < date_str:
                return True
        return False

    def _fetch_commits_for_repo(
        self, owner_repo: str, repo: str, date_str: str, seen_commits: set, commit_details: List[Dict]
    ) -> int:
        commits_url = self._commits_list_url(owner_repo, repo)
        if _commits_all_branches_enabled():
            try:
                branch_names = self._list_branch_names(owner_repo, repo)
                branches: List[Optional[str]] = branch_names if branch_names else [None]
            except PermissionError:
                raise
            except Exception as e:
                logging.warning(f"Failed to list branches for {repo}, using default: {e}")
                branches = [None]
        else:
            branches = [None]

        initial_len = len(commit_details)

        for branch in branches:
            page = 1
            max_pages = 20
            while page <= max_pages:
                params = {
                    "since": f"{date_str}T00:00:00Z",
                    "per_page": 100,
                    "page": page,
                }
                if branch:
                    params["sha"] = branch
                try:
                    response = self._make_request_with_retry(commits_url, params=params)
                except PermissionError:
                    raise
                except Exception as e:
                    logging.warning(f"Failed to fetch commits for {repo} (branch={branch}, page={page}): {e}")
                    break
                if response.status_code == 403:
                    _forbidden_or_ratelimit(response, repo, "commits")
                if response.status_code != 200:
                    break
                commits_data = response.json()
                if not commits_data:
                    break
                stop = self._process_commits_page(commits_data, date_str, seen_commits, commit_details)
                if stop:
                    break
                if len(commits_data) < 100:
                    break
                page += 1

        return len(commit_details) - initial_len

    def _fetch_repo_data(self, repo: str, date_str: str) -> Dict:
        repo_commits = 0
        repo_prs = 0
        repo_issues = 0
        seen_commits = set()
        commit_details = []

        owner_repo = self._owner_repo(repo)

        try:
            repo_commits = self._fetch_commits_for_repo(owner_repo, repo, date_str, seen_commits, commit_details)
        except PermissionError:
            raise
        except Exception as e:
            logging.warning(f"Failed to fetch commits for {repo}: {e}")

        if "/" in owner_repo:
            prs_url = f"{self.api_base}/repos/{owner_repo}/pulls"
        else:
            prs_url = f"{self.api_base}/repos/{self.username}/{repo}/pulls"
        params = {"state": "all", "since": f"{date_str}T00:00:00Z"}

        try:
            response = self._make_request_with_retry(prs_url, params=params)
            _forbidden_or_ratelimit(response, repo, "PRs")
            if response.status_code == 200:
                prs_data = response.json()
                repo_prs = len([pr for pr in prs_data if pr["created_at"].startswith(date_str)])
        except PermissionError:
            raise
        except Exception as e:
            logging.warning(f"Failed to fetch PRs for {repo}: {e}")

        if "/" in owner_repo:
            issues_url = f"{self.api_base}/repos/{owner_repo}/issues"
        else:
            issues_url = f"{self.api_base}/repos/{self.username}/{repo}/issues"
        params = {"state": "all", "since": f"{date_str}T00:00:00Z"}

        try:
            response = self._make_request_with_retry(issues_url, params=params)
            _forbidden_or_ratelimit(response, repo, "issues")
            if response.status_code == 200:
                issues_data = response.json()
                repo_issues = len([issue for issue in issues_data if issue["created_at"].startswith(date_str)])
        except PermissionError:
            raise
        except Exception as e:
            logging.warning(f"Failed to fetch issues for {repo}: {e}")

        display_name = owner_repo.split("/")[-1] if "/" in owner_repo else repo
        return {
            "repo": display_name,
            "commits": repo_commits,
            "prs": repo_prs,
            "issues": repo_issues,
            "commit_details": commit_details,
        }

    def collect_data_for_date(self, target_date: date) -> Dict:
        commits = 0
        prs = 0
        issues = 0
        repository_details = {}
        has_403_error = False
        error_repos = []

        date_str = target_date.strftime("%Y-%m-%d")

        skip_fanout = self._preflight_should_skip_full_scan(date_str)
        if skip_fanout is True:
            print(
                "⚡ Preflight: no commits (any committer) and no issues/PRs created in configured repos; "
                "skipping per-repo API calls. "
                "(GITHUB_PREFLIGHT=off or GITHUB_DISABLE_PREFLIGHT=1 for a full scan.)"
            )
            return {
                "commits": 0,
                "prs": 0,
                "issues": 0,
                "repository_details": {},
                "preflight_skipped_fanout": True,
                "repositories_configured": len(self.repositories),
            }

        max_workers = _get_github_fetch_max_workers(len(self.repositories))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._fetch_repo_data, repo, date_str): repo for repo in self.repositories}

            for future in as_completed(futures):
                try:
                    result = future.result()
                    repo_commits = result["commits"]
                    repo_prs = result["prs"]
                    repo_issues = result["issues"]
                    repo_commit_details = result.get("commit_details", [])

                    commits += repo_commits
                    prs += repo_prs
                    issues += repo_issues

                    if repo_commits > 0 or repo_prs > 0 or repo_issues > 0:
                        repository_details[result["repo"]] = {
                            "commits": repo_commits,
                            "prs": repo_prs,
                            "issues": repo_issues,
                            "commit_details": repo_commit_details,
                        }
                except PermissionError as e:
                    repo = futures[future]
                    has_403_error = True
                    error_repos.append(repo)
                    logging.error(f"403 Forbidden error for {repo}: {e}")
                except Exception as e:
                    repo = futures[future]
                    logging.error(f"Error processing {repo}: {e}")

        if has_403_error:
            error_message = (
                f"\n❌ GITHUB API ACCESS DENIED (403 Forbidden)\n"
                f"   GitHub is not accessible. Please check:\n"
                f"   1. Your GitHub API token is valid and not expired\n"
                f"   2. The token has the necessary permissions\n"
                f"   3. Your network connection is working\n"
                f"   Affected repositories: {', '.join(error_repos[:5])}{'...' if len(error_repos) > 5 else ''}\n"
                f"   Process stopped. No calendar files will be written.\n"
            )
            raise PermissionError(error_message)

        return {
            "commits": commits,
            "prs": prs,
            "issues": issues,
            "repository_details": repository_details,
            "preflight_skipped_fanout": False,
            "repositories_configured": len(self.repositories),
        }


def _fetch_repo_commits(owner_repo: str, token: str, since_iso: str, until_iso: str) -> Dict:
    api_base = "https://api.github.com"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"{api_base}/repos/{owner_repo}/commits"
    params = {"since": since_iso, "until": until_iso, "per_page": 100}
    try:
        resp = _github_get_with_retry(url, headers, params=params, timeout=30)
        if resp.status_code == 403:
            if _rate_limit_is_error(resp):
                wait_time = _rate_limit_wait_seconds(resp) or 3600
                error_msg = f"GitHub API rate limit exceeded for {owner_repo}. Please wait {wait_time} seconds before retrying."
                logging.error(error_msg)
                return {
                    "repository": owner_repo,
                    "error": "HTTP 403 Rate Limit",
                    "commits": [],
                    "is_403": True,
                    "is_rate_limit": True,
                }
            error_msg = f"GitHub API returned 403 Forbidden for {owner_repo}. Access denied - token may be invalid or expired."
            logging.error(error_msg)
            return {"repository": owner_repo, "error": "HTTP 403 Forbidden", "commits": [], "is_403": True}
        if resp.status_code != 200:
            return {"repository": owner_repo, "error": f"HTTP {resp.status_code}", "commits": []}
        data = resp.json()
        commits = []
        for c in data:
            commit_obj = c.get("commit", {})
            message = commit_obj.get("message", "") or ""
            title, _, body = message.partition("\n\n")
            commits.append(
                {
                    "sha": c.get("sha"),
                    "html_url": c.get("html_url"),
                    "title": title.strip(),
                    "description": body.strip(),
                    "author": (commit_obj.get("author") or {}).get("name"),
                    "date": (commit_obj.get("author") or {}).get("date"),
                }
            )
        return {"repository": owner_repo, "commits": commits}
    except Exception as e:
        return {"repository": owner_repo, "error": str(e), "commits": []}


def fetch_commits_parallel_from_config(config_path: str, since_date: date, until_date: date) -> Dict:
    setup_env(Path(config_path))
    if DOTENV_AVAILABLE:
        env_path = Path(config_path).parent.parent.parent / ".env"
        if not env_path.exists():
            env_path = Path(config_path).parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)

    with open(config_path, "r") as f:
        cfg = json.load(f)
    gh_cfg = cfg.get("github", {})
    token = os.getenv("GITHUB_API_TOKEN") or os.getenv("GITHUB_TOKEN") or gh_cfg.get("api_token", "")
    username = os.getenv("GITHUB_USERNAME") or gh_cfg.get("username", "")
    raw_repos = gh_cfg.get("repositories", [])
    repos = [normalize_repo_identifier(r, username) for r in raw_repos]

    since_iso = f"{since_date.isoformat()}T00:00:00Z"
    until_iso = f"{until_date.isoformat()}T23:59:59Z"

    results: Dict[str, List[Dict]] = {}
    errors: Dict[str, str] = {}
    has_403_error = False
    max_workers = _get_github_fetch_max_workers(len(repos))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(_fetch_repo_commits, repo, token, since_iso, until_iso): repo for repo in repos
        }
        for fut in as_completed(future_map):
            repo = future_map[fut]
            res = fut.result()
            if "error" in res and res["error"]:
                errors[repo] = res["error"]
                if res.get("is_403", False) and not res.get("is_rate_limit", False):
                    has_403_error = True
                elif "403" in res["error"] and "Rate Limit" not in res["error"]:
                    has_403_error = True
            results[repo] = res.get("commits", [])

    if has_403_error:
        error_repos = [repo for repo, error in errors.items() if "403" in error]
        error_message = (
            f"\n❌ GITHUB API ACCESS DENIED (403 Forbidden)\n"
            f"   GitHub is not accessible. Please check:\n"
            f"   1. Your GitHub API token is valid and not expired\n"
            f"   2. The token has the necessary permissions\n"
            f"   3. Your network connection is working\n"
            f"   Affected repositories: {', '.join(error_repos[:5])}{'...' if len(error_repos) > 5 else ''}\n"
            f"   Process stopped.\n"
        )
        raise PermissionError(error_message)

    return {
        "since": since_date.isoformat(),
        "until": until_date.isoformat(),
        "total_repositories": len(repos),
        "total_commits": sum(len(c) for c in results.values()),
        "repositories": results,
        "errors": errors,
    }
