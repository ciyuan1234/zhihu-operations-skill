---
name: zhihu-operations
description: "Operate Zhihu technical answers, anti-AI lint and cadence."
version: 1.5.0
author: 秋安 (ciyuan1234), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zhihu, creator, social-media, anti-ai, publishing, operations, github-sync]
    category: social-media
---

# Zhihu Operations Skill

Operate Zhihu (知乎) creator accounts for developer and technology verticals. Enforces Wilson score algorithm alignment, strict anti-AI style linting, Hemingway technical prose architecture, 3-tier evidence gates, publishing cadence guardrails, traffic-channel monetization separation (致知计划 vs 好物推荐 vs 付费咨询), anxiety-to-solution conversion frameworks, vertical domain purity gates, automated deduplication, DraftJS paste event handling, SPA navigation optimization, and automated GitHub open-source synchronization.

## When to Use

- Writing, reviewing, or editing Zhihu answers, articles, or thoughts in software, AI, or developer tooling.
- Applying Hemingway technical prose standards: concise declarative sentences, cold sensory realism (terminal cursor, panic stack traces, memory limits), zero marketing filler.
- Turning high-traffic anxiety questions ("Will AI replace programmers?", job market concerns) into authoritative technical answers with reproducible solutions.
- Constructing evergreen content moats around CS fundamentals (OS, Computer Organization, Networks, Debugging methodology).
- Enforcing domain purity gates to prevent persona dilution or cross-vertical contamination.
- Auditing draft answers against anti-AI standards (`scripts/lint.py`) to prevent content folding, account de-weighting, or Wali/Wukong automated penalty.
- Checking publishing cadence and intervals (`scripts/guard.py`) to prevent spam flags (daily cap 1-3, minimum 4-6h gap, midnight blackout 00:00-07:00 CST).
- Scoring potential questions (`scripts/question_evaluator.py`, `selector.py`) to target high-traction, high-search-value answer candidates.
- Filtering out already-answered questions from candidate pools to prevent accidental answer overwrites.
- Automating DraftJS editor input (answers, comments, and thoughts) using native `ClipboardEvent('paste')` synthesis.
- Executing fast browser navigation via in-session `eval "location.href = '...'; 'ok'"` to bypass blocking CLI goto timeouts on heavy SPAs.
- Handling dynamic anti-crawler `zse-ck` challenges with mandatory 25-minute quiet cooldowns.
- Applying the 3-Tier Evidence Standard (official docs -> reproducible benchmarks -> qualitative observations) to eliminate fabricated metrics.
- Structuring monetization funnels while strictly keeping 致知计划 (pure traffic revenue) and affiliate cards physically separated.
- Synchronizing local skill updates to the open-source GitHub repository (`ciyuan1234/zhihu-operations-skill`).
- Don't use for: Salt fiction/storytelling, generic marketing ad spam, or paid upvote/shill rings (banned by platform).

## Prerequisites

- Python 3.9+ (Python 3.10+ recommended) for linting, cadence guard, and evaluation scripts.
- Platform account: Zhihu account (`zhihu.com`).
- GitHub repository: `https://github.com/ciyuan1234/zhihu-operations-skill`.

## Quick Reference

```bash
# Lint an answer draft against anti-AI and structure rules
python3 scripts/lint.py drafts/answer_example.md

# Check if publishing is currently allowed
python3 scripts/guard.py check

# Record a published answer event
python3 scripts/guard.py record-answer

# Evaluate question traffic potential
python3 scripts/question_evaluator.py --followers 1200 --answers 35 --views 150000

# Trigger immediate manual sync to GitHub
sync-skills
```

## Core Invariants & Rules

1. **Wilson Confidence Bound Ranking & High-Weight Downvotes**:
   - Zhihu ranks answers by the lower bound of the Wilson score interval, not raw upvote counts. Upvote ratio (赞同比) is vastly more important than total upvotes.
   - Downvotes from high-weight domain creators are catastrophic. A technical claim with errors can sink an answer instantly. Content must have zero factual mistakes.

2. **Developer Voice & Anti-AI Standard**:
   - **Golden First 100 Words**: Deliver the direct verdict and first-hand stance immediately. State the testing environment, tool version, and concrete outcome within the first 3 sentences. No philosophical lead-ins.
   - **Micro-Paragraphs & Sentence Variance**: Keep paragraphs under 3 sentences to prevent dense corporate-report aesthetics, but avoid uniform 1-sentence paragraphs throughout the whole answer (which triggers the `[WARN] §5 段落句数几乎全为 1 句` linter alert). Interweave punchy single-sentence declarations with 2-3 sentence technical context.
   - **Absolute Phrase Bans**: Ban rhetorical binary contrasts ("不是A而是B", "并非……而是……"), mechanical transition labels ("首先/其次/最后", "总而言之"), platform clichés ("作为一名程序员", "在AI飞速发展的今天"), and bolded tag lists (`- **性能：** ...`).
   - **Cross-Answer Deduplication & Fingerprinting**: Never reuse identical opening formulas ("日期 + 先说结论"), benchmark values, or closing question patterns across answers on the same account.

3. **Hemingway Technical Style (海明威文风硬核技术白描)**:
   - **Cold Factual Realism**: Open with direct physical and machine reality (exact timestamp like 凌晨三点, blinking terminal cursor, fan acoustic noise, compiler panics, exact memory or token limits).
   - **Iceberg Principle (冰山法则)**: State visible operational facts, concrete terminal outputs, and mechanical mechanisms (e.g. database row locks, TCP retransmissions, test assertions). Eliminate abstract philosophical speculation and corporate jargon.
   - **Sentence Rhythm & Variance**: Enforce sentence length variation (CV >= 0.35) by interspersing ultra-short punchy declarative clauses with precise engineering statements.

4. **Question Deduplication Gate (唯一回答门禁)**:
   - Zhihu strictly allows only ONE answer per question per account.
   - Automated question selectors must cross-reference `logs/run.jsonl` (published answers with status=ok) and queued drafts to exclude previously answered questions. Picking an answered question overwrites existing content or fails when locating the composer.

5. **DraftJS & Synthetic Paste Pipeline (输入法合成事件门禁)**:
   - Zhihu composer interfaces (answers, comments, and thoughts) use Draft.js `contenteditable`.
   - Direct CDP text insertion (`Input.insertText` / `cmux browser type`) modifies DOM text without committing to React component state, leaving the submit button permanently disabled.
   - Reliable automation must click the editor to mount toolbars, then dispatch a synthetic `ClipboardEvent('paste')` populated with `DataTransfer('text/plain')`.
   - Verification of comments must query `/api/v4/comment_v5/answers/{aid}/root_comment` for author `url_token` rather than relying on ephemeral DOM disappearance.

6. **Anti-Crawler zse-ck Challenge Protocol (动态风控防爬静置原则)**:
   - When evaluating browser state via cmux, if `document.readyState === 'loading'` and `document.body.innerText === ''`, the tab has triggered an asynchronous `zse-ck` challenge or SPA hydration stall.
   - Enforce a strict 25-minute quiet period with zero automated reloads, zero clicks, and zero polling API calls to allow the challenge to resolve without escalating to visual captcha or IP throttling.

7. **Three-Tier Evidence Standard (三级证据门禁)**:
   - **Tier 1 (Official Documentation)**: Verified vendor specs and release notes.
   - **Tier 2 (Reproducible Benchmarks)**: Backed by real execution logs on disk. Any specific number (latency in seconds, token counts, pricing, speedup) must have a corresponding log. Never synthesize pseudo-precise metrics (e.g. "18.2秒", "71% 成功率").
   - **Tier 3 (Qualitative Observations)**: When exact measurement is absent, state findings qualitatively ("明显卡顿", "调用成本显著降低") rather than fabricating numbers.

8. **Publishing Cadence Guard**:
   - Daily answer limit: 1-3 per day (paced across golden windows).
   - Minimum interval gap: Strictly >= 4 hours between answers.
   - Midnight blackout: 00:00–07:00 CST forbidden.
   - Cold-start window: The first 2 hours after publishing determine algorithmic survival.

9. **Monetization Channel Physical Separation**:
   - **致知计划 (Traffic Share)**: Requires Lv4+, 100+ followers, quality score ≥ 3,000. Strictly forbids affiliate cards ("好物推荐") or consultation cards. Maintain 80% pure technical answers.
   - **好物推荐 (Affiliate CPS)**: Dedicated 20% product recommendation answers.
   - **付费咨询 (1-on-1 Consultation)**: Unlocked at Lv3. Peer debugging and configuration guidance (¥39-¥69).
   - **Lightweight Digital Assets**: Self-developed script packs and checklists (¥19-¥39). Assets must physically exist.

10. **Anxiety-to-Solution Conversion Rule (借势破圈反焦虑与解法变现)**:
    - High-traffic industry anxiety questions ("Will AI replace programmers?", "Job market crash for juniors") attract massive impressions but carry severe risks if handled purely as emotional venting.
    - Pure anxiety selling is penalized by Zhihu quality models (lowering 致知计划 revenue), yields negligible bookmark/favorite rates, and destroys peer-developer trust.
    - The winning conversion framework: **Open by acknowledging the macro anxiety -> Shatter vague fear with cold, detailed engineering realities (system crashes, concurrency deadlocks, responsibility boundaries, AST syntax trees) -> Deliver reproducible solutions (small unit test suites, Git diff audits, lightweight toolkits)**. Topic traffic drives the impressions; calm engineering certainty drives bookmarks, follows, and consulting conversions.

11. **Vertical Domain Purity & Anti-Dilution Gate (赛道纯度与防人设撕裂门禁)**:
    - Maintain strict domain purity for the technical developer persona (大三独立开发者、终端实测).
    - Strictly prohibit drifting into unrelated consumer verticals (e.g., parenting/mom content, lifestyle hacks, generic resume tips, finance speculation). Cross-vertical posts destroy algorithm topic clustering and trigger instant un-follows.
    - Career/job topics are permitted ONLY at the hard-core technical intersection: real code reading vs bloated tutorial projects, AST inspection, unit test boundary assertions, and sandbox debugging—never generic HR interview clichés or motivational advice.

12. **SPA Navigation & Process Isolation (SPA 极速跳转与进程解释器隔离)**:
    - In browser automation via `cmux`, avoid calling blocking `cmux browser goto <url>` on SPA web pages. The CLI command waits for page network-idle / domcontentloaded events, which on Zhihu frequently delay or timeout (>45s) due to background analytics or long-lived polling.
    - Navigate using in-session script evaluation: `eval "location.href = '<url>'; 'ok'"` to achieve instant (0.1s) redirection.
    - In automation scripts spawning child CLI subprocesses (e.g. calling `guard.py` from `engage.py` or `runner.py`), never hardcode `"python3"`. Always use `sys.executable` to guarantee that child processes inherit the validated runtime environment and avoid invoking broken or mismatched system Python wrappers.

13. **CS Fundamentals & Debugging Moat Architecture (计算机底层与排障硬核护城河)**:
    - Expand beyond ephemeral tooling comparisons into evergreen CS fundamentals (Operating Systems, Computer Organization, Computer Networks, and Debugging methodologies) targeting multi-thousand to ten-thousand follower questions.
    - Strictly avoid abstract academic terminology recitations and avoid unrealistic "write kernel from scratch" extremes. Ground every article in terminal physics: `strace` system calls, `/proc/<pid>/maps` virtual memory, `tcpdump -X` raw hex packet headers, micro-benchmarks demonstrating 64-byte Cache Line false sharing, `git bisect` mechanical bisection, and red-to-green unit test contract closures.

14. **Automated GitHub Open-Source Synchronization**:
    - Local skill changes are symlinked directly to the Git repository.
    - The macOS LaunchAgent (`com.kite.skill-github-sync`) watches for modifications and runs tests before committing.
    - Broken unit tests block auto-push to protect remote repository health.

## Detailed References

- `references/wilson_ranking_and_algorithm.md`: Deep dive on Wilson score interval lower bound and upvote weighting.
- `references/multi_target_feed_and_search.md`: DNN 8-objective recommendation model, bookmark weights, and long-tail SEO.
- `references/anti_ai_linter_and_fingerprint.md`: Complete de-AI lint rules, banned patterns, Hemingway prose standards, and account fingerprint avoidance.
- `references/three_tier_evidence_system.md`: The 3-Tier Evidence verification protocol.
- `references/publishing_cadence_and_antiban.md`: Publishing quotas, golden windows, zse-ck quiet protocols, and anti-ban mechanics.
- `references/monetization_and_traffic_separation.md`: Detailed revenue paths, the 80/20 physical separation rule, and anxiety conversion mechanics.

## Step-by-Step Procedure

1. **Question Selection & Scouting**:
   - Filter candidate pools to exclude already-answered questions (`run.jsonl`).
   - Target questions with high follower-to-answer ratios using `scripts/question_evaluator.py` or `selector.py`.
   - Prefer technical troubleshooting, tool comparisons, or developer workflow topics with long-tail search value.
   - When tackling high-traffic anxiety questions, ensure the angle allows for an engineering-backed solution.

2. **Drafting Answer**:
   - Open with the Golden First 100 Words: direct verdict, version, environment.
   - Apply Hemingway technical prose: lean declarative sentences, cold physical/terminal realism, micro-paragraphs (<=3 sentences), zero corporate buzzwords.
   - Mix single-sentence declarations with 2-3 sentence technical context to prevent uniform paragraph structure warnings.
   - Maintain 800–2,500 words with H2/H3 headings, code blocks, and 2-3 genuine screenshots.
   - Adhere strictly to the 3-Tier Evidence Standard.

3. **Running Linter**:
   - Execute `python3 scripts/lint.py <draft_path>`.
   - Fix all hard-ban violations, excessive bold density (>8%), or uniform paragraph lengths.

4. **Checking Cadence**:
   - Run `python3 scripts/guard.py check`. Ensure `allowed: true` and current time is outside midnight blackout.

5. **Publishing & Recording**:
   - Publish through web or automated injection using `ClipboardEvent('paste')` on DraftJS editors.
   - Use `location.href` via eval rather than blocking CLI `goto` for SPA navigation.
   - If `zse-ck` loading state is encountered, observe the mandatory 25-minute quiet period before retrying.
   - Verify comment/thought submissions via platform API (`/api/v4/comment_v5/...`).
   - Log timestamp: `python3 scripts/guard.py record-answer`.

6. **Synchronize Skill Updates**:
   - When modifying rules, scripts, or references, changes are automatically pushed to GitHub by `com.kite.skill-github-sync` daemon upon test pass, or via `sync-skills`.

## Pitfalls

- **Do not post pure anxiety without concrete solutions**: Pure venting or doom-mongering earns impressions but zero bookmarks and kills consulting credibility. Always anchor anxiety topics with reproducible terminal commands, test assertions, or architecture diagrams.
- **Do not drift into non-technical verticals**: Mixing parenting, general lifestyle, or HR resume tropes into a developer account shatters account topic clustering and drives away core technical followers.
- **Do not make every paragraph 1 single sentence**: Uniform 1-sentence paragraphing triggers linter warnings for structural monotony. Interleave punchy lines with multi-sentence explanatory context.
- **Do not use blocking CLI `goto` in SPA automation**: `cmux browser goto` blocks on long-lived network streams on Zhihu SPA, causing script timeouts. Use `eval "location.href = '...'; 'ok'"` for instant navigation.
- **Do not hardcode `"python3"` in subprocess calls**: System Python may be outdated or misconfigured; always invoke `sys.executable` to inherit the current execution environment.
- **Do not teach CS fundamentals purely from textbooks**: Avoid writing answers that recite theoretical definitions without terminal verification; anchor concepts in measurable terminal outputs (syscall latencies, hex packet offsets, CPU cache line timings).
- **Do not select already-answered questions**: Zhihu strictly permits only one answer per question per account. Automated selectors must filter candidates against `run.jsonl` to prevent overwriting existing answers or throwing composer errors.
- **Do not rely on CDP type/insertText for DraftJS composers**: Synthetic `ClipboardEvent('paste')` with `DataTransfer('text/plain')` is mandatory to trigger React internal state; raw typing leaves submit buttons disabled. Verify submissions via `/api/v4/comment_v5/answers/{aid}/root_comment` rather than ephemeral DOM nodes.
- **Do not spam reload during zse-ck challenges**: When the page enters `readyState === 'loading'` with empty body, hammering with reloads triggers severe WAF blocking. Wait 25 minutes quietly for the token to settle.
- **Do not fabricate benchmark numbers**: Synthetic numbers like "提升了 3.8 倍" without real logs will be dismantled by Zhihu technical readers.
- **Do not mix affiliate cards into 致知计划 answers**: Disqualifies the answer from traffic revenue share entirely.
- **Do not use repetitive answer openings**: Wali/Wukong flags cross-answer templated patterns as automated AI farms.
- **Do not break unit tests during skill editing**: Automated GitHub push executes `python3 -m unittest` pre-flight gate; broken tests abort auto-push to prevent pushing failing code.

## Verification

- Linter passes clean: `python3 scripts/lint.py <draft>` exits with code 0.
- Pacing gate confirms: `python3 scripts/guard.py check` returns `\"allowed\": true`.
- Every quoted metric resolves to an official source or reproducible test.
- Unit tests pass: `python3 -m unittest discover -s tests -p \"test_*.py\"` exits with code 0.
