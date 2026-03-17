---
name: deep-research
description: Enforce Learn vs Research mode selection in #research channel before any research is done
---

# Deep Research Skill

## Trigger
When a message appears in channel `1477790472180207818` (#research), this skill activates.

## Auto-Start Server
If the deep research server at localhost:2024 is not running, start it first:
```
~/start-langgraph.sh
```
Wait for it to come online before proceeding.

## Mandatory Workflow

### Step 1: Never research without mode selection
When a user posts a research topic, you MUST respond asking for mode preference BEFORE doing any research:

> **Got it — researching: [TOPIC]**
>
> How do you want this?
>
> 🧠 **Learn** — I'll go deep and explain it to you conversationally. Good for building intuition.
>
> 📋 **Research** — I'll produce a structured brief with full citations and save it to your vault.

Wait for the user to select a mode before proceeding.

### Step 2: Clarification (Optional)
After mode selection, you MAY ask at most 2 clarifying questions if the topic is too broad. Otherwise, proceed to research.

### Step 3: Execute Research
Run the research using open_deep_research via the local API at http://127.0.0.1:2024

### Step 4: Deliver Results

**Learn Mode:**
- Conversational response in the thread
- Lead with the most interesting/counterintuitive finding
- Cite sources inline naturally

**Research Mode:**
- Summary in thread
- Full report saved to vault at `references/YYYY-MM-DD-[topic-slug].md`

## Rules
- NEVER skip the mode selection step
- NEVER begin research without user confirmation
- Always ask Learn vs Research first
- Always check/start the server at localhost:2024 first
