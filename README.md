# LLM Judgment Control Engine

![demo](assets/demo-block.gif)

Stop LLMs from drifting, forgetting context, hallucinating, and wasting expensive model calls.

---

## 🔴 The Problem

LLMs in long sessions:

* forget key context
* drift away from the task
* hallucinate under uncertainty
* overuse expensive models

---

## 🎬 Demo 0 — System Overview

[Watch demo](assets/demo_overview.gif)

→ Runtime judgment layer before execution

---

## 🎬 Demo 1 — Dangerous Change (Block)

[Watch demo](assets/demo_block.gif)

→ Prevents breaking API / destructive execution

---

## 🎬 Demo 2 — Normal Execution (Commit)

[Watch demo](assets/demo_commit.gif)

→ Safe task proceeds with lightweight model

---

## 🎬 Demo 3 — Constraint-Aware Execution (Commit)

[Watch demo](assets/demo_commit2.gif)

→ Executes while preserving constraints and context

---

## 🎬 Demo 4 — Context Drift (Hold)

[Watch demo](assets/demo_hold.gif)

→ Pauses execution when context becomes unstable

---

## 🧠 Core Mechanism

task → thesis check → slot carry → recovery recenter → risk gate → decision

---

## Benchmark

| Mode       | Full Executions   | Tokens   | Thesis Score   |
| ---------- | ----------------- | -------- | ---------------|
| Baseline   | 100               | 81,411   | 4.52           |
| Engine     | 18~35             | ↓79%     | ↑              |

---

## Vision

LLMs should not just generate.

They should decide when to act.
