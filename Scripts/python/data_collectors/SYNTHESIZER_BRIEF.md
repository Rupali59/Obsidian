# Brief: implement the Gemma synthesizer (Phase 1)

Hand this file (or its path) to a fresh Claude Code session. Self-contained — no
need to load the prior conversation.

## Read these first (in order)
1. `Notes/System/Architecture.md` — full target architecture; **Phase 1** is what to build
2. `Calendar/2025/December/04-12-2025.md` — the quality bar; output must look like this
3. `Scripts/python/data_collectors/main.py` — current orchestrator, will be refactored
4. `Scripts/python/data_collectors/collectors/github.py` — current collector, becomes a BaseCollector subclass
5. `Scripts/python/data_collectors/obsidian_calendar/formatter.py` — current keyword formatter, becomes the fallback path
6. `Scripts/python/data_collectors/obsidian_calendar/updater.py` — disk writer, unchanged

## Build (in order)
1. **`collectors/base.py`** — ABC with `collect(date) -> dict` and `is_available() -> bool`
2. **Refactor `collectors/github.py`** to subclass `BaseCollector`
3. **`synthesizer.py`** — Gemma via Ollama. Inputs: `(date, collector_results, prior_context)` where `prior_context` is a list of the prior 7 days' Markdown read off disk. Output: Markdown string. Use the `ollama` Python package (`pip install ollama`). Default model from config: `ollama.model` (default `gemma3:27b`).
4. **`diagram_generator.py`** — Gemini Nano Banana via `google-genai`. Two calls: a small "diagram needed?" classifier (Gemma), then if yes, image gen with the description. Save PNG to `Calendar/diagrams/YYYY-MM-DD-<slug>.png`. Env: `GEMINI_API_KEY`.
5. **Refactor `main.py`** to the plugin pattern: `collectors = [GitHubCollector(...), BrowserHistoryCollector(...) if available]`, iterate, pass results to synthesizer.
6. **Update `Scripts/config/unified_data_config.json.template`** with `ollama: { host, model }` and `gemini: { api_key }` blocks.

## Quality gate (run before declaring done)
```bash
ollama pull gemma3:27b
curl -s http://localhost:11434/api/tags | grep -q gemma3 && echo ok
cd Scripts/python && /usr/bin/python3 -m data_collectors.main --date 2026-04-22
diff Calendar/2026/April/22-04-2026.md Calendar/2025/December/04-12-2025.md  # eyeball: similar structure, narrative quality, tag style
```
Iterate the synthesizer prompt until the output matches Dec 2025 in: narrative tone, section structure, tag consistency, `[[YYYY-MM-DD]]` interconnection.

## Failure modes (must handle, see Architecture.md "Failure modes" section)
- Ollama not running → fall back to `formatter.py`
- Gemma response malformed → fall back to `formatter.py`
- Gemma >60s → fall back, log
- Gemini Nano Banana fail → emit Markdown without diagram, log
- Historical repo gone → narrate the gap, never fabricate

## Don't redo (already shipped this week)
- `[!private]` callout stripping (Quartz transformer in WorkTracker)
- Vault → WorkTracker sync (manifest + GitHub Actions chain)
- Notes/System/Architecture.md (the spec — read it, don't rewrite it)
- Hardlink + ci-sync infrastructure

## Success
A nightly run produces a December-2025-quality entry. Backfill April. Some days will be partial (deleted repos) — note them in `Calendar/_partial-days.md`, not silently.
