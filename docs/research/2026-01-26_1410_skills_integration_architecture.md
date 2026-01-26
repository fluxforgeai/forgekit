# Research: Skills Integration Architecture

**Date**: 2026-01-26
**Researcher**: Claude Code (Sessions 81-82)
**Status**: Complete

---

## Question

How should the 7 Claude Code skills in this project be integrated into a cohesive, orchestrated system? What patterns exist for skill chaining, cross-skill handoffs, and autonomous workflows?

---

## TL;DR

The project has 7 skills forming two distinct layers: a **tactical incident response pipeline** (incident, investigate, rca-bugfix, watchdog) and a **strategic analysis layer** (analyze, design, research). Cross-skill connections already exist via manual handoff suggestions (e.g., analyze escalates to design). The recommended integration architecture is a **Sequential Pipeline with Handoff Points** pattern, leveraging Claude Code's native `context: fork` frontmatter for isolation and the Skill tool for invocation. Full autonomous chaining is not yet supported by Claude Code's skill system -- skills must be user-invoked -- so the integration focuses on structured handoff protocols and shared artifacts.

---

## Skills Inventory

### The 7 Skills

| # | Skill | Trigger | Purpose | Layer |
|---|-------|---------|---------|-------|
| 1 | **incident** | `/incident {desc}` | Document WHAT happened (factual record) | Tactical |
| 2 | **investigate** | `/investigate {report}` | Analyze WHY it happened (deep investigation) | Tactical |
| 3 | **rca-bugfix** | `/rca-bugfix {issue}` | Root cause analysis + fix prompt generation | Tactical |
| 4 | **watchdog** | `/watchdog {desc}` | Autonomous bash-based passive log monitoring | Tactical |
| 5 | **analyze** | `/analyze {mode} [scope]` | Strategic system analysis (health, patterns, risk, component, architecture) | Strategic |
| 6 | **design** | `/design {mode} {topic}` | Research-driven architectural design analysis | Strategic |
| 7 | **research** | `/research {question}` | Topic research with documented findings | Strategic |

### Skill Characteristics

| Skill | Interactive | Autonomous | Produces Artifact | Suggests Next Skill |
|-------|------------|------------|-------------------|---------------------|
| incident | No | No | `docs/incidents/*.md` | investigate, rca-bugfix |
| investigate | No | No | `docs/investigations/*.md` | rca-bugfix, plan |
| rca-bugfix | Yes (context check) | No | `docs/RCAs/*.md` + `docs/prompts/*.md` | plan |
| watchdog | No | **Yes** (bash script) | `/tmp/watchdog_*` + incident JSONs | incident |
| analyze | **Yes** (checkpoints) | No | `docs/analysis/*.md` + `system-map.md` | investigate, rca-bugfix, design, plan |
| design | **Yes** (9 checkpoints) | No | `docs/design/*.md` | plan (EnterPlanMode) |
| research | No | No | `docs/research/*.md` | investigate, plan |

---

## Current Cross-Skill Connections

### Existing Handoff Protocols

The skills already have documented handoff suggestions, though all require manual user invocation:

```
                    ┌─────────────────────┐
                    │  /analyze           │  Strategic Layer
                    │  Systems Analyst    │
                    └─────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  /watchdog  │  │  /research  │  │  /design    │   Operational
    │  Monitor    │  │  Explore    │  │  Architect  │
    └─────────────┘  └─────────────┘  └─────────────┘
              │                               │
              ▼                               ▼
    ┌─────────────┐                  ┌─────────────┐
    │  /incident  │                  │  /plan      │   Tactical
    │  Document   │                  │  Execute    │
    └─────────────┘                  └─────────────┘
              │
              ▼
    ┌─────────────────┐
    │  /investigate    │
    │  Deep Analyze    │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │  /rca-bugfix     │
    │  Diagnose & Fix  │
    └─────────────────┘
```

### Documented Handoff Points

| From | To | Trigger | Documented In |
|------|----|---------|---------------|
| watchdog | incident | Error detected in logs | watchdog/SKILL.md |
| incident | investigate | User wants to understand cause | incident/SKILL.md |
| incident | rca-bugfix | User wants direct fix | incident/SKILL.md |
| investigate | rca-bugfix | Investigation complete | investigate/SKILL.md |
| rca-bugfix | plan | Fix prompt ready | rca-bugfix/SKILL.md |
| analyze | investigate | Pattern found needing investigation | analyze/SKILL.md |
| analyze | rca-bugfix | Root cause identified | analyze/SKILL.md |
| analyze | design | **Design escalation** triggered | DESIGN_ESCALATION.md |
| analyze | plan | Implementation needed | analyze/SKILL.md |
| design | plan | Design approved, ready to implement | design/SKILL.md |

### Design Escalation (Key Innovation)

The analyze skill includes a design escalation mechanism documented in `DESIGN_ESCALATION.md`. When analysis findings suggest architectural redesign rather than point fixes, the skill offers:

1. **Inline exploration** -- quick trade-off table within the analysis
2. **Deep dive** -- suggests running `/design tradeoff {topic}`
3. **Note it** -- records finding without exploring alternatives
4. **Accepted limitation** -- marks as known and accepted

**Escalation triggers:**
- Same logic duplicated in 3+ files
- Technology choice conflicts with requirements
- Approach won't scale to 10x
- Same component in 3+ incidents
- High coupling hotspot

---

## Claude Code Skills Architecture

### How Skills Work (Official Documentation)

**Progressive Disclosure**: At startup, Claude Code pre-loads only the `name` and `description` from every installed skill into its system prompt. The full SKILL.md content is loaded only when the skill is invoked.

**Frontmatter Configuration**: Skills use YAML frontmatter between `---` markers:

```yaml
---
name: "My Skill"
description: "When to use this skill"
context: fork          # Run in isolated context (subagent)
agent: Explore         # Specify agent type
allowed-tools:         # Restrict available tools
  - Read
  - Grep
  - Glob
---
```

**Key Frontmatter Fields**:
- `description` -- Tells Claude when the skill is relevant (recommended for all skills)
- `context: fork` -- Runs skill in an isolated subagent context, keeping main conversation clean
- `agent: Explore` -- Specifies which agent type to use for forked execution
- `allowed-tools` -- Restricts which tools the skill can use
- `disable-model-invocation` -- Prevents model from using the skill autonomously

**Supporting Files**: Skills can bundle additional files in their directory. Claude discovers and reads them only as needed, enabling complex skills without bloating the initial context.

### Known Limitation: `context: fork` via Skill Tool

There is a known issue (GitHub #17283) where `context: fork` and `agent:` frontmatter fields are ignored when a skill is invoked via the Skill tool. The skill runs in the main conversation context instead of spawning the specified subagent. This affects skills that perform extensive exploration (like analyze) which would benefit from running in an isolated Explore agent.

### Skills vs Subagents vs MCP

| Primitive | Purpose | Invocation | Context |
|-----------|---------|------------|---------|
| **Skills** | Procedural knowledge ("how to do X") | User-invoked via `/skill` | Main or forked |
| **Subagents** | Delegation & isolation | System-spawned via Task tool | Always isolated |
| **MCP Servers** | External connectivity | Tool calls | Main context |
| **Projects** | Persistent context | Auto-loaded | Main context |

---

## Agent Orchestration Patterns (2026 Landscape)

### Pattern 1: Sequential Pipeline (Assembly Line)

```
Agent A → Agent B → Agent C → Result
```

Each agent processes output from the previous one. Linear, deterministic, easy to debug. Best for workflows with clear dependencies.

**Applicability to our skills**: The incident response pipeline (`watchdog → incident → investigate → rca-bugfix → plan`) is a natural sequential pipeline.

### Pattern 2: Coordinator-Worker (Hub-and-Spoke)

A central coordinator receives tasks, breaks them into subtasks, delegates to specialist workers, and aggregates results.

**Applicability**: The `analyze` skill acts as a coordinator that can delegate to `investigate`, `rca-bugfix`, `design`, or `plan` based on findings.

### Pattern 3: Handoff Orchestration

Agents dynamically delegate to one another without a central manager. Each agent assesses the task and decides to handle it or transfer it to another with more expertise.

**Applicability**: This is the pattern our skills currently use -- each skill suggests the next skill at completion. The handoff is user-mediated (user decides which skill to invoke next).

### Pattern 4: Hierarchical / Nested Teams

Supervisors manage groups of specialists. Enables complex organizational structures with delegation chains.

**Applicability**: The two-layer structure (strategic analyze/design layer supervising tactical incident/investigate layer) is a simplified hierarchy.

### Pattern 5: Agent-as-Tool

A sub-agent's entire workflow is wrapped as a single function call for a parent agent.

**Applicability**: Claude Code's Task tool already enables this -- an agent can spawn subagents. However, skills cannot currently spawn other skills programmatically.

### Pattern 6: Shared Artifacts

Agents communicate through persistent artifacts rather than direct message passing. Each agent reads from and writes to shared documents.

**Applicability**: Our skills already use this pattern extensively:
- `system-map.md` is the shared artifact for analyze modes
- `docs/RCAs/*.md` are read by investigate, rca-bugfix, and analyze
- `docs/prompts/*.md` bridge rca-bugfix to plan mode

---

## Recommended Integration Architecture

### Architecture: Structured Handoff Pipeline with Shared Artifacts

Given Claude Code's current limitations (skills cannot invoke other skills programmatically, `context: fork` has known issues), the recommended architecture combines:

1. **Sequential Pipeline** for the incident response flow
2. **Coordinator-Worker** for the analyze/design strategic layer
3. **Shared Artifacts** for cross-skill communication

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SHARED ARTIFACTS LAYER                         │
│                                                                       │
│  system-map.md    docs/RCAs/    docs/incidents/    docs/prompts/     │
│  docs/analysis/   docs/design/  docs/research/     docs/plans/       │
│                                                                       │
│  All skills READ from and WRITE to these shared artifacts.            │
│  Artifacts persist across sessions = institutional memory.            │
└──────────────────────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │                    │                    │
┌────────┴────────┐  ┌───────┴────────┐  ┌───────┴────────┐
│ STRATEGIC LAYER │  │ TACTICAL LAYER │  │ AUTONOMOUS     │
│                 │  │                │  │                │
│ /analyze ──────►│  │ /incident     │  │ /watchdog      │
│    │            │  │    │           │  │ (bash script)  │
│    ├─► /design  │  │    ▼           │  │    │           │
│    │            │  │ /investigate   │  │    ▼           │
│    └─► /research│  │    │           │  │ Telegram alert │
│                 │  │    ▼           │  │ + incident JSON│
│ User decides    │  │ /rca-bugfix   │  │                │
│ next action     │  │    │           │  │ Runs without   │
│ at checkpoints  │  │    ▼           │  │ Claude session │
│                 │  │ /plan          │  │                │
└─────────────────┘  └────────────────┘  └────────────────┘
```

### Integration Principles

1. **User-Mediated Handoffs**: Every skill stops and suggests next steps. The user decides which skill to invoke next. This aligns with the 2026 "human-on-the-loop" pattern.

2. **Shared Artifact Communication**: Skills don't pass data directly to each other. Instead, they write to shared docs (`docs/RCAs/`, `docs/analysis/`, etc.) and subsequent skills read those artifacts for context.

3. **Mandatory History Review**: The investigate and rca-bugfix skills already require reading past RCAs, investigations, and research before making recommendations. This ensures institutional memory.

4. **Design Escalation Bridge**: The analyze → design handoff via DESIGN_ESCALATION.md is the only cross-layer bridge. It enables strategic findings to flow to design decisions.

5. **Watchdog Autonomy**: The watchdog skill is uniquely autonomous (runs as bash script without Claude). It bridges to the tactical pipeline by creating incident JSON files and sending Telegram alerts, which the user then feeds into `/incident`.

### Standardized Handoff Protocol

Every skill should end with a consistent handoff format:

```
{Skill} complete.

Report saved to: {path}

Summary: {1-2 sentences}

Recommended next steps:
- /skill1 {description of when to use}
- /skill2 {description of when to use}
- Ask me to continue with {alternative action}

Awaiting your instructions.
```

This pattern is already implemented in most skills but should be standardized across all 7.

---

## Integration Gaps and Recommendations

### Gap 1: No Automated Skill Chaining

**Current**: Each skill must be manually invoked by the user.
**Impact**: Multi-step workflows require the user to remember and invoke each skill in sequence.
**Recommendation**: Accept this limitation for now. Claude Code does not support programmatic skill-to-skill invocation. The structured handoff suggestions are the best available pattern. Monitor GitHub for updates to the Skill tool that might enable chaining.

### Gap 2: No Shared Context Between Skills

**Current**: Each skill invocation starts fresh (unless in the same conversation).
**Impact**: When `/investigate` runs after `/incident`, it must re-read the incident report from disk rather than receiving it directly.
**Recommendation**: The shared artifacts pattern handles this well. Ensure all skills write to consistent paths and read from them. The `system-map.md` artifact for analyze is a good model to follow.

### Gap 3: Watchdog-to-Incident Gap

**Current**: Watchdog creates JSON incident files in `/tmp/`, but `/incident` expects a natural language description.
**Impact**: User must manually read watchdog incident files and translate them for `/incident`.
**Recommendation**: Add a helper command or section in the incident skill that can accept a watchdog incident JSON path as input and auto-parse it.

### Gap 4: Research Skill Underutilized

**Current**: The `/research` skill is standalone with no explicit integration into other skill workflows.
**Impact**: Investigate and rca-bugfix do their own research inline rather than building on accumulated research artifacts.
**Recommendation**: Add `/research` as a suggested pre-step in investigate and rca-bugfix workflows. Add a "Check existing research" step that reads `docs/research/*.md` before performing new research.

### Gap 5: Context Budget Awareness

**Current**: Only rca-bugfix checks context usage (asks user to run `/context`).
**Impact**: Other skills (especially analyze and design with many checkpoints) can exhaust context mid-execution.
**Recommendation**: Add context-awareness to analyze and design skills. At minimum, suggest `/context` check before starting and at midpoint of long analyses.

---

## Implementation Roadmap

### Phase 1: Standardize Handoff Protocol (Low Effort)
- Ensure all 7 skills use the standard handoff format
- Verify all skills suggest appropriate next skills
- Add `context: fork` frontmatter where appropriate (future-proofing for when GitHub #17283 is resolved)

### Phase 2: Add Shared Artifact References (Low Effort)
- Add "Check existing artifacts" step to investigate, rca-bugfix, and research skills
- Document the shared artifact paths in each SKILL.md
- Ensure system-map.md refresh strategy is implemented in analyze

### Phase 3: Watchdog-Incident Bridge (Medium Effort)
- Add incident JSON parsing capability to the incident skill
- Allow `/incident /tmp/watchdog_{id}_incidents/fix-related_*.json` as input
- Auto-extract timeline, error type, and stack trace from JSON

### Phase 4: Context-Aware Execution (Medium Effort)
- Add context checks to analyze and design skills
- Implement graceful degradation: if context is high, produce abbreviated report
- Add `--quick` flag to all skills for reduced-context execution

### Phase 5: Move to fluxforgeai Repo (Separate Track)
- Extract generic skill framework (frontmatter patterns, handoff protocol, artifact sharing)
- Make skills project-agnostic (remove Kuda-specific references)
- Publish as reusable skill templates

---

## 2026 Industry Context

### AI Agent Orchestration Market

The autonomous AI agent market is projected to reach **US$8.5 billion by 2026** and **US$35 billion by 2030** (Deloitte). Better orchestration could increase these projections by 15-30%.

### Key Trends Relevant to This Architecture

1. **Shift from Task Automation to Workflow Ownership**: AI agents in 2026 take ownership of entire workflows -- planning, calling tools, managing dependencies, and adapting when things break. Our skill system moves in this direction with the sequential pipeline pattern.

2. **Human-on-the-Loop**: The most advanced businesses in 2026 are shifting from human-in-the-loop to human-on-the-loop orchestration. Our architecture aligns -- the user supervises and makes decisions at checkpoints rather than micromanaging each step.

3. **Domain-Specific Over General-Purpose**: Enterprises favor domain-specific agents over general-purpose ones. Our skills are domain-specific (incident response, system analysis, design) rather than generic.

4. **Shared Artifacts as Communication**: The pattern of agents communicating through persistent artifacts (rather than direct message passing) is emerging as a best practice for multi-agent systems.

### Claude Code Skills Ecosystem (2026)

- **Official skills documentation**: Skills are the recommended way to extend Claude Code with procedural knowledge
- **Progressive disclosure**: Name + description loaded at startup; full content loaded on invocation
- **Supporting files**: Skills can bundle additional files discovered on demand
- **Frontmatter configuration**: YAML-based behavior configuration (context, agent type, tool restrictions)
- **Known limitation**: `context: fork` not yet honored via Skill tool invocation (GitHub #17283)
- **Community growing**: curated skill repositories emerging (e.g., awesome-claude-skills on GitHub)

---

## Sources

### Official Documentation
1. [Claude Code - Extend Claude with Skills](https://code.claude.com/docs/en/skills)
2. [Anthropic - Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
3. [Claude Agent Skills Deep Dive - Lee Han Chung](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

### Agent Orchestration Patterns
4. [Microsoft Azure - AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
5. [Google Developers - Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
6. [Deloitte - Unlocking Exponential Value with AI Agent Orchestration](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-agent-orchestration.html)
7. [Digital Applied - AI Agent Orchestration Workflows Guide](https://www.digitalapplied.com/blog/ai-agent-orchestration-workflows-guide)

### 2026 Trends
8. [Analytics Vidhya - 15 AI Agents Trends 2026](https://www.analyticsvidhya.com/blog/2026/01/ai-agents-trends/)
9. [Kellton - Generative AI 2.0: Agentic Systems Redefine Workflows 2026](https://www.kellton.com/kellton-tech-blog/generative-ai-2-0-agentic-workflows-2026)
10. [AIM Research - Top 10+ Agentic Orchestration Frameworks 2026](https://research.aimultiple.com/agentic-orchestration/)

### Known Issues
11. [GitHub #17283 - Skill tool should honor context: fork and agent: frontmatter](https://github.com/anthropics/claude-code/issues/17283)

### Internal Project Documents
12. `.claude/skills/analyze/DESIGN_ESCALATION.md` -- Cross-skill escalation design
13. `.claude/skills/analyze/DESIGN_SKILL_SPEC.md` -- Design skill full specification
14. `docs/research/2026-01-23_0615_systems_analyst_skill_design.md` -- Systems analyst research (1,600 lines)

---

## Related Documents

- `docs/research/2026-01-23_0615_systems_analyst_skill_design.md` -- Foundational research for analyze skill
- `.claude/skills/analyze/DESIGN_ESCALATION.md` -- Cross-skill bridge specification
- `.claude/skills/analyze/DESIGN_SKILL_SPEC.md` -- Design skill detailed spec

---

**Research Complete**: 2026-01-26 14:30 UTC
