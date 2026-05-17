# CHERENKOV Agent Memory
## Technical Decisions & Lessons Learned

### Architecture
- **Monorepo layout**: All source under `packages/cherenkov/`. Root is clean — only config files, Dockerfiles, and multi-agent coordination docs. Do not add scripts or test files to root.
- **Import path**: Always `from cherenkov.core.X import Y`, never `from src.cherenkov.X`.
- **`@` alias** in React maps to `packages/cherenkov/web/` (package root), so imports are `@/src/lib/api`, `@/src/hooks/useMetrics`, etc.

### Version
- Canonical version is **1.1.0** everywhere: `pyproject.toml`, `packages/cherenkov/web/package.json`, FastAPI app `version="1.1.0"`.
- Git milestone tag for this release: `v1.1.0` (AGENTS.md milestone: `v1.1.0 — Swarm Concurrency`).
- Do not bump version without updating all three locations.

### Backend (FastAPI — `packages/cherenkov/api/main.py`)
- `/api/v1/*` routes are on `v1 = APIRouter(prefix="/api/v1")` registered at the bottom of main.py.
- WebSocket is at `/ws/live` — singleton broadcast hub `_ws_clients: Set[WebSocket]`.
- **Rate limiting**: `slowapi` (not custom middleware). Scan endpoints: `CHERENKOV_SCAN_RATE_LIMIT` (default 20/min). Workflow: `CHERENKOV_WORKFLOW_RATE_LIMIT` (default 10/min). Both env-configurable.
- **Health endpoint** (`GET /api/v1/health`): fully wired — live Ollama check, Meissner circuit breaker state, active scan count from SQLite, Qdrant vector count, Docker container count. Legacy `GET /health` delegates to `v1_health()`.
- **Right-to-erasure** (`DELETE /api/v1/data/target`): ADMIN-only. Nulls findings payload, purges audit_log entries for a target URL, returns signed erasure receipt. Law 151/2020 Art. 15 compliance.
- CORS: `allow_origins` from env `cherenkov_CORS_ORIGINS`, default includes `:3000` and `:8000`.
- `Command` and `Tokamak` are imported at module level from `cherenkov.core.tokamak`.

### Frontend (React — `packages/cherenkov/web/`)
- `src/lib/api.ts` is the single source of truth: `API_BASE`, `getWsUrl()`, typed interfaces, fetch helpers.
- Vite proxy in dev: `/api → http://127.0.0.1:8000`, `/ws → ws://127.0.0.1:8000`, `/health → http://127.0.0.1:8000`. Both dev (port 3000) and prod (port 8000 StaticFiles) paths are confirmed working.
- `useLiveEvents.ts` — singleton WebSocket, 3s reconnect, module-level state (one WS per page load).
- Scan results flow: `TacticalOperationsPanel` → `submitScan()` → `cherenkov:scan_complete` CustomEvent → `ThreatIntelPanel`.
- `DISABLE_HMR=true` env var disables hot reload (used by Antigravity preview).

### Testing
- **Virtual Environments**: Use `.venv/Scripts/pytest.exe` (Windows) or `.venv/bin/pytest` (Linux/CI).
- **Integration tests** are gated by marker `integration` + `ai_generated` — correctly skipped when real API keys absent.
- **Known pre-existing failures**: `test_android_scanner`, `test_compliance_mapper`, `test_file_upload_scanner`, `test_hitl_api`, `test_path_traversal_scanner`, `test_xxe_scanner` — fail due to missing modules in `cherenkov.scanners`. Do not fix these without reading the scanner registry first.
- Test files live in `tests/` (not `packages/`, not root).

### Encoding / Windows
- Python CLI scripts: avoid Unicode chars (`──`) in print output — Windows CMD (cp1252) throws `UnicodeEncodeError`. Use ASCII equivalents.
- Git bash on Windows: use `git -C /path/to/repo` for absolute paths when CWD changes across tool calls.

### Agent Coordination
- **Antigravity (Google IDE)**: Runs Vite dev server on `:3000`. "Reactive state is disabled" = Google server-side flag, resolves itself — not locally fixable. Extension host crash was caused by `ms-python.vscode-python-envs` + `meta.pyrefly` — both renamed to `.disabled` in `C:/Users/moaid/.antigravity/extensions/`.
- **Claude GitHub Actions**: Triggered by `@claude` in issue/PR comments. Workflow: `.github/workflows/claude.yml`. Needs `ANTHROPIC_API_KEY` secret.
- **Continue.dev**: Local Qwen 3.5 via Ollama. Config: `.continue/agents/new-config.yaml`. MCP servers not yet wired.
- **Autonomous pipeline**: `.github/workflows/autonomous-dev.yml` — daily at 2AM UTC, runs `scripts/autonomous_roadmap_executor.py --batch-size 3`, PRs into `auto-dev/<run_number>`.
- **Branching rule**: NEVER commit directly to main. All changes via branch + PR. Branch format: `<type>/<issue-number>-<short-description>`.

### Sprint Boundaries
- Sprint 1 (BaseScanner) ✅ — `packages/cherenkov/core/base_scanner.py`
- Sprint 2 (Parallel + AIMD) ✅ — `circuit_breaker.py`, `ai_workflows_orchestrator.py`
- Sprint 3 (TOKAMAK + LATTICE + Health) ✅ — all three P0s shipped in PR #226
- Sprint 4 (HITL) ⏳ — `PendingApprovalsPanel` organism, badge count in `ForensicHeader`
- Sprint 5 (Compliance) ⏳ — not started

### TOKAMAK PoC Execution ✅ WIRED
- `packages/cherenkov/core/tokamak.py` — fully implemented.
- `Command(payload, scanner_name, timeout, profile)` — `profile` selects `TOKAMAKProfile.STANDARD / MOBILE / KALI`.
- `Tokamak.execute(command)` uses `_PROFILE_CONFIGS[command.profile]` for image and network_mode. Containers are labelled `cherenkov.tokamak=true`.
- SHA-256 trace and shred receipt on every execution. Shred receipt includes `attested_by`, `license_number`, `standard` fields for CBE submission.
- Endpoints: `POST /api/v1/sandbox/execute` (OPERATOR role), `GET /api/v1/sandbox/status`.
- 5 unit tests in `tests/unit/test_tokamak.py` — all pass.

### LATTICE Bridge ✅ WIRED
- `packages/cherenkov/ai/lattice.py` — three public functions:
  - `embed_and_store(result: ScanResult) -> int` — ABLATION-gated, embeds via `nomic-embed-text`, upserts to Qdrant `cherenkov_findings` collection.
  - `query_similar_targets(target: str, k: int) -> list[dict]` — queries Qdrant before each scan to seed TENSOR context.
  - `label_false_positive(finding_id: str) -> bool` — excludes vectors from future context.
- Hook in `packages/cherenkov/core/engine.py`: `_lattice_context()` called before `scan_all()`, `_lattice_store()` fire-and-forget after each scanner result.
- MEISSNER: all Qdrant/Ollama traffic on localhost only.
- ABLATION: every finding passes through `AblationBridge.sanitize()` before embedding.
- Embed model: `nomic-embed-text` (768-dim). Collection: `cherenkov_findings`. Qdrant at `localhost:6333`.
- 4 unit tests in `tests/unit/test_lattice.py` — all pass.

### Data Retention & Compliance
- **WORM**: `save_scan()` enforces no-overwrite. `audit_log` has `trace_hash` on every entry.
- **Pruning**: `prune_old_scans(days=90)` exists but is NOT called automatically — add a scheduled job if needed.
- **Right to erasure** (Law 151/2020): `erase_target_data(target)` in `database.py` nulls findings, purges audit entries, returns signed receipt. Exposed as `DELETE /api/v1/data/target` (ADMIN only).
- **Audit log** has no pruning function — grows indefinitely. Add `prune_audit_log()` if required by CBE.

### Known Issues / Gotchas
- `autonomous_generated/` contains many broken/duplicate files from early swarm generation — do not refactor without reading first.
- `src/cherenkov/` (old path) may still exist in some legacy scripts — do not use; canonical path is `packages/cherenkov/`.
- `pytest_output.txt` and `scan_report_*.json` are gitignored runtime files — do not commit.
- `qdrant/` at root is gitignored — Qdrant runtime state, never commit.
- Two docker-compose files exist: `docker-compose.yml` (root, primary) and `deploy/docker-compose.yml`. Qdrant is not in either — it runs as a standalone process.

### Import Rules
- The canonical package path is `packages/cherenkov/` not `src/`.
- All imports must be from `cherenkov.*` not `src.cherenkov.*` or `packages.cherenkov.*`.
- NEVER import from `autonomous_generated` in production code.

### Execution Context
- DVWA runs at `localhost:80`. Always available for scanner validation.
- Qdrant runs at `localhost:6333`. Always available for LATTICE operations.
- Ollama runs at `localhost:11434` with `llama3.2:3b` pulled. `nomic-embed-text` must be pulled for LATTICE.
- PYTHONPATH must include `packages/` directory.
- Use `docker exec -i` (not `-it`) for CI/CD commands.

### Agent Tasks Workflow
- Single task only: pick one open `status:in-progress` issue.
- Read `CLAUDE.md` first. Do not read other files unless necessary.
- Export `PYTHONPATH=$PYTHONPATH:$(pwd)/packages` before running any python command.
- Run `ruff format packages/` and `ruff check packages/ --ignore W,S,B` before committing Python.
- Run `tsc --noEmit` before committing TypeScript.
- Commit with conventional commit message. Never commit directly to main.
- Report: what changed, what tests passed, any blockers.
