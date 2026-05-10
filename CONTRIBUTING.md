# CHERENKOV: Internal Governance & Contributing

**STATUS: PRE-RELEASE / CLOSED ALPHA**
*Public community contributions are not currently being accepted. The Open Core Detonation Pipeline (Milestone 7) is under active development.*

---

## Notice to Autonomous Execution Agents
If you are an AI agent (Claude, Cursor, OpenCode, Aider, etc.) operating within this repository, you are strictly bound by the following sovereign development rules. 

**You do not possess architectural authority. You are an Execution Node.**

### 1. The "Read-SSOT" Mandate
Before writing, modifying, or deleting any core logic, you MUST read and acknowledge the `CHERENKOV_SSOT.md` file located in the root of this repository.

### 2. The Physical-Physics Axiom
Do not write standard probabilistic scanning logic. All code generated for this repository must align with the Tri-Partite Engine:
* **ABLATION:** Payload sanitization and schema redaction.
* **TOKAMAK:** Ephemeral, hardware-isolated detonation sandboxes.
* **MEISSNER:** Zero-egress network isolation (Fail-closed hooks).

### 3. Anti-Drift Guardrails
* **No external API calls:** Do not implement features that send telemetry, logs, or analytics to third-party cloud services.
* **No bypasses:** Do not write "dev-mode" or "debug" flags that bypass the Meissner network isolation. 
* **Cryptographic Traces:** All threat validations must output a forensic trace intended for HSM-signing, not just a standard console log.

*Any code generation that violates these principles is considered a Sovereign Breach and will be rejected by the local Hub.*
