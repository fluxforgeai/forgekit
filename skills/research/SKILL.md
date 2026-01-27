# Research Skill

**Trigger**: Use `/research {question or topic}` when you need to research a technical topic, error, or concept and create a documented record.

**Purpose**: Research topics thoroughly, document findings with sources, and build a knowledge base to avoid repeating the same issues.

**Examples**:

- `/research Why does Iterable batch export return 400 after job expires?`
- `/research What are httpx timeout best practices for long-running downloads?`
- `/research How does GCS resumable upload handle network interruptions?`
- `/research [pasted error message or documentation]`

---

## Instructions

1. **Identify the technoloies/topics** involved in the question
2. **Research official documentation** (search as of {current_month_year})
3. **Research online** for community knowledge, Stack Overflow, GitHub issues (search as of {current_month_year})
4. **Check existing research** in `docs/research/` and `docs/RCAs/` to avoid duplicating work
5. **Write research report** to `docs/research/{YYYY-MM-DD_HHMM}_{topic}.md`
6. **STOP** and await further instructions

---

## Research Process

### Step 1: Identify What to Research

Parse the user's question or pasted text to identify:

- Which technologies/API/library are involved?
- What specific behavior, enhancement or error needs explanation?
- What is the user trying to understand?
- What is the user trying to implement?

### Step 2: Search Official Documentation

**Search as of {current_month_year}** for the relevant technology:

**EXAMPLES** (use as patterns, search for whatever is relevant):

- If about **Iterable**: Search "Iterable API {topic} {current_month_year}"
- If about **Intercom**: Search "Intercom API {topic} {current_month_year}"
- If about **GCS**: Search "Google Cloud Storage {topic} {current_month_year}"
- If about **httpx**: Search "Python httpx {topic} {current_month_year}"
- If about **FastAPI**: Search "FastAPI {topic} {current_month_year}"
- If about **PostgreSQL**: Search "PostgreSQL {topic} {current_month_year}"
- If about **Python**: Search "Python {topic} {current_month_year}"

**IMPORTANT**: Only search documentation relevant to the actual question. Identify the technology first, then search.

### Step 3: Search Online Resources

Search for:

- Stack Overflow questions/answers
- GitHub issues and discussions
- Blog posts from reputable sources
- Official changelogs or release notes

### Step 4: Check Existing Knowledge

Before writing, check:

- `docs/research/` - Have we researched this before?
- `docs/RCAs/` - Have we encountered this issue before?
- `docs/investigations/` - Any related investigations?
- `docs/plans/` - Any implementation plans that addressed this?

If existing research exists, reference it and add new findings.

### Step 5: Synthesize Findings

Combine all sources into a coherent answer:

- What does the official documentation say?
- What does the community say?
- Are there any gotchas or undocumented behaviors?
- What are the best practices?

---

## Research Report Template

Write to: `docs/research/{YYYY-MM-DD_HHMM}_{topic}.md`

Example: `docs/research/2026-01-22_1730_iterable_batch_export_expiration.md`

```markdown
# Research: {Topic/Question}

**Date**: {YYYY-MM-DD}
**Researcher**: Claude Code
**Status**: Complete

---

## Question

{The original question or topic being researched}

---

## TL;DR

{2-3 sentence summary of the key findings}

---

## Official Documentation

### {Technology Name} Documentation

{Findings from official docs}

> "{Direct quote from documentation}"
> — Source: [{Doc title}]({URL})

### Key Points from Docs
- {Point 1}
- {Point 2}
- {Point 3}

---

## Community Knowledge

### Stack Overflow / GitHub Issues

{Findings from community sources}

> "{Relevant quote or summary}"
> — Source: [{Title}]({URL})

### Common Pitfalls Mentioned
- {Pitfall 1}
- {Pitfall 2}

---

## Best Practices

Based on research:

1. **{Practice 1}**: {Explanation}
2. **{Practice 2}**: {Explanation}
3. **{Practice 3}**: {Explanation}

---

## Relevance to Our Codebase

{How this applies to our specific implementation}

### Files That May Be Affected
- {file1.py}
- {file2.py}

---

## Implementation Analysis

### Already Implemented
{What we already have in place that addresses this topic}

- {Feature/pattern we already use}: `{file.py:line}` - {how it relates}
- {Another existing implementation}: `{file.py:line}` - {how it relates}

### Should Implement
{What we should add based on this research}

1. **{Recommendation}**
   - Why: {Justification based on research}
   - Where: `{file.py}`
   - How: {Brief approach}

2. **{Recommendation}**
   - Why: {Justification based on research}
   - Where: `{file.py}`
   - How: {Brief approach}

### Should NOT Implement
{What we should avoid and why}

1. **{Anti-pattern or approach to avoid}**
   - Why not: {Reason based on research - gotchas, performance, compatibility}
   - Source: {Reference to doc or community warning}

2. **{Another thing to avoid}**
   - Why not: {Reason}
   - Source: {Reference}

---

## Sources

1. [{Title 1}]({URL1}) - {brief description}
2. [{Title 2}]({URL2}) - {brief description}
3. [{Title 3}]({URL3}) - {brief description}

---

## Related Documents

- {Link to related RCA if any}
- {Link to related investigation if any}
- {Link to related research if any}

---

**Research Complete**: {YYYY-MM-DD HH:MM} UTC
```

---

## After Writing

**STOP** and tell the user:

```
Research complete.

Report saved to: docs/research/{YYYY-MM-DD_HHMM}_{topic}.md

Summary: {2-3 sentence TL;DR}

Key sources:
- {Source 1 with link}
- {Source 2 with link}

Awaiting your instructions. Options:
- Ask follow-up questions
- Run `/investigate` if this relates to an incident
- Run `/plan` to implement recommendations
```

**Do NOT continue.** Wait for the user to decide how to proceed.
