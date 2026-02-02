# ForgeKit - Product Requirements Document

**Product**: ForgeKit - AI Engineering Skills Toolkit
**Company**: FluxForge AI
**Author**: Johan Genis
**Version**: 0.1.0
**Created**: 2026-01-26
**Last Updated**: 2026-01-26

---

## 1. Product Vision

ForgeKit is an AI engineering skills toolkit that gives AI coding assistants (Claude Code, Cursor, Cline, GitHub Copilot) domain-specific capabilities for incident response, systems analysis, and architectural design. It transforms generic AI assistants into specialized engineering partners.

### One-Line Description

ForgeKit is a closed-source, cross-platform AI engineering skills toolkit that provides domain-specific incident response, systems analysis, and architectural design capabilities to AI coding assistants via MCP server distribution.

---

## 2. Problem Statement

### The Gap

AI coding assistants are powerful but generic. They lack:
- **Structured incident response** methodology (document, investigate, diagnose, fix)
- **Systems analysis** frameworks (health checks, risk assessment, pattern detection)
- **Architectural design** workflows (trade-off analysis, impact assessment, migration planning)
- **Session continuity** across conversations (handoff documents, context preservation)
- **Institutional memory** across sessions (shared artifacts, RCA history)

### The Cost

Without these capabilities, engineering teams:
- Reinvent investigation approaches for every incident
- Lose context between AI sessions (repeat discoveries)
- Make architectural decisions without structured analysis
- Cannot leverage past incidents/RCAs for future debugging
- Get inconsistent quality from AI assistants across team members

### The Opportunity

The autonomous AI agent market is projected to reach $8.5B by 2026 (Deloitte). MCP (Model Context Protocol) is becoming the industry standard for extending AI tools, with marketplace infrastructure already operational (MCPize, Cline, Apify). No existing product offers an integrated SRE/DevOps skill suite via MCP.

---

## 3. Target Users

### Primary: Senior/Staff Engineers

- Run production systems
- Handle incidents and on-call
- Make architectural decisions
- Use AI coding assistants daily
- Value structured methodology over ad-hoc prompting

### Secondary: Engineering Teams

- Need consistent incident response across team members
- Want to accumulate institutional knowledge (RCAs, design decisions)
- Standardize how the team uses AI for engineering tasks

### Tertiary: DevOps/SRE Teams

- Manage monitoring and alerting
- Perform root cause analysis
- Design resilient systems

---

## 4. Product Requirements

### 4.1 Skills (Core Product)

#### 4.1.1 Tactical Layer (Incident Response Pipeline)

| ID | Skill | Requirement | Priority |
|----|-------|-------------|----------|
| SK-001 | `/incident` | Document incidents with structured template (timeline, impact, affected systems) | P0 |
| SK-002 | `/investigate` | Deep investigation with 5-Whys, evidence gathering, hypothesis testing | P0 |
| SK-003 | `/rca-bugfix` | Root cause analysis producing RCA report + executable fix prompt | P0 |
| SK-004 | `/watchdog` | Autonomous background log monitoring with error pattern detection and Telegram alerts | P1 |

#### 4.1.2 Strategic Layer (Analysis & Design)

| ID | Skill | Requirement | Priority |
|----|-------|-------------|----------|
| SK-005 | `/analyze health` | System health assessment with component scoring | P0 |
| SK-006 | `/analyze risk` | Risk assessment with scoring matrix | P0 |
| SK-007 | `/analyze patterns` | Pattern detection across incidents, code, and logs | P1 |
| SK-008 | `/analyze component` | Deep dive into a single component | P1 |
| SK-009 | `/analyze architecture` | Full architecture review | P1 |
| SK-010 | `/design tradeoff` | Compare approaches with weighted scoring against user priorities | P0 |
| SK-011 | `/design validate` | Review proposed designs for completeness, feasibility, risk | P1 |
| SK-012 | `/design migrate` | Plan migration between approaches with rollback strategy | P2 |
| SK-013 | `/design impact` | Assess blast radius of a proposed change | P1 |
| SK-014 | `/design pattern` | Explain and assess applicability of a design pattern | P2 |
| SK-015 | `/research` | Topic research with documented findings and sources | P0 |
| SK-019 | `/blueprint` | Transform design/research output into implementation spec + prompt for `/plan` | P0 |
| SK-020 | `/finding` | Log proactive discoveries with type classification (Defect/Vulnerability/Debt/Gap/Drift) and severity assessment. Entry point for audit pipeline. | P0 |

#### 4.1.3 Session Management

| ID | Skill | Requirement | Priority |
|----|-------|-------------|----------|
| SK-016 | `/session-start` | Initialize session with project context, handoff reading, greeting | P0 |
| SK-017 | `/session-end` | Create handoff document + session summary, archive old handoffs | P0 |
| SK-018 | `/verify-session` | Verify handoff files are correctly configured | P1 |

### 4.2 Cross-Skill Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| INT-001 | Skills suggest next skill at completion (structured handoff) | P0 |
| INT-002 | Skills read shared artifacts from previous skill invocations | P0 |
| INT-003 | Design escalation: `/analyze` findings trigger `/design` suggestion | P1 |
| INT-004 | Watchdog-to-incident bridge: `/incident` can parse watchdog JSON | P2 |
| INT-005 | Research integration: `/investigate` and `/rca-bugfix` check `docs/research/` | P2 |
| INT-006 | Fix escalation: `/analyze` findings trigger `/finding` suggestion for corrective action | P1 |
| INT-007 | Finding artifacts (`docs/findings/`) read by `/investigate`, `/analyze`, `/rca-bugfix`, `/research` | P1 |

### 4.3 Distribution

| ID | Requirement | Priority |
|----|-------------|----------|
| DST-001 | CLI tool for local development (`forgekit init/update/status/diff/commit/push/uninstall`) | P0 (DONE) |
| DST-002 | Symlink-based installation into any project's `.claude/` directory | P0 (DONE) |
| DST-003 | MCP server serving skills as Prompts, Tools, and Resources | P0 (Phase 2) |
| DST-004 | API key authentication with tier-based access control | P0 (Phase 2) |
| DST-005 | Platform adaptation layer (Claude Code / Cursor / Copilot tool name mapping) | P1 (Phase 2) |
| DST-006 | Usage metering (per-invocation, per-user) | P1 (Phase 2) |
| DST-007 | Marketplace listing (MCPize, Cline) | P1 (Phase 3) |
| DST-008 | AGENTS.md export for non-MCP tools | P2 (Phase 4) |

### 4.4 Monetization

| ID | Requirement | Priority |
|----|-------------|----------|
| MON-001 | Free tier with basic skills (incident, research) | P1 (Phase 3) |
| MON-002 | Pro tier with all skills + modes ($19-29/mo) | P1 (Phase 3) |
| MON-003 | Enterprise tier with custom skills + team features ($99-199/seat/mo) | P2 (Phase 4) |
| MON-004 | Billing integration (Stripe / Paddle) | P1 (Phase 3) |
| MON-005 | Usage analytics dashboard | P2 (Phase 4) |

---

## 5. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-001 | MCP server response time | < 500ms per prompt request |
| NFR-002 | MCP server uptime | 99.9% |
| NFR-003 | Skill content never written to user's filesystem (MCP mode) | Always |
| NFR-004 | API key validation on every request | Always |
| NFR-005 | Support Python 3.10+ for CLI | Always |
| NFR-006 | Zero external dependencies for CLI (stdlib only) | Always |
| NFR-007 | Skills work without internet (local symlink mode) | Always |

---

## 6. Success Metrics

### Phase 1 (Development)
- [x] All 8 skills portable across projects via symlinks
- [x] CLI tool functional (7 commands)
- [x] Zero project-specific references in skills

### Phase 2 (MVP)
- [ ] MCP server serving all skills
- [ ] Verified working with 3+ AI tools (Claude Code, Cursor, Cline)
- [ ] 5+ private beta users

### Phase 3 (Monetization)
- [ ] Listed on 2+ marketplaces
- [ ] 50+ paying users within 3 months of launch
- [ ] Net Promoter Score > 40

### Phase 4 (Expansion)
- [ ] 500+ active users
- [ ] 3+ enterprise customers
- [ ] 15+ skills in the library

---

## 7. Competitive Analysis

| Competitor | What They Offer | ForgeKit Advantage |
|-----------|----------------|-------------------|
| awesome-claude-skills (GitHub) | Community-curated skill collection | Integrated pipeline, not isolated skills |
| ClaudeMDEditor | Config editor for multiple AI tools | We provide the skills, not just the editor |
| Generic prompts/templates | One-shot prompt templates | Interactive checkpoints, shared artifacts, institutional memory |
| Custom GPTs (OpenAI) | Pre-configured ChatGPT personas | Works in coding environment, not browser chat |
| Cursor Rules marketplace | Cursor-specific rules | Cross-platform via MCP, deeper methodology |

### Key Differentiators

1. **Triple pipelines**: Reactive (watchdog -> incident -> investigate -> rca-bugfix -> plan), Proactive (research -> design -> blueprint -> plan), and Audit (analyze -> finding -> investigate/design -> rca-bugfix/blueprint -> plan) converge at `/plan`
2. **Interactive methodology**: Checkpoints adapt to user context (not one-shot templates)
3. **Design escalation**: Analysis findings automatically suggest architectural exploration
4. **Institutional memory**: Shared artifacts accumulate knowledge across sessions
5. **Cross-platform**: MCP distribution works with any compatible AI tool
6. **Closed-source**: Methodology protected via server-side delivery

---

## 8. Out of Scope (v1)

- Web UI / dashboard (CLI + MCP only)
- Team collaboration features (single-user first)
- Custom skill authoring (ForgeKit-authored only)
- IDE extension (rely on MCP integration)
- Mobile support

---

## 9. Dependencies

| Dependency | Type | Risk |
|-----------|------|------|
| MCP Protocol stability | External | Low (Linux Foundation backed) |
| Claude Code skill system | External | Low (Anthropic primary platform) |
| Cursor MCP support | External | Low (already supported) |
| Hosting platform (Fly.io/Railway) | External | Low (commodity) |
| Billing provider (Stripe/Paddle) | External | Low (commodity) |

---

## 10. Legal Considerations

- **IP Protection**: Skills qualify as trade secrets (kept confidential via MCP server)
- **Copyright**: Human-authored skill instructions are copyrightable
- **Terms of Service**: Required for marketplace listing and user agreements
- **Privacy Policy**: Required if collecting user data (API keys, usage analytics)
- **EU AI Act**: Monitor for applicability (likely not high-risk, but assess)
- **POPIA (South Africa)**: Applicable if serving South African users

---

**Document Status**: Living document. Update as product evolves.
