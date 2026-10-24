---
name: zhihu-operations
description: "Operate Zhihu technical answers, anti-AI lint and cadence."
version: 1.11.0
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
- Checking publishing cadence and intervals (`scripts/guard.py`) to prevent spam flags (daily cap 1-2, minimum 4-6h gap, midnight blackout 00:00-07:00 CST).
- Scoring potential questions (`scripts/question_evaluator.py`, `selector.py`) to target high-traction, high-search-value answer candidates.
- Scouting questions and fetching metrics without DOM stalls via authenticated in-session `fetch('/api/v4/search_v3?t=question&q=...')`.
- Filtering out already-answered questions from candidate pools to prevent accidental answer overwrites.
- Automating DraftJS editor input (answers, comments, and thoughts) using native `ClipboardEvent('paste')` synthesis.
- Executing fast browser navigation via in-session `eval "location.href = '...'; 'ok'\"` to bypass blocking CLI goto timeouts on heavy SPAs.
- Handling dynamic anti-crawler `zse-ck` challenges with mandatory 25-minute quiet cooldowns.
- Applying the 3-Tier Evidence Standard (official docs -> reproducible benchmarks -> qualitative observations) to eliminate fabricated metrics.
- Structuring monetization funnels while strictly keeping 致知计划 (pure traffic revenue) and affiliate cards physically separated.
- Synchronizing local skill updates to the open-source GitHub repository (`ciyuan1234/zhihu-operations-skill`).
- Don't use for: Salt fiction/storytelling, generic marketing ad spam, or paid upvote/shill rings (banned by platform).

## Prerequisites

- Python 3.9+ (Python 3.10+ recommended) for linting, cadence guard, and evaluation scripts.
- Platform account: Zhihu account (`zhihu.com`).
- GitHub repository: `https://github.com/ciyuan1234/zhihu-operations-skill` (`social-media/zhihu-operations`).

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
   - **Micro-Paragraphs & Single-Newline Markdown Linebreak Pitfall**: Keep paragraphs under 3 sentences. `lint.py` treats semicolons (`；;`) and exclamation marks (`!！？`) as sentence terminators across raw markdown without stripping code blocks or inline backticks. Avoid semicolons in text lists. In code blocks, wrap multi-clause statements across multiple lines. **Critical Linter Parsing Rule**: `lint.py` splits paragraphs via `text.split("\n")` (single newline), NOT `\n\n`. If a draft soft-wraps sentences with `\n` inside a paragraph, each line is parsed as an independent 1-sentence paragraph, triggering `[WARN] §5 段落句数几乎全为 1 句，结构过于整齐`. Markdown paragraphs must be formatted as single continuous strings without embedded newlines, separated strictly by blank lines (`\n\n`).
   - **Paragraph Sentence Count Diversity Gate (`len(set(counts)) >= 3`)**: While paragraphs must stay `<= 3` sentences, making all paragraphs 1 sentence or having only two distinct paragraph lengths triggers `[WARN] §5 段落句数几乎全为 X 句，结构过于整齐` (template monotony). Interleave 1-sentence punchy claims, 2-sentence technical context, and 3-sentence analytical paragraphs so that `set(counts)` contains at least 3 distinct integers (e.g. `{1, 2, 3}`).
   - **Subheading Hierarchy Compression**: Cap H2/H3 subheadings at `<= 5` across the entire answer (e.g. `## 一` to `## 五`). More than 5 subheadings triggers `[WARN] §5 小标题 >5 骨架感强`. When decomposing sub-points, use bold inline lead-ins (`**核心死穴一：...**`) rather than `###` subheadings.
   - **Definitive Stance Gate**: Include clear evaluative stance words (specifically from the linter whitelist: `是倒退`, `不推荐`, `慎买`, `别买`, `没必要`, `不划算`, `最贵`, `坑`, `跑偏`, `不够`, `不诚实`, `最强`, `天花板`). Answers lacking these trigger `[WARN] §3 未检测到明确立场词，检查是否以「各有优劣」收尾`.
   - **Concrete Specificity & Version Anchors Gate (`§3 具体数字/版本/时间 ≥ 3`)**: Answers must include at least 3 verified, concrete anchors matching `SPECIFIC` regex (`\d+(?:\.\d+)?%|\$\d+|\d+[KkMm]?\s*(?:token|美元|美金|次|万|K)|v?\d+\.\d+(?:\.\d+)?|\d{4}\s*年`)—such as specific library/engine versions (`v8.0`, `MySQL 8.0.36`), testing years (`2026 年`), percentages (`95%`), or scale metrics (`10 万次`).
   - **Absolute Phrase Bans**: Ban rhetorical binary contrasts ("不是A而是B", "并非……而是……"), mechanical transition labels ("首先/其次/最后", "总而言之"), platform clichés ("作为一名程序员", "在AI飞速发展的今天", "在...的今天"), marketing jargon (strictly ban "闭环", "底层逻辑", "颗粒度", "赋能", "降维打击", "碾压", "心智负担"), hyperbole ("颠覆性", "颠覆了什么", "史诗级"), adulatory praise words (strictly ban `至关重要|举足轻重|不可或缺` under `§2 溢美`), and pseudo-philosophical AI template phrases (strictly ban `微观物理真相|物理真相|铁血契约|工业级军规|阿喀琉斯之踵|判决四重奏|教科书式谎言|全行业讨论频次最高|基石底座`). Express trade-offs affirmatively ("不能只盯着……更要深入排查……", "跳出……的局限，转为……") rather than negation antithesis.
   - **Cross-Answer Deduplication & Fingerprinting**: Never reuse identical opening formulas ("日期 + 先说结论"), benchmark values, formulaic comment structures, or closing question patterns across answers on the same account.

3. **Topic Quarantine & AI Batch-Generation Risk Gate (选题避险与防批量AI归因门禁)**:
   - **Generic AI Coding Tool Listicle Quarantine**: Platform NLP classifiers heavily monitor generic topics ("哪些AI编程工具更好用", "Codex体验真有那么好吗", "普通人用Codex有什么用", "Cursor/Claude选型对比", "如何充值/降低费用"). Across 38 published answers, 7 were collapsed with `可能包含 AI 创作内容`, and 100% of the collapsed answers belonged to this generic tool review cluster.
   - **Zero-Collapse on CS Fundamentals**: Deep computer science and engineering topics (OS memory mapping, Linux CFS/BBR, MySQL MVCC version chains, network protocol mechanics) had a 0% collapse rate. All future pipeline content must anchor strictly in CS fundamentals and hard engineering reality.
   - **Length & Density Bounding (2,000–3,500 Words)**: Uncapped, encyclopedic generation (6,000–8,500 words) triggers template and artificial inflation flags. Anchor articles strictly in the lean, dense 2,000–3,500 word sweet spot.
   - **Throttled Natural Cadence**: Cap daily publishing at 1-2 answers/day (with >=4-6h gaps) to eliminate machine-like temporal clustering.

4. **Hemingway Technical Style (海明威文风硬核技术白描)**:
   - **Cold Factual Realism**: Open with direct physical and machine reality (exact timestamp like 凌晨三点, blinking terminal cursor, fan acoustic noise, compiler panics, exact memory or token limits).
   - **Iceberg Principle (冰山法则)**: State visible operational facts, concrete terminal outputs, and mechanical mechanisms (e.g. database row locks, TCP retransmissions, test assertions). Eliminate abstract philosophical speculation and corporate jargon.
   - **Sentence Rhythm & Variance**: Enforce sentence length variation (CV >= 0.35) by interspersing ultra-short punchy declarative clauses with precise engineering statements.

5. **Question Deduplication Gate (唯一回答门禁)**:
   - Zhihu strictly allows only ONE answer per question per account.
   - Automated question selectors must cross-reference `logs/run.jsonl` (published answers with status=ok) and queued drafts to exclude previously answered questions.

6. **DraftJS & Synthetic Paste Pipeline (输入法合成事件门禁)**:
   - Zhihu composer interfaces (answers, comments, and thoughts) use Draft.js `contenteditable`.
   - Direct CDP text insertion modifies DOM text without committing to React component state, leaving the submit button permanently disabled.
   - Reliable automation must click the editor to mount toolbars, then dispatch a synthetic `ClipboardEvent('paste')` populated with `DataTransfer('text/plain')`.
   - Verification of comments must query `/api/v4/comment_v5/answers/{aid}/root_comment` for author `url_token` rather than relying on ephemeral DOM disappearance.

7. **Anti-Crawler zse-ck Challenge Protocol (动态风控防爬静置原则)**:
   - When evaluating browser state via cmux, if `document.readyState === 'loading'` and `document.body.innerText === ''`, the tab has triggered an asynchronous `zse-ck` challenge or SPA hydration stall.
   - Enforce a strict 25-minute quiet period with zero automated reloads, zero clicks, and zero polling API calls to allow the challenge to resolve without escalating to visual captcha or IP throttling.

8. **Three-Tier Evidence Standard (三级证据门禁)**:
   - **Tier 1 (Official Documentation)**: Verified vendor specs and release notes.
   - **Tier 2 (Reproducible Benchmarks)**: Backed by real execution logs on disk. Any specific number must have a corresponding log. Never synthesize pseudo-precise metrics.
   - **Tier 3 (Qualitative Observations)**: When exact measurement is absent, state findings qualitatively ("明显卡顿", "调用成本显著降低") rather than fabricating numbers.

9. **Publishing Cadence Guard**:
   - Daily answer limit: 1-2 per day (paced across golden windows).
   - Minimum interval gap: Strictly >= 4 hours between answers.
   - Midnight blackout: 00:00–07:00 CST forbidden.
   - Cold-start window: The first 2 hours after publishing determine algorithmic survival.

10. **Monetization Channel Physical Separation**:
    - **致知计划 (Traffic Share)**: Requires Lv4+, 100+ followers, quality score ≥ 3,000. Strictly forbids affiliate cards or consultation cards. Maintain 80% pure technical answers.
    - **好物推荐 (Affiliate CPS)**: Dedicated 20% product recommendation answers.
    - **付费咨询 (1-on-1 Consultation)**: Unlocked at Lv3. Peer debugging and configuration guidance (¥39-¥69).
    - **Lightweight Digital Assets**: Self-developed script packs and checklists (¥19-¥39). Assets must physically exist.

11. **Anxiety-to-Solution Conversion Rule (借势破圈反焦虑与解法变现)**:
    - High-traffic industry anxiety questions attract massive impressions but carry severe risks if handled purely as emotional venting.
    - Pure anxiety selling is penalized by Zhihu quality models and yields negligible bookmarks.
    - The winning conversion framework: Open by acknowledging macro anxiety -> Shatter vague fear with cold, detailed engineering realities -> Deliver reproducible solutions.

12. **Vertical Domain Purity & Anti-Dilution Gate (赛道纯度与防人设撕裂门禁)**:
    - Maintain strict domain purity for the technical developer persona.
    - Strictly prohibit drifting into unrelated consumer verticals.
    - Career/job topics are permitted ONLY at the hard-core technical intersection.

13. **In-Session API Scouting & SPA Navigation (API 极速调研与 SPA 避坑)**:
    - In browser automation via `cmux`, avoid calling blocking `cmux browser goto <url>` on SPA web pages.
    - Navigate using in-session script evaluation: `eval "location.href = '<url>'; 'ok'\"` to achieve instant redirection.
    - Scout questions or metrics by evaluating `fetch('/api/v4/search_v3?t=question&q=...')` directly inside the authenticated browser tab.
    - In automation scripts spawning child CLI subprocesses, never hardcode `python3`. Always use `sys.executable`.
    - **Surface Isolation & Deep Administrative URL Avoidance**: Never navigate the active runner browser tab away from standard domain URLs (like `https://www.zhihu.com/`) to deep internal administrative or moderation URLs (such as `/community/messages/...`). Internal administrative routes can drop frontend authentication context and redirect the surface to `/signin`, causing background runner operations to stall.

14. **CS Fundamentals & Debugging Moat Architecture (计算机底层与排障硬核护城河)**:
    - Expand into evergreen CS fundamentals (Operating Systems, Computer Organization, Networks, and Debugging methodologies) targeting high-follower questions.
    - Ground every article in terminal physics: system calls, virtual memory maps, raw packet headers, cache line timings, and unit test assertions.

15. **Automated GitHub Open-Source Synchronization**:
    - Local skill changes are symlinked directly to the Git repository.
    - The macOS LaunchAgent watches for modifications and runs tests before committing. Broken tests block auto-push.

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
   - Query candidate metrics via cmux browser `fetch('/api/v4/search_v3?...')` or evaluate with `scripts/question_evaluator.py`.
   - Target questions with high follower-to-answer ratios and evergreen technical search value in CS fundamentals.

2. **Drafting Answer**:
   - Open with the Golden First 100 Words: direct verdict, version, environment.
   - Apply Hemingway technical prose: lean declarative sentences, cold physical/terminal realism, micro-paragraphs (<=3 sentences), zero corporate buzzwords.
   - Keep each paragraph formatted as a single continuous line without internal `\n` linebreaks, separated strictly by blank lines (`\n\n`).
   - Cap subheadings at `<= 5` to avoid rigid outline feel; use bold lead-in phrases (`**核心死穴一：...**`) for sub-points.
   - Avoid semicolons inside lists or explanations to prevent accidental sentence splitting in linting.
   - Wrap compound statements or loops in code blocks across multiple lines to prevent semicolons and `!=` from inflating sentence count.
   - Mix single-sentence declarations, 2-sentence context, and 3-sentence analyses to satisfy paragraph sentence count diversity (`len(set(counts)) >= 3`).
   - Plant explicit stance vocabulary (`是倒退`, `不推荐`, `坑`, `跑偏`, `没必要`) to ground the engineering verdict.
   - Include at least 3 concrete anchors matching `SPECIFIC` regex to satisfy the specificity gate.
   - Maintain 2,000–3,500 words with H2 headings, code blocks, and 2-3 genuine screenshots.
   - Adhere strictly to the 3-Tier Evidence Standard.

3. **Running Linter**:
   - Execute `python3 scripts/lint.py <draft_path>` and verify dry-run HTML blocks via `injector.py --dry-run`.
   - Fix all hard-ban violations, excessive bold density (>8%), uniform paragraph lengths, missing stance markers, or missing specific anchors.

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

- **Do not soft-wrap markdown lines within paragraphs with `\n`**: `lint.py` parses paragraphs by splitting on single `\n`. Internal line breaks turn a single paragraph into multiple 1-sentence pseudo-paragraphs, immediately triggering `§5 段落句数几乎全为 1 句，结构过于整齐`. Format each paragraph as a single continuous string.
- **Do not write words like '不可或缺' or '至关重要'**: Triggers `§2 溢美` hard ban in `lint.py`. Use objective technical terminology like `基本前提` or `核心前提`.
- **Do not navigate the active runner browser tab to deep internal message routes**: Navigating directly to `/community/messages/...` or admin paths can break session context and redirect to `/signin`, stalling background automated execution.
- **Do not write one-line loops with semicolons and `!=` in code blocks**: `lint.py` treats raw markdown lines inside code fences as paragraphs and splits on `[。！？!?；;]`. Wrap loop clauses across multiple lines.
- **Do not make paragraph sentence lengths uniform**: Having only 1-sentence or only two distinct paragraph lengths triggers `§5 段落句数几乎全为 X 句，结构过于整齐`. You must interleave 1-sentence, 2-sentence, and 3-sentence paragraphs so that `len(set(counts)) >= 3`.
- **Do not use more than 5 subheadings**: Having `> 5` H2/H3 headers triggers `§5 小标题 >5 骨架感强`. Group sub-points under bold inline lead-ins (`**核心死穴一：...**`) rather than `###` subheadings.
- **Do not omit stance words in technical explanations**: Without explicit stance vocabulary (`是倒退`, `不推荐`, `坑`, `跑偏`, `没必要`), `lint.py` warns for lack of clear stance.
- **Do not omit concrete version/scale anchors**: A pure conceptual answer without at least 3 specific anchors triggers `§3 具体数字/版本/时间仅 X 处（目标 ≥3）`. Explicitly cite exact engine versions, testing years, or percentage benchmarks.
- **Do not publish generic AI tool comparison or ranking listicles**: High-density NLP classification zone; triggers automated batch generation flags. Stick to deep CS fundamentals (OS, Linux kernel, networks, DB engine).
- **Do not use formulaic pseudo-philosophical phrases**: Words like '微观物理真相', '铁血契约', '工业级军规', '阿喀琉斯之踵', '基石底座' form cross-article cluster fingerprints. Express mechanisms directly through code, logs, and syscalls.
- **Do not publish in bursts on the same category**: Even compliant articles trigger batch-generation clustering flags if published consecutively on the same generic topic. Interleave topics and maintain >=4-6h natural human pacing.
- **Do not inflate technical answers beyond 3,500 words with repetitive definitions**: Excessive 6,000-8,000 word encyclopedic dumps trigger batch generation and reader abandonment. Keep to lean, dense 2,000–3,500 words.
- **Do not use contrastive negation like '不是A而是B'**: Express trade-offs affirmatively without the contrast particle.
- **Do not use words containing '颠覆'**: Triggers hyperbole hard-ban. Use '机制革新' or '架构重构'.
- **Do not use buzzwords like '碾压' or '闭环'**: Triggers marketing jargon hard-ban in `lint.py`.
- **Do not post pure anxiety without concrete solutions**: Pure venting earns impressions but zero bookmarks. Always anchor anxiety topics with reproducible terminal commands, test assertions, or architecture diagrams.
- **Do not drift into non-technical verticals**: Mixing parenting or general lifestyle hacks into a developer account shatters account topic clustering.
- **Do not use blocking CLI `goto` or page reload for question scouting**: `cmux browser goto` blocks on long-lived network streams on Zhihu SPA. Evaluating `fetch('/api/v4/search_v3?t=question&q=...')` directly inside the browser returns candidate data in milliseconds.
- **Do not hardcode `python3` in subprocess calls**: Always invoke `sys.executable` to inherit the current execution environment.
- **Do not teach CS fundamentals purely from textbooks**: Anchor concepts in measurable terminal outputs (syscall latencies, hex packet offsets, CPU cache line timings).
- **Do not select already-answered questions**: Automated selectors must filter candidates against `run.jsonl`.
- **Do not rely on CDP type/insertText for DraftJS composers**: Synthetic `ClipboardEvent('paste')` with `DataTransfer('text/plain')` is mandatory to trigger React internal state.
- **Do not spam reload during zse-ck challenges**: Wait 25 minutes quietly for the token to settle.
- **Do not fabricate benchmark numbers**: Synthetic numbers without real logs will be dismantled by Zhihu technical readers.
- **Do not mix affiliate cards into 致知计划 answers**: Disqualifies the answer from traffic revenue share entirely.
- **Do not use repetitive answer openings**: Wali/Wukong flags cross-answer templated patterns as automated AI farms.
- **Do not break unit tests during skill editing**: Automated GitHub push executes `python3 -m unittest` pre-flight gate; broken tests abort auto-push.

## Verification

- Linter passes clean: `python3 scripts/lint.py <draft>` exits with code 0.
- Pacing gate confirms: `python3 scripts/guard.py check` returns `\"allowed\": true`.
- Every quoted metric resolves to an official source or reproducible test.
- Unit tests pass: `python3 -m unittest discover -s tests -p \"test_*.py\"` exits with code 0.
