# Research: ForgeKit Monetization, Distribution & Cross-Platform Strategy

**Date**: 2026-01-26 15:49 UTC
**Researcher**: Claude Code (Session 82)
**Status**: Complete
**Related**: `docs/research/2026-01-26_1410_skills_integration_architecture.md`

---

## Question

How should ForgeKit (fluxforgeai/forgekit) be architected for closed-source monetization? Will the skills work with OpenAI and Gemini models? What is the optimal distribution mechanism?

---

## TL;DR

**Cross-platform**: ForgeKit's skills do NOT work natively with OpenAI/Gemini/Cursor/Copilot -- they use Claude Code-specific tool names and concepts. However, the *methodology* (incident response, systems analysis, design trade-offs) is entirely platform-agnostic.

**Distribution**: The Model Context Protocol (MCP) solves both the cross-platform AND closed-source challenges simultaneously. Skills served as MCP prompts/tools work with any MCP-compatible client (Claude Code, Cursor, Cline, VS Code Copilot, and growing). The prompts never exist as files on the user's machine.

**Monetization**: MCP marketplace infrastructure already exists (MCPize: 70% revenue share, Apify: 36K+ monthly developers, Moesif: metering/billing). Usage-based pricing (per-invocation, subscription tiers) is the natural model.

**IP Protection**: Prompts are protectable as trade secrets under both U.S. and international law when kept confidential and commercially valuable. MCP server distribution maintains confidentiality -- the strongest protection available for prompt-based IP.

**Recommendation**: Build the ForgeKit private repo with markdown skills NOW (Phase 1: development). When ready to monetize, wrap skills in an MCP server (Phase 2: MVP). The markdown files become source code that feeds the server -- they're never distributed directly to users.

---

## 1. Cross-Platform Compatibility Analysis

### 1.1 The Fragmentation Problem

Every AI coding tool has its own configuration format. There is **no native cross-compatibility**:

| AI Tool | Config Location | Format | Skill System |
|---------|----------------|--------|-------------|
| **Claude Code** | `.claude/skills/*/SKILL.md` | YAML frontmatter + markdown | Full skill system (progressive disclosure, frontmatter, supporting files) |
| **Cursor** | `.cursor/rules/*.mdc` | Markdown with frontmatter | Rules system (cursor-specific) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Plain markdown | Single instructions file per repo/org |
| **Windsurf** | `.windsurfrules` | Plain markdown | Rules file |
| **Gemini CLI** | `.gemini/` | Markdown | Custom instructions |
| **Cline** | MCP servers + custom instructions | MCP protocol + markdown | MCP-native |
| **VS Code (Copilot)** | MCP server config | MCP protocol | MCP support added 2025/2026 |

### 1.2 ForgeKit's Claude Code Dependencies

Our 7 skills use Claude Code-specific primitives that do NOT exist in other tools:

**Tool Names** (Claude Code-specific):
- `Read`, `Write`, `Edit`, `Grep`, `Glob` -- Cursor/Copilot use different tool names
- `AskUserQuestion` -- No equivalent in most other tools
- `EnterPlanMode`, `ExitPlanMode` -- Claude Code-only concepts
- `Task` with subagent types (`Explore`, `Plan`, `Bash`) -- Claude Code-only
- `WebSearch`, `WebFetch` -- Naming varies by platform

**Frontmatter** (Claude Code-specific):
- `context: fork` -- Only meaningful in Claude Code's skill system
- `agent: Explore` -- Subagent concept specific to Claude Code
- `allowed-tools` -- Claude Code's tool restriction mechanism

**Concepts** (Claude Code-specific):
- Progressive disclosure (name/description loaded at startup, full content on invocation)
- Supporting files in skill directories
- Slash command invocation (`/analyze`, `/design`, etc.)

**Verdict**: If you copy ForgeKit's SKILL.md files into Cursor or Copilot, the AI will read the markdown instructions but won't be able to execute Claude Code-specific tool calls. The *intent* will be understood, but the *execution* will fail.

### 1.3 What IS Portable

The **methodology** embedded in the skills is 100% platform-agnostic:

| Portable (Methodology) | Not Portable (Implementation) |
|------------------------|-------------------------------|
| Incident documentation structure | `AskUserQuestion` checkpoints |
| Investigation 5-Whys framework | `Read`, `Grep` tool calls |
| RCA analysis patterns | `EnterPlanMode` transitions |
| Design trade-off matrices | `context: fork` frontmatter |
| Risk scoring methodology | `Task` subagent delegation |
| Systems analysis framework | Slash command invocation |
| Shared artifact conventions | Tool-specific file operations |

### 1.4 Emerging Cross-Platform Standards

**AGENTS.md** (July 2025, Sourcegraph):
- Vendor-neutral specification: "one file, any agent"
- Promises cross-tool compatibility
- Adopted by some tools but NOT universally yet
- Limited to static instructions (no interactive checkpoints, no frontmatter)

**rulesync** CLI:
- Generates tool-specific config from shared `.rulesync/*.md` files
- Supports Claude Code, Cursor, Gemini CLI, Copilot, Cline, Roo Code
- Open source, actively maintained
- Good for static rules, but can't replicate Claude Code's skill features

**ClaudeMDEditor**:
- Multi-tool config editor
- Manages Claude Skills, Cursor Rules, Windsurf Rules, Copilot Instructions
- Commercial tool (SaaS)

### 1.5 The MCP Solution

MCP (Model Context Protocol) is the **only mechanism** that provides true cross-platform compatibility WITH the ability to serve complex, interactive skill logic:

| MCP Client | Status | Source |
|------------|--------|--------|
| Claude Code | Full support (native) | Anthropic (MCP creator) |
| Cursor | Supported | cursor.com |
| Cline | Full support (MCP-native) | cline.bot |
| VS Code (Copilot) | Supported (2025+) | code.visualstudio.com |
| OpenAI Agents SDK | Supported | openai.github.io |
| Gemini | In progress | Google Cloud |

MCP is now under the **Linux Foundation** (Agentic AI Foundation), co-founded by Anthropic, Block, and OpenAI. This is not a single-vendor standard -- it's becoming the industry protocol.

---

## 2. Monetization Models Analysis

### 2.1 Model Comparison

| Model | IP Protection | Cross-Platform | Revenue Potential | Complexity | Verdict |
|-------|--------------|---------------|-------------------|------------|---------|
| **Open source + consulting** | None | Yes (public) | Low-Medium | Low | Good for awareness, bad for IP |
| **CLI + license key** | Weak (files readable) | Claude Code only | Medium | Medium | Easy to copy once installed |
| **SaaS subscription** | Medium (server-side) | Via API | Medium-High | High | Requires full web platform |
| **MCP server** | **Strong** (prompts on server) | **All MCP clients** | **High** | **Medium** | **Best fit for ForgeKit** |
| **Marketplace listing** | Strong (via marketplace) | Via marketplace | Medium-High | Low | Dependent on marketplace terms |
| **Enterprise licensing** | Strong (legal + technical) | Custom adapters | Very High | Very High | Requires sales team |

### 2.2 Why MCP Server Wins

The MCP server model solves every challenge simultaneously:

1. **IP Protection**: Skill prompts live on the server. Users connect to an MCP endpoint. The methodology, step-by-step instructions, templates, and logic **never exist as files on the user's filesystem**. The client receives prompt content in-memory, uses it for the current conversation, and discards it.

2. **Cross-Platform**: Any MCP-compatible tool (Claude Code, Cursor, Cline, VS Code Copilot, OpenAI Agents SDK) can connect to the same MCP server. Write skills once, serve everywhere.

3. **Monetization**: Natural usage metering -- bill per invocation, per skill, per seat, or via subscription. Infrastructure already exists (Moesif, MCPize, Apify).

4. **Updates**: Update skills server-side. All users get the latest version instantly. No `forgekit update` needed.

5. **Analytics**: Track which skills are used, how often, by whom. Data-driven product decisions.

6. **Access Control**: Tier skills by plan (Free/Pro/Enterprise). Revoke access immediately.

### 2.3 MCP Marketplace Infrastructure (Existing)

| Platform | Revenue Share | Audience | Features |
|----------|--------------|----------|----------|
| **MCPize** | 70% to developer | Growing marketplace | Unified billing, instant payouts, discovery |
| **Apify** | Varies | 36K+ monthly devs | "Build once, earn forever," zero upfront costs |
| **Cline Marketplace** | Varies | Hundreds of thousands | One-click install, developer controls monetization |
| **MCP Market** | Directory (no billing) | Discovery focused | Listing and discovery |
| **Official MCP Registry** | No monetization | Industry standard | Discovery, quality signals |

### 2.4 Pricing Strategy

| Tier | Skills Included | Target | Price Model |
|------|----------------|--------|-------------|
| **Free** | incident, research | Individual devs, trial | Free forever |
| **Pro** | All 7 skills + all modes + session management | Professional devs, small teams | $19-29/mo or usage-based |
| **Enterprise** | All skills + custom skill development + team analytics + priority support | Teams, organizations | $99-199/seat/mo |

Alternative: **Usage-based pricing** (per JSON-RPC method invocation):
- Each `/analyze`, `/design`, `/incident` call = 1 invocation
- Free tier: 50 invocations/month
- Pro: Unlimited invocations
- Enterprise: Unlimited + analytics + custom skills

---

## 3. MCP Technical Architecture for ForgeKit

### 3.1 MCP Primitives and How Skills Map

MCP defines three core primitives:

| Primitive | Control | Purpose | How ForgeKit Uses It |
|-----------|---------|---------|---------------------|
| **Tools** | Model-controlled (auto-invoked) | Execute actions with side effects | Skill execution logic (e.g., `analyze_risk`, `create_incident_report`) |
| **Prompts** | User-controlled (explicitly invoked) | Structured templates and workflows | Skill instructions (methodology, templates, output formats) |
| **Resources** | Application-controlled | Data context (files, APIs, DBs) | Shared artifacts (system-map, RCA templates, conventions) |

### 3.2 Skill-to-MCP Mapping

Each ForgeKit skill maps to MCP primitives:

```
ForgeKit Skill                    MCP Representation
─────────────                     ──────────────────
/incident {desc}        →        Prompt: "incident_report"
                                  - Parameters: {description, severity}
                                  - Returns: Structured prompt for incident documentation

/analyze risk           →        Prompt: "analyze_risk"
                                  - Parameters: {scope, risk_tolerance}
                                  - Returns: Multi-step analysis prompt with checkpoints
                                  + Tool: "analyze_discover_components"
                                  - Scans project and returns component list

/design tradeoff {topic} →       Prompt: "design_tradeoff"
                                  - Parameters: {topic, goal, constraints, priorities}
                                  - Returns: Full design analysis workflow
                                  + Resource: "design_report_template"
                                  - Provides output format template

/watchdog               →        Tool: "watchdog_start"
                                  - Parameters: {log_source, interval, keywords}
                                  - Side effect: Starts monitoring process
                                  + Tool: "watchdog_status"
                                  - Returns current monitoring status
```

### 3.3 MCP Server Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     ForgeKit MCP Server                        │
│                     (Python / FastAPI)                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │ Auth Layer  │  │ Metering    │  │ Skill Registry       │ │
│  │             │  │             │  │                      │ │
│  │ API keys    │  │ Per-call    │  │ skills/*.md (source) │ │
│  │ Tier check  │  │ Per-user    │  │ Parsed at startup    │ │
│  │ Rate limit  │  │ Analytics   │  │ Cached in memory     │ │
│  └─────────────┘  └─────────────┘  └──────────────────────┘ │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                  MCP Protocol Layer                    │   │
│  │                                                       │   │
│  │  Prompts:                                             │   │
│  │  ├── incident_report(description, severity)           │   │
│  │  ├── investigate(report_path)                         │   │
│  │  ├── rca_bugfix(issue)                                │   │
│  │  ├── analyze_health()                                 │   │
│  │  ├── analyze_risk(scope, tolerance)                   │   │
│  │  ├── analyze_component(component)                     │   │
│  │  ├── analyze_patterns(time_period)                    │   │
│  │  ├── analyze_architecture(focus)                      │   │
│  │  ├── design_tradeoff(topic, goal, constraints)        │   │
│  │  ├── design_validate(proposal)                        │   │
│  │  ├── design_migrate(from, to)                         │   │
│  │  ├── design_impact(change)                            │   │
│  │  ├── research(question)                               │   │
│  │  ├── session_start()                                  │   │
│  │  ├── session_end()                                    │   │
│  │  └── verify_session()                                 │   │
│  │                                                       │   │
│  │  Tools:                                               │   │
│  │  ├── watchdog_start(log_source, interval)             │   │
│  │  ├── watchdog_status()                                │   │
│  │  └── watchdog_stop()                                  │   │
│  │                                                       │   │
│  │  Resources:                                           │   │
│  │  ├── forgekit://conventions                           │   │
│  │  ├── forgekit://templates/incident                    │   │
│  │  ├── forgekit://templates/rca                         │   │
│  │  └── forgekit://templates/design-report               │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                  Transport Layer                       │   │
│  │                                                       │   │
│  │  Local:   stdio (for local development)               │   │
│  │  Remote:  Streamable HTTP (for hosted service)        │   │
│  │                                                       │   │
│  │  Note: SSE transport is deprecated as of 2026.        │   │
│  │  Use Streamable HTTP for remote MCP servers.          │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

User's AI Tool Config:
{
  "mcpServers": {
    "forgekit": {
      "url": "https://api.forgekit.ai/mcp",
      "headers": {
        "Authorization": "Bearer fk_..."
      }
    }
  }
}
```

### 3.4 How a Skill Invocation Works (MCP Flow)

```
User types: "I need to analyze the risk of our API layer"
                    │
                    ▼
┌─────────────────────────────────────────┐
│ AI Tool (Claude Code / Cursor / Cline)  │
│                                         │
│ 1. Sees ForgeKit MCP server connected   │
│ 2. Discovers available prompts          │
│ 3. Matches user intent → analyze_risk   │
│ 4. Calls: get_prompt("analyze_risk",    │
│      {scope: "API layer",               │
│       tolerance: "moderate"})           │
└─────────────────────────────────────────┘
                    │
                    ▼ (MCP JSON-RPC call)
┌─────────────────────────────────────────┐
│ ForgeKit MCP Server                     │
│                                         │
│ 1. Authenticates API key                │
│ 2. Checks tier (Pro required for        │
│    analyze_risk)                        │
│ 3. Meters the invocation                │
│ 4. Reads skills/analyze/SKILL.md        │
│ 5. Extracts risk mode instructions      │
│ 6. Adapts tool names for client type    │
│    (Claude: Read → Cursor: readFile)    │
│ 7. Returns structured prompt            │
└─────────────────────────────────────────┘
                    │
                    ▼ (MCP response with prompt content)
┌─────────────────────────────────────────┐
│ AI Tool                                 │
│                                         │
│ 1. Receives skill instructions          │
│ 2. Follows methodology step-by-step     │
│ 3. Uses local tools to read codebase    │
│ 4. Generates analysis report            │
│ 5. Presents findings to user            │
│                                         │
│ Note: Prompt content is IN-MEMORY only. │
│ Never written to disk. Discarded after  │
│ conversation ends.                      │
└─────────────────────────────────────────┘
```

### 3.5 Platform Adaptation Layer

The MCP server can adapt tool references for different clients:

```python
# Pseudo-code for platform adaptation
TOOL_MAPPING = {
    "claude_code": {
        "read_file": "Read",
        "search_code": "Grep",
        "find_files": "Glob",
        "edit_file": "Edit",
        "run_command": "Bash",
        "ask_user": "AskUserQuestion",
    },
    "cursor": {
        "read_file": "readFile",
        "search_code": "searchCode",
        "find_files": "findFiles",
        "edit_file": "editFile",
        "run_command": "runTerminalCommand",
        "ask_user": "askFollowup",
    },
    "copilot": {
        "read_file": "readFile",
        "search_code": "searchFiles",
        "find_files": "listFiles",
        "edit_file": "editFile",
        "run_command": "runCommand",
        "ask_user": "askUser",
    }
}

def adapt_skill_for_client(skill_content: str, client_type: str) -> str:
    """Replace generic tool references with client-specific names."""
    mapping = TOOL_MAPPING.get(client_type, TOOL_MAPPING["claude_code"])
    for generic, specific in mapping.items():
        skill_content = skill_content.replace(f"{{tool:{generic}}}", specific)
    return skill_content
```

This means the skill markdown files use generic tool references (`{tool:read_file}`) that get replaced with platform-specific names at serve time.

---

## 4. IP Protection Strategy

### 4.1 Legal Framework

AI prompts and skill instructions are protectable under multiple IP frameworks:

**Trade Secret** (Strongest for ForgeKit):
- Prompts that are original, confidential, and commercially valuable qualify as trade secrets
- Protection requires: (a) economic value from secrecy, (b) reasonable steps to maintain secrecy
- MCP server distribution = reasonable confidentiality measure (prompts never stored on user's machine)
- No registration required -- protection is automatic when conditions are met
- Both U.S. (Defend Trade Secrets Act) and international (TRIPS Agreement) protection

**Copyright** (Secondary protection):
- AI prompts are protectable as literary works when created with human skill and judgment
- ForgeKit's skills clearly demonstrate significant human authorship (methodology design, framework architecture, template creation)
- Copyright vests automatically upon creation
- Consider formal registration (U.S. Copyright Office) for enforcement advantages

**Contractual** (Tertiary protection):
- Terms of Service / EULA prohibiting reverse engineering, copying, redistribution
- API key agreement with usage restrictions
- Required for marketplace listing (MCPize, Apify)

### 4.2 Protection by Distribution Method

| Method | Trade Secret? | Copyright? | Contractual? | Overall |
|--------|--------------|-----------|-------------|---------|
| Open source repo | No (public) | Yes (license) | License only | Weak |
| CLI + symlinks | Weak (files on disk) | Yes | EULA possible | Moderate |
| **MCP server** | **Yes (prompts on server)** | **Yes** | **ToS + API agreement** | **Strong** |
| Marketplace | Yes (via platform) | Yes | Platform ToS | Strong |

### 4.3 Practical Measures

1. **MCP distribution**: Prompts served in-memory, never written to user's filesystem
2. **API key authentication**: Every invocation tied to an account
3. **Rate limiting**: Prevents bulk extraction of prompt content
4. **Terms of Service**: Explicitly prohibit:
   - Storing, copying, or redistributing prompt content
   - Reverse engineering the methodology
   - Automated extraction of prompt templates
5. **Metering/logging**: Detect unusual access patterns (potential extraction attempts)
6. **Obfuscation**: While not security, compressing/minifying served prompts raises the bar

### 4.4 Regulatory Considerations

**EU AI Act** (fully applicable August 2, 2026):
- ForgeKit skills are not high-risk AI (they're instructions for coding assistants)
- But monitor: transparency requirements may apply to agentic AI tools
- Consult legal counsel before EU market entry

**South Africa POPIA**:
- If collecting user data (analytics, API keys), POPIA compliance required
- Privacy policy, data processing agreements

---

## 5. Phased Architecture & Roadmap

### Phase 1: Private Development (NOW)

**Goal**: Consolidate skills into a private repo, develop and refine.

```
fluxforgeai/forgekit (private GitHub repo)
├── pyproject.toml                  # Package definition + CLI
├── README.md
├── CONVENTIONS.md
├── src/forgekit/
│   ├── __init__.py
│   └── cli.py                      # init, update, status, commit, push
├── skills/                         # 7 operational skills
│   ├── incident/SKILL.md
│   ├── investigate/SKILL.md
│   ├── rca-bugfix/SKILL.md
│   ├── watchdog/SKILL.md
│   ├── analyze/
│   │   ├── SKILL.md
│   │   ├── DESIGN_ESCALATION.md
│   │   └── DESIGN_SKILL_SPEC.md
│   ├── design/SKILL.md
│   └── research/SKILL.md
├── commands/                       # Session management
│   ├── session-start.md
│   ├── session-end.md
│   ├── session-init.md
│   └── verify-session.md
└── docs/research/                  # Skill design research
```

**Usage**: Symlinks for personal use across projects.
**Distribution**: None (private repo, personal use only).
**IP Status**: Trade secret (private, access-controlled).

### Phase 2: MCP Server MVP

**Goal**: Serve skills via MCP for closed-source distribution + cross-platform support.

```
fluxforgeai/forgekit
├── (Phase 1 structure)
├── server/                         # NEW: MCP server
│   ├── pyproject.toml
│   ├── src/forgekit_server/
│   │   ├── __init__.py
│   │   ├── main.py                 # MCP server entrypoint
│   │   ├── auth.py                 # API key validation
│   │   ├── skill_registry.py       # Load + cache skills from markdown
│   │   ├── platform_adapter.py     # Tool name mapping per client
│   │   ├── prompts.py              # MCP prompt handlers
│   │   ├── tools.py                # MCP tool handlers (watchdog)
│   │   └── resources.py            # MCP resource handlers (templates)
│   └── tests/
├── deploy/
│   ├── Dockerfile
│   └── fly.toml                    # or Railway/Render config
```

**Usage**: Beta users connect MCP client to hosted server.
**Distribution**: API key gated, hosted MCP server.
**IP Status**: Strong (trade secret + copyright + ToS).

### Phase 3: Marketplace & Monetization

**Goal**: Revenue from ForgeKit skills.

- List on MCPize (70% revenue share)
- List on Cline Marketplace
- Register on Official MCP Registry
- Implement Moesif metering/billing
- Launch pricing tiers (Free/Pro/Enterprise)
- Marketing: dev blog, social, demo videos

### Phase 4: Platform Expansion

**Goal**: Maximize reach across all AI coding tools.

- Implement platform adaptation layer (Claude/Cursor/Copilot tool mapping)
- Add AGENTS.md export (for tools that don't support MCP yet)
- Build custom MCP clients for platforms without native support
- Enterprise: Custom skill development, team analytics dashboard

---

## 6. Market Opportunity

### 6.1 Market Size

| Metric | Value | Source |
|--------|-------|--------|
| AI market (2023) | $200 billion | Statista |
| AI market (2030) | $1.8 trillion | Statista |
| Autonomous AI agent market (2026) | $8.5 billion | Deloitte |
| Autonomous AI agent market (2030) | $35 billion | Deloitte |
| Orchestration uplift potential | +15-30% | Deloitte |
| AIOps market (2025-2030) | $11-16B → $30B+ | Middleware.io |
| MTTR reduction with AI | 17.8% avg, 30-70% leaders | incident.io |

### 6.2 Competitive Landscape

**Direct competitors** (AI coding skill marketplaces):
- MCPize, Cline Marketplace -- marketplace platforms, not skill creators
- awesome-claude-skills (GitHub) -- community-curated, open source, no monetization
- ClaudeMDEditor -- config editor, not skill content

**No direct competitor** exists that offers:
- A complete, integrated skill suite (incident → investigate → analyze → design pipeline)
- Cross-platform MCP delivery
- SRE/DevOps domain expertise embedded in skills
- Interactive checkpoints and design escalation

### 6.3 Differentiation

ForgeKit is NOT just a set of prompt templates. The differentiation is:

1. **Integrated pipeline**: Skills chain together (watchdog → incident → investigate → rca-bugfix → plan). Individual prompts don't have this.

2. **Interactive methodology**: Skills with checkpoints (`AskUserQuestion`) adapt to the user's context rather than being one-shot templates.

3. **Design escalation**: The analyze → design bridge is a novel pattern -- analysis findings automatically suggest architectural exploration.

4. **Institutional memory**: Shared artifacts pattern (`docs/RCAs/`, `docs/analysis/`, `system-map.md`) build knowledge across sessions.

5. **Domain depth**: SRE incident response, systems analysis, and architectural design -- not generic "code review" or "documentation" skills.

---

## 7. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| MCP adoption stalls | Low (Linux Foundation backing, Anthropic+OpenAI+Block) | High | Maintain CLI fallback, AGENTS.md export |
| Prompt extraction via MCP | Medium (determined users could capture in-memory prompts) | Medium | Legal protection (ToS), rate limiting, obfuscation |
| Platform breaks MCP compatibility | Low | Medium | Multi-platform testing, adapter layer |
| Competitor copies methodology | Medium (can't protect ideas, only expression) | Medium | First-mover advantage, continuous innovation, brand |
| EU AI Act compliance burden | Low (not high-risk AI) | Low | Monitor regulations, consult legal |
| Market too early (not enough MCP users) | Medium | Medium | Start with Claude Code symlinks (Phase 1), transition to MCP when market matures |
| Context budget: MCP-served prompts still consume tokens | Certain | Low | Optimize prompt length, offer `--quick` mode |

---

## 8. Key Decisions

### 8.1 Decided

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Repo name | `fluxforgeai/forgekit` | Brandable, no "Claude" trademark risk, product-ready |
| Distribution (Phase 1) | Private repo + symlinks | Development environment, no exposure |
| Distribution (Phase 2+) | MCP server | Cross-platform + closed-source + monetizable |
| IP protection | Trade secret + copyright + ToS | Strongest available for prompt-based IP |
| Include session commands | Yes | Part of the integrated toolkit |
| Include research docs | Yes | Skill design research = product documentation |

### 8.2 To Decide (Future)

| Decision | Options | When to Decide |
|----------|---------|----------------|
| MCP server hosting | Fly.io / Railway / Render / self-hosted | Phase 2 |
| Marketplace listing | MCPize / Cline / both / own | Phase 3 |
| Pricing model | Subscription vs usage-based vs hybrid | Phase 3 |
| Platform adaptation | Generic tool refs vs platform-specific builds | Phase 2 |
| Free tier scope | Which skills free vs paid | Phase 3 |
| Team/org features | Analytics, shared artifacts, RBAC | Phase 4 |

---

## 9. Immediate Next Steps

1. **Create `fluxforgeai/forgekit` repo** on GitHub (private)
2. **Move all 7 skills + 3 commands** into repo
3. **Genericize** project-specific references (absolute paths → relative)
4. **Build CLI** (`forgekit init/update/status/commit/push`)
5. **Symlink back** to pilot_connector for continued use
6. **Verify** skills work through symlinks
7. **Start thinking** about generic tool references in SKILL.md files (prep for Phase 2 MCP adaptation)

---

## Sources

### Cross-Platform & Configuration
1. [rulesync: Unified AI config management for Claude Code, Gemini CLI, Cursor](https://dev.to/dyoshikawatech/rulesync-published-a-tool-to-unify-management-of-rules-for-claude-code-gemini-cli-and-cursor-390f)
2. [One Prompt to Rule Them All: Reuse Instructions Across Copilot, Claude, Cursor & Codex](https://medium.com/@genyklemberg/one-prompt-to-rule-them-all-how-to-reuse-the-same-markdown-instructions-across-copilot-claude-42693df4df00)
3. [AGENTS.md: Why your README matters more than AI configuration files](https://devcenter.upsun.com/posts/why-your-readme-matters-more-than-ai-configuration-files/)
4. [ClaudeMDEditor: Manage AI Coding Assistant Config Files](https://www.claudemdeditor.com/)
5. [Sharing rules between Copilot and Cursor - Cursor Forum](https://forum.cursor.com/t/sharing-rules-between-copilot-and-cursor/53873)

### MCP Protocol & Architecture
6. [MCP Server Concepts - Official Documentation](https://modelcontextprotocol.io/docs/learn/server-concepts)
7. [What Is MCP? The 2026 Guide](https://generect.com/blog/what-is-mcp/)
8. [MCP - Wikipedia (governance, Linux Foundation)](https://en.wikipedia.org/wiki/Model_Context_Protocol)
9. [Building Effective AI Agents with MCP - Red Hat](https://developers.redhat.com/articles/2026/01/08/building-effective-ai-agents-mcp)
10. [What is MCP? - Google Cloud](https://cloud.google.com/discover/what-is-model-context-protocol)
11. [What is MCP? - IBM](https://www.ibm.com/think/topics/model-context-protocol)
12. [OpenAI Agents SDK - MCP Support](https://openai.github.io/openai-agents-python/mcp/)
13. [MCP Servers in VS Code (Copilot)](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)

### MCP Monetization & Marketplaces
14. [MCPize: MCP Server Marketplace - 70% Revenue Share](https://mcpize.com/)
15. [Building the MCP Economy: Lessons from 21st.dev - Cline Blog](https://cline.bot/blog/building-the-mcp-economy-lessons-from-21st-dev-and-the-future-of-plugin-monetization)
16. [Monetizing MCP Servers with Moesif](https://www.moesif.com/blog/api-strategy/model-context-protocol/Monetizing-MCP-Model-Context-Protocol-Servers-With-Moesif/)
17. [Build and Monetize MCP Servers - Apify](https://apify.com/mcp/developers)
18. [MCP Server Economics: TCO, Business Models & ROI](https://zeo.org/resources/blog/mcp-server-economics-tco-analysis-business-models-roi)
19. [Official MCP Registry](https://registry.modelcontextprotocol.io/)

### IP Protection
20. [IP Protection for AI Prompts - Shift Law](https://shiftlaw.ca/intellectual-property-protection-for-ai-prompts/)
21. [From Prompt to Protection: Who Owns AI-Generated IP? - Tannenbaum Helpern](https://www.thsh.com/blog/from-prompt-to-protection-who-owns-ai-generated-ip/)
22. [Practical Guide to Protecting AI Models with Trade Secrets - Hunton](https://www.hunton.com/insights/publications/a-practical-guide-to-protecting-ai-models-with-trade-secrets)
23. [Protecting AI Assets with IP Strategies - Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/12/protecting-ai-assets-and-outputs-with-ip-strategies-in-a-changing-world)

### Market & Trends
24. [Deloitte: Unlocking Exponential Value with AI Agent Orchestration](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-agent-orchestration.html)
25. [Analytics Vidhya: 15 AI Agent Trends 2026](https://www.analyticsvidhya.com/blog/2026/01/ai-agents-trends/)
26. [5 Practical Ways Engineers Are Monetizing AI Skills 2026](https://medium.com/@AThoughtbySnehal/5-practical-ways-engineers-are-monetizing-ai-skills-in-2026-b0b8367ed789)
27. [12 AI Coding Trends That Will Dominate 2026](https://medium.com/ai-software-engineer/12-ai-coding-emerging-trends-that-will-dominate-2026-dont-miss-out-dae9f4a76592)

### Claude Code Skills
28. [Claude Code: Extend Claude with Skills](https://code.claude.com/docs/en/skills)
29. [Anthropic: Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
30. [GitHub #17283: context:fork not honored via Skill tool](https://github.com/anthropics/claude-code/issues/17283)

### Related Internal Documents
31. `docs/research/2026-01-26_1410_skills_integration_architecture.md` -- Skills integration architecture (how the 7 skills interconnect)
32. `docs/research/2026-01-23_0615_systems_analyst_skill_design.md` -- Systems analyst skill foundational research
33. `.claude/skills/analyze/DESIGN_ESCALATION.md` -- Analyze → Design escalation bridge
34. `.claude/skills/analyze/DESIGN_SKILL_SPEC.md` -- Design skill full specification

---

**Research Complete**: 2026-01-26 15:49 UTC
