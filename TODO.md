# CHERENKOV TODO — Phase 2 Active Sprint

## Sprint 2: Orchestration Hardening [DONE ✅]
- [x] `ScanEngine.scan_all()` — true asyncio gather across all registered scanners (#182)
- [x] Per-scanner timeout isolation (one scanner failure doesn't kill others) (#182)
- [x] Broadcast `scan_progress` WS events per scanner completion (#182)
- [x] Integration test: parallel scan finishes faster than sequential (#182)
- [x] Target-level circuit breaker (Meissner) integration (#182)

## Sprint 3: TOKAMAK Execution Sandbox [IN PROGRESS]
- [ ] Wire `core/tokamak.py` to `Dockerfile.tokamak` — pass sandbox a `Command` payload, return signed JSON receipt
- [ ] Implement cryptographic erasure ("shred receipt") after sandbox teardown per CLAUDE.md invariant
- [ ] Write `tests/unit/test_tokamak.py` — verify: payload reaches sandbox, output is SHA-256 signed, receipt is valid JSON
- [ ] Add `GET /api/v1/sandbox/status` FastAPI endpoint so dashboard can poll TOKAMAK state

## Sprint 4: HITL Workflows [DONE ✅]
- [x] `POST /api/v1/findings/{id}/approve` — pause workflow, require operator signature before HIGH/CRITICAL PoC execution
- [x] `GET /api/v1/findings/pending` — list findings awaiting approval
- [x] `POST /api/v1/findings/{id}/reject` — reject finding with operator audit
- [x] Store pending state in SQLite (WAL mode) so restarts don't lose pending approvals
- [x] Frontend: `PendingApprovalsPanel` organism — badge count in `ForensicHeader`, full list in sidebar

## Sprint 5: Compliance & Reporting [NOT STARTED]
- [ ] Build `packages/cherenkov/compliance/` mapper: CWE/CVE → SAMA CSF / EGY-FIN CSF / DORA / OWASP Top 10
- [ ] `GET /api/v1/reports/{scan_id}/sarif` — export scan as SARIF 2.1 JSON
- [ ] `GET /api/v1/reports/{scan_id}/pdf` — generate local PDF audit report (no cloud dependency)
- [ ] Map compliance framework to `NewScanForm.tsx` `compliance` dropdown options

## Backend Hardening [ONGOING]
- [ ] Move `_scan_history` from in-memory list to SQLite WAL vault (survives restart)
- [ ] `GET /api/v1/health` — wire `meissner.state` from real `CircuitBreakerRegistry` instead of hardcoded `"CLOSED"`
- [ ] `GET /api/v1/health` — wire `nodes` to actual Ollama process check (ping localhost:11434)
- [ ] Broadcast `circuit_breaker` WebSocket events from `Meissner._transition_to_open()`

## Scanner Graduation [ONGOING]
- [ ] Audit `autonomous_generated/scanners/` — identify the 5-10 best implementations
- [ ] Refactor them to inherit `BaseScanner`, add proper `scan()` async method
- [ ] Move graduated scanners to `packages/cherenkov/scanners/` with unit tests
- [ ] Register them in `ScannerRegistry` so they run on every `/api/v1/scan`

## Agentic Infrastructure [DONE ✅]
- [x] `AGENTS.md` — agent roles, branching rules, label taxonomy
- [x] `CODEOWNERS` — updated to `packages/cherenkov/*` layout
- [x] `claude.yml` — @claude GitHub Actions integration
- [x] `autonomous-dev.yml` — daily scanner generation pipeline
- [x] `.continue/agents/new-config.yaml` — Continue.dev Qwen 3.5 local agent

## Backlog
- [ ] Branch protection on `main` — require PR + CI pass (currently pushing direct to main)
- [ ] `agent_state/` cleanup — archive stale checkpoint files
- [ ] `autonomous_generated/` — remove broken/duplicate files (many are non-functional)
