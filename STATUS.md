# CHERENKOV Project Status

## Build Health
| Check | Status |
|---|---|
| Tests | ✅ 68 passed, 7 skipped (integration correctly gated) |
| Ruff lint | ✅ Passing |
| Ruff format | ✅ Passing |
| TypeScript (web) | ✅ Zero errors |
| Vite build | ✅ Clean (414 kB JS, 54 kB CSS) |

## Current Phase: Phase 2 — Swarm Optimization & Parallelism
**Target:** v1.1.0 | **Timeline:** Q2 2026

### Sprint Progress
| Sprint | Goal | Status |
|---|---|---|
| Sprint 1 — BaseScanner | Uniform scanner interface | ✅ Done — `packages/cherenkov/core/base_scanner.py` |
| Sprint 2 — Parallel Orchestration | asyncio + AIMD circuit breakers | ✅ Done — `circuit_breaker.py`, `ai_workflows_orchestrator.py` |
| Sprint 3 — TOKAMAK Sandbox | Docker isolation + PoC execution | ✅ Done — Command pattern, SHA-256 signing, shred receipt |
| Sprint 4 — HITL Workflows | API pause gate + UI approval flow | ✅ Done — approve/reject endpoints, pending findings, audit vault |
| Sprint 5 — Compliance & Reporting | SAMA/EGY-FIN mapping + PDF/SARIF | ✅ Done — 19 CWE mapper, map_all()/coverage(), SARIF + PDF export |

## Active Work
- **Frontend dashboard** (`packages/cherenkov/web/`) — React 19 / Vite / Tailwind v4, live scan results, WebSocket events ✅
- **FastAPI backend** (`packages/cherenkov/api/main.py`) — `/api/v1/*` routes, `/ws/live` WebSocket, scan history ✅
- **Compliance module** (`packages/cherenkov/compliance/`) — 19 CWE → OWASP/SAMA/EGY-FIN/DORA, SARIF + PDF export ✅
- **HITL workflows** — approve/reject endpoints, pending findings, audit vault ✅
- **TOKAMAK sandbox** — Docker execution, Command pattern, SHA-256 signing, shred receipt ✅
- **Scanner graduation** — promoting autonomous_generated scanners into production under BaseScanner

## Agent Coordination
| Agent | Domain | Channel |
|---|---|---|
| Google Antigravity | Frontend React/Vite | localhost:3000 preview |
| Claude (GitHub Actions) | Code review, issue work | `@claude` in issues/PRs |
| Continue.dev (Qwen 3.5) | Local autonomous coding | `.continue/agents/` |
| Autonomous Pipeline | Scanner generation | `scripts/autonomous_roadmap_executor.py` daily |
| Claude Code (local) | Architecture, agentic coordination | This terminal |

## Module Ownership
See `.github/CODEOWNERS` for full ownership map.
