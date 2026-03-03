---
name: tera-time-blocking
description: "Plan days/weeks with time-blocking: maintain persistent backlog, convert vague tasks into SMART discrete assignments, estimate in 15-minute blocks, prioritize (Work→Passion→Play), output clean schedule. Use when user says plan my day/week, time block, schedule tasks, what should I do today, or shares messy task list."
---

# Tera Time Blocking

## Quick Start

1. **Maintain a task backlog** — Store all tasks in a table with: outcome, blocks, category, priority, due date
2. **Convert tasks to SMART format** before scheduling — outcome + time leash + bullet steps
3. **Use 15-minute blocks** as your unit of time
4. **Follow WPP order** — Work → Passion → Play

## Core Workflow

### A) Intake: Messy → Discrete Assignments

When user mentions a task (even casually):
1. If vague, ask clarifying questions immediately
2. If >8 blocks (2 hours), split into multiple assignments
3. Convert to SMART format:
   - **Outcome** — What "done" looks like
   - **Blocks** — Time leash (15-min units)
   - **Steps** — Next-action bullets + mousetrap if likely to resist
4. Add to backlog table

### B) Plan the Day ("plan my day", "time block today")

1. **Establish window** — Weekdays: before 9AM + after 5PM. Weekends: ask user.
2. **Pull tasks** — From backlog + any new ones processed via Intake
3. **Prioritize** — Work → Passion → Play, then: Eat-the-frog / Quick wins / Deadline / Energy matching
4. **Slot into blocks** — Show start→end time, task, notes
5. **If overflow** — Show what doesn't fit, propose defer/drop

### C) Plan the Week ("plan my week")

1. Show backlog summary (priorities + due dates)
2. Assign tasks to days (no times yet)
3. Offer to drill into specific day

## Key Reference

Read `references/tera-system-prompt.md` for:
- Full Noah-specific constraints (9-5 work, 8pm bedtime, gym drive times)
- Task table format details
- Status/category values
- Example output formats
- Complete interaction rules

## Output Format

- Backlog table (only if changed or user asked)
- Time-blocked schedule with timestamps + block counts
- Carry-forward list (Todo + In Progress)

## Guardrails

- Never schedule >8 blocks continuously — split it
- Don't guess durations — ask if unsure
- Always warn when overcommitted (show math)
- Protect decompression time — don't fill every block
