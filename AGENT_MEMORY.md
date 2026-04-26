# Agent Session Memory

## Session 1 (2026-04-26, 4:11 PM EEST)

### Setup Complete ✅
- **Tools installed:** uv, Ollama (downloading models), Aider, pre-commit, pytest, ruff, bandit
- **AI Models:** llama3.2:3b-instruct-q4_K_M, qwen2.5-coder:7b-instruct-q4_K_M (downloading)
- **Repository:** Initialized at ~/daqiq-dev
- **Agent rules:** Configured (.clinerules)
- **Pre-commit hooks:** Ready to install

### System Constraints
- **Hardware:** Ryzen 9 8945HS, 12GB WSL2 limit
- **Budget:** $0 (Gemini/Groq free tier only)
- **Timeline:** 30 weeks (Phase 0-5)
- **API Limits:** Gemini 15 RPM free, Groq 30 RPM free

### Architectural Decisions
1. **Model Selection:**
   - Code generation: qwen2.5-coder:7b (better than llama3.2:3b)
   - Code review: Groq Llama 3.3 70B (faster than Gemini)
   - Local execution: llama3.2:3b (lightweight)

2. **Development Workflow:**
   - TDD mandatory (tests before implementation)
   - Pre-commit blocks commits if coverage <80%
   - Git branch per feature (no direct commits to main)
   - Builder (Gemini) → Reviewer (Groq) → Human (merge)

3. **Security Standards:**
   - Skip NPU acceleration (use CPU only for stability)
   - All secrets in .env (never hardcoded)
   - Fail-closed error handling
   - Pydantic validation on all inputs

### Next Session Goals
- [ ] Install Python dev tools (pytest, ruff, bandit, aider)
- [ ] Install pre-commit hooks
- [ ] Generate CloudInstruction Pydantic schema
- [ ] Generate SiyaadaSanitizer with HMAC
- [ ] Achieve >80% code coverage

### Agent-Specific Notes

#### Roo Code (Builder - Gemini 2.5 Flash)
- **Best prompts:** Detailed specs with exact field names, validators
- **Struggles with:** Vague requests like "improve this"
- **Strength:** File editing, running terminal commands, context awareness
- **Usage:** Primary code generator

#### Roo Code (Reviewer - Groq Llama 3.3 70B)  
- **Best prompts:** "Review branch X for security/edge cases"
- **Strength:** Spotting SQL injection, XSS, race conditions
- **Weakness:** Sometimes over-engineers
- **Usage:** Switch API provider to Groq for code review

### Current Blockers
- Ollama models still downloading (ETA: 5-10 min)

### Open Questions (Deferred)
- HMAC key rotation strategy → Phase 4
- Multi-APK batch processing → Phase 5
