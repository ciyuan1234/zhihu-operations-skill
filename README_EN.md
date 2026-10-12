# Zhihu Technical Creator Operations Skill

[![Hermes Agent Skill](https://img.shields.io/badge/Hermes_Agent-Skill-blue.svg)](https://hermes-agent.nousresearch.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)
[![Tested with Unittest](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](zhihu-operations/tests)

A battle-tested creator operations and content engineering Skill designed for **software engineers, AI builders, open-source developers, and technical writers** publishing on Zhihu (知乎).

Distilled from reverse-engineering Zhihu's algorithmic ranking mechanics, anti-bot filtering counter-measures, and autonomous multi-agent pipelines, this Skill addresses four core bottlenecks faced by technical creators:
1. **Misunderstanding Ranking Mechanics**: Assuming raw upvotes determine position, failing to recognize that Zhihu uses the **Wilson score interval lower bound** with **domain-weighted voting**, where a single downvote from a senior developer can sink an answer;
2. **Algorithmic Folding for "AI-Generated Content"**: Triggering Wali anti-bot classifiers due to dialectical clichés ("不是A而是B"), boilerplate summaries, and listicle formatting over-saturation;
3. **Severe Peer Backlash from Fabricated Data**: Fabricating unverified precision metrics (e.g. "3.8x speedup", "18.2s execution time") that are dismantled by technical readers in comments;
4. **Chaotic Monetization Strategy**: Contaminating traffic-revenue answers (致知计划) with commercial affiliate cards, instantly disqualifying the answer from traffic payouts.

---

## 🌟 Core Architecture

```
zhihu-operations/
├── SKILL.md                                 # Hermes Agent / Claude Code skill specification
├── scripts/
│   ├── lint.py                              # De-AI text linter, AI density auditor & fingerprint detector
│   ├── guard.py                             # Pacing guard (1-2 answers/day, 6h min gap, midnight blackout)
│   └── question_evaluator.py                # Multi-dimensional question potential evaluator
├── references/
│   ├── wilson_ranking_and_algorithm.md      # Wilson score mathematical model, weighted votes & downvotes
│   ├── multi_target_feed_and_search.md      # DNN 8-objective recommendation model & long-tail search SEO
│   ├── anti_ai_linter_and_fingerprint.md    # Detection vectors, banned patterns, formatting density & fingerprints
│   ├── three_tier_evidence_system.md        # 3-Tier Evidence protocol: Official docs -> Benchmarks -> Qualitative
│   ├── publishing_cadence_and_antiban.md    # Quotas, golden posting windows & the crucial 2h cold-start window
│   └── monetization_and_traffic_separation.md# Monetization channels & the 80/20 physical separation rule
└── templates/
    ├── answer_technical_deep_dive.md        # Deep debugging & system internals answer template
    ├── answer_tool_evaluation.md            # Tool comparison & monorepo evaluation template
    └── consulting_card_hook.md              # Commercial consulting hook & retention footer template
```

---

## 🚀 Key Rules & Invariants

### 1. Wilson Score Lower Bound & Downvote Fatality
- **Upvote Ratio Trumps Raw Volume**: Zhihu ranks answers by the lower bound of the Wilson score interval, which penalizes small samples and heavily penalizes negative feedback. An answer with 20 upvotes and 0 downvotes often outranks an answer with 500 upvotes and 80 downvotes.
- **High-Weight Peer Downvotes**: Downvotes cast by senior creators with high topical authority carry massive negative weight. Technical content must be rock-solid with zero factual bugs.

### 2. Three-Tier Evidence Standard
- **Tier 1 (Official Specs)**: Grounded in vendor release notes or architecture whitepapers;
- **Tier 2 (Reproducible Benchmarks)**: Backed by disk logs and exact hardware specifications (e.g. M3 Pro 18GB). Synthetic numbers like "3.8x speedup" without reproduction are strictly banned;
- **Tier 3 (Qualitative Observations)**: When precise instrument logs are unavailable, **honestly fall back to qualitative observations** ("substantially smoother response", "occasional hitching on 50MB files") instead of inventing pseudo-precise figures.

### 3. De-AI Standards & Fingerprint Elimination
- **Golden First 100 Words**: Deliver the direct verdict, version, and hardware environment in the first 3 sentences. Avoid preamble background context.
- **Formatting Density Gating**: Bold text must not exceed **8%** of body characters; list items must not exceed **8 items**.
- **Anti-Fingerprinting**: Avoid templated opening formulas ("Date + conclusion") and identical closing rhetorical questions across multiple answers on the same account.

### 4. 80/20 Physical Separation for Monetization
- **致知计划 (Traffic Share)**: Requires Lv4+, 100+ followers, and 3,000 quality score. Pure traffic duration payout. **Strictly forbids affiliate cards ("好物推荐") or consultation cards**, which immediately void revenue. 80% of answers must remain pure technical content.
- **Commercial Cards (20% Allocation)**: Dedicated hardware reviews or book recommendations with contextual affiliate links, or 1-on-1 paid technical troubleshooting sessions.

---

## 🛠️ Quick Start

### One-Click Installation
```bash
git clone https://github.com/ciyuan1234/zhihu-operations-skill.git
cd zhihu-operations-skill

# Install into Hermes Agent skills directory (~/.hermes/skills/social-media/)
./install.sh
```

Windows PowerShell:
```powershell
.\install.ps1
```

### 1. Run Automated Linter
```bash
python3 zhihu-operations/scripts/lint.py zhihu-operations/templates/answer_technical_deep_dive.md
```

### 2. Check Cadence Guard
```bash
python3 zhihu-operations/scripts/guard.py check
python3 zhihu-operations/scripts/guard.py record-answer
python3 zhihu-operations/scripts/guard.py set-cooldown 48
```

### 3. Evaluate Question Potential
```bash
python3 zhihu-operations/scripts/question_evaluator.py --followers 1800 --answers 25 --views 65000 --title "How to manage subprocess concurrency cleanly in Python?"
```

---

## 🧪 Unit Testing

Run the test suite verifying linter rules, cadence constraints, and question scoring:
```bash
python3 -m unittest discover -s zhihu-operations/tests -p "test_*.py"
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
