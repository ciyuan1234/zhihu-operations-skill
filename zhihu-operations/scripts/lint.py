#!/usr/bin/env python3
"""Zhihu answer text & anti-AI linter.

Enforces developer voice, hard banned phrases, AI density checks,
and paragraph structure rules.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from typing import Any

# Hard bans: triggers instant failure
HARD_BANS = [
    (r"不是[^。\n]{0,20}，?\s*而是", "§2 不是A而是B（经典二元说教句式）"),
    (r"并非[^。\n]{0,20}，?\s*而是", "§2 并非A而是B（经典二元说教句式）"),
    (r"与其说[^。\n]{0,25}，?\s*不如说", "§2 与其说不如说（机械对比）"),
    (r"综上所述|总而言之|总的来说", "§2 总结套话（公文体/AI腔）"),
    (r"值得注意的是|众所周知|不难发现|不可否认", "§2 空转过渡套话"),
    (r"让我们拭目以待|让我们一起|一起来看看", "§2 舞台腔"),
    (r"这背后反映的是|深层来看|追根究底|究其本质", "§2 强行升华与抽象拔高"),
    (r"作为一名|从业\s*\d+\s*年来", "§2 借身份压人说教"),
    (r"在[^。\n]{0,15}的今天|随着[^。\n]{0,15}的发展", "§2 宏大叙事开头套话"),
    (r"你怎么看|你怎么评价|欢迎在?评论区|对此[，,]?\s*你", "§2 反问求互动"),
    (r"赋能|抓手|闭环|底层逻辑|颗粒度|心智[模型]?|降维打击|碾压|吊打|封神", "§2 互联网黑话/夸大营销"),
    (r"颠覆性|革命性|里程碑意义|未来可期|前景广阔|潜力巨大", "§2 夸大公关辞藻"),
    (r"深入探讨|深度剖析|全面解读|全方位把握", "§2 空洞公文词汇"),
    (r"至关重要|举足轻重|不可或缺", "§2 溢美辞藻"),
    (r"实际上，?首先|首先[，,].{0,30}其次[，,].{0,30}最后[，,]", "§2 机械三段式结构"),
    (r"🚀|💡|✅|❌|→|⬇️|🔥|📈", "§4 符号墙/营销箭头清单装饰"),
    (r"(?m)^- \*\*[^*\n]{1,20}[:：]", "§2 加粗标签排比列表"),
    (r"希望这篇(回答|内容)?(能|对)?(帮|有用)|希望能帮到|欢迎指正|欢迎交流", "§2 谄媚客套套话"),
    (r"我希望能|如果觉得有用|点个赞|求赞|求三连|关注我", "§2 乞赞乞关注"),
]

# Soft warnings
SOFT_WARNS = [
    (r"——", "§2 破折号过多", 2),
    (r"！{2,}|!{2,}", "§2 连续感叹号", 0),
    (r"首先[，,]|其次[，,]", "§2 首先其次过度使用", 1),
    (r"不仅[^。\n]{0,25}，?\s*(而且|更|也)", "§2 不仅而且递进排比", 1),
    (r"其实[^。\n]{0,10}不是[^。\n]{0,15}，(而)?是", "§1 变体不是而是句式", 0),
]

SPECIFIC_FIGURES = re.compile(
    r"\d+(?:\.\d+)?%|\$\d+|\d+[KkMm]?\s*(?:token|美元|美金|次|万|K|MB|GB|TB|ms|s)|v?\d+\.\d+(?:\.\d+)?|\d{4}\s*年"
)

LEAD_RE = re.compile(r"^\s*(20\d{2}年\d{1,2}月\d{1,2}日)?\s*先(给|说|摆|纠|讲|道)")


def count_sentences(paragraph: str) -> int:
    parts = [p for p in re.split(r"[。！？!?；;]", paragraph) if p.strip()]
    return len(parts) if parts else (1 if paragraph.strip() else 0)


def check_ai_density(text: str) -> list[str]:
    warns: list[str] = []
    chars = len(re.sub(r"\s", "", text)) or 1

    bold_chars = sum(len(m) for m in re.findall(r"\*\*([^*]+)\*\*", text))
    if bold_chars / chars > 0.08:
        warns.append(f"§5 加粗文字占比 {bold_chars / chars:.1%} > 8% (营销清单体特征)")

    list_items = len(re.findall(r"(?m)^\s*[-*]\s+|\s*\d+[.、]\s+", text))
    if list_items > 8:
        warns.append(f"§5 列表项多达 {list_items} 条 (超过 8 条易显模板化)")

    headings = len(re.findall(r"(?m)^#{2,3}\s", text))
    if headings > 5:
        warns.append(f"§5 小标题数量 {headings} 个 (超过 5 个骨架感过强)")

    paras = [p.strip() for p in text.split("\n") if p.strip() and not p.strip().startswith(("#", "-", "*"))]
    if len(paras) >= 6:
        counts = [count_sentences(p) for p in paras]
        if len(set(counts)) <= 1:
            warns.append(f"§5 所有段落结构均全为 {counts[0]} 句，排版过于整齐机械")

    return warns


def check_fingerprint(path: str, text: str) -> list[str]:
    warns: list[str] = []
    if not path or not os.path.exists(path):
        return warns

    parent = os.path.dirname(os.path.abspath(path))
    siblings = [f for f in glob.glob(os.path.join(parent, "*.md")) if os.path.abspath(f) != os.path.abspath(path)]
    if len(siblings) < 4:
        return warns

    if LEAD_RE.match(text):
        same_count = 0
        for f in siblings:
            try:
                with open(f, encoding="utf-8") as fp:
                    if LEAD_RE.match(fp.read()):
                        same_count += 1
            except Exception:
                pass
        if same_count >= 4:
            warns.append(f"§5 跨答案指纹: 「日期+先说结论」开头在同目录下已被 {same_count + 1} 篇使用")

    lines = [p for p in text.strip().split("\n") if p.strip()]
    if lines:
        tail = lines[-1]
        if re.match(r"^(你们|大家)", tail) and re.search(r"[？?]$", tail):
            same_tail = 0
            for f in siblings:
                try:
                    with open(f, encoding="utf-8") as fp:
                        sub_lines = [p for p in fp.read().strip().split("\n") if p.strip()]
                        if sub_lines and re.match(r"^(你们|大家)", sub_lines[-1]) and re.search(r"[？?]$", sub_lines[-1]):
                            same_tail += 1
                except Exception:
                    pass
            if same_tail >= 3:
                warns.append(f"§5 跨答案指纹: 「你们…吗？」收尾在同账号已被 {same_tail + 1} 篇使用")

    return warns


def check_text(text: str, file_path: str = "") -> dict[str, Any]:
    fails: list[str] = []
    warns: list[str] = []
    notes: list[str] = []

    # Strip image placeholders <!--img:...-->
    clean = re.sub(r"<!--img:[^>]*-->\n?", "", text)

    # Hard bans
    for pat, label in HARD_BANS:
        for m in re.finditer(pat, clean):
            ctx = clean[max(0, m.start() - 12): m.end() + 12].replace("\n", " ")
            fails.append(f"{label} -> 「…{ctx}…」")

    # Soft warnings
    for pat, label, limit in SOFT_WARNS:
        matches = len(re.findall(pat, clean))
        if matches > limit:
            warns.append(f"{label}: 发现 {matches} 处 (警戒阈值 {limit})")

    # Word count
    chars = len(re.sub(r"\s", "", clean))
    notes.append(f"纯文本字数: {chars} 字 (致知计划底线 500 字，推荐 800-2000 字)")
    if chars < 400:
        fails.append(f"§1 字数严重不足: 纯字数 {chars} < 400（缺乏论述深度与权威感）")

    # AI density check
    warns.extend(check_ai_density(clean))

    # Cross-answer fingerprint check
    if file_path:
        warns.extend(check_fingerprint(file_path, clean))

    # Specific evidence figures
    spec = len(SPECIFIC_FIGURES.findall(clean))
    notes.append(f"具体数值/版本证据: {spec} 处")
    if spec < 3:
        warns.append(f"§3 缺乏实测数据: 仅发现 {spec} 处具体版本/时间/开销参数 (建议 >=3 处以满足三级证据链)")

    return {
        "passed": len(fails) == 0,
        "fails": fails,
        "warns": warns,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Zhihu Answer Text Linter")
    parser.add_argument("path", nargs="?", help="Answer markdown file path")
    parser.add_argument("--text", help="Raw answer text string")
    args = parser.parse_args()

    if args.text:
        content = args.text
        fpath = ""
    elif args.path:
        if not os.path.exists(args.path):
            print(f"Error: file '{args.path}' not found", file=sys.stderr)
            return 2
        fpath = args.path
        with open(args.path, encoding="utf-8") as f:
            content = f.read()
    else:
        parser.print_help()
        return 2

    res = check_text(content, fpath)

    print("=" * 60)
    print(" Zhihu Answer Linter Report")
    print("=" * 60)
    for n in res["notes"]:
        print(f"[*] {n}")

    if res["warns"]:
        print("\n[!] WARNINGS (软警告建议改进):")
        for w in res["warns"]:
            print(f"  - {w}")

    if res["fails"]:
        print("\n[x] FAILURES (硬性阻断必须修正):")
        for f in res["fails"]:
            print(f"  - {f}")
        print("\nResult: LINT FAILED")
        return 1
    else:
        print("\nResult: LINT PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
