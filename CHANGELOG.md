# Changelog

All notable changes to the `zhihu-operations-skill` project will be documented in this file.

## [1.0.0] - 2026-10-12

### Initial Open-Source Release
- **Core Skill Spec**: Release `zhihu-operations/SKILL.md` compliant with Hermes Agent, Claude Code, and OpenCode workflows.
- **De-AI Answer Linter**: Standalone `lint.py` enforcing developer voice, 19 hard bans, AI density gates (bold text <= 8%, list items <= 8), and cross-answer fingerprint checks.
- **Publishing Cadence Guard**: Stateful `guard.py` implementing daily answer limits (1-2 answers), minimum 6h gap, midnight blackout (00:00-07:00 CST), and 48h risk cooldown.
- **Question Potential Evaluator**: CLI tool `question_evaluator.py` scoring follower-to-answer ratio, view density, and Wilson cold-start viability.
- **Reference Playbooks**:
  - `wilson_ranking_and_algorithm.md`: Deep dive on Wilson score interval lower bound and upvote weighting.
  - `multi_target_feed_and_search.md`: DNN 8-objective recommendation model and long-tail SEO.
  - `anti_ai_linter_and_fingerprint.md`: Anti-AI detection paths, hard bans, and cross-answer fingerprint elimination.
  - `three_tier_evidence_system.md`: 3-Tier Evidence protocol (official docs -> reproducible benchmarks -> qualitative observations).
  - `publishing_cadence_and_antiban.md`: Publishing quotas, golden windows, and anti-ban mechanics.
  - `monetization_and_traffic_separation.md`: Four monetization paths and the 80/20 physical separation rule.
- **Templates**: Production-grade answer templates for technical deep-dives, tool evaluations, and consulting cards.
- **Automated Tests**: 100% passing unit tests under Python `unittest`.
