#!/usr/bin/env python3
"""Zhihu Question Traffic & Potential Evaluator.

Evaluates question potential using follower-to-answer ratio, view density,
and Wilson score cold-start viability.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any


def evaluate_question(
    followers: int,
    answers: int,
    views: int,
    title: str = "",
) -> dict[str, Any]:
    """Calculate potential score (0 - 100) and recommendation tier."""
    notes: list[str] = []

    # 1. Supply-demand ratio (followers per answer)
    # Higher ratio means more demand than supply
    if answers <= 0:
        ratio = float(followers)
        answers_safe = 1
    else:
        ratio = followers / answers
        answers_safe = answers

    # 2. View density (views per answer)
    view_density = views / answers_safe

    # 3. Base score components
    # A: Ratio score (max 40 pts)
    # Target: ratio >= 30 is great, ratio >= 50 is outstanding
    ratio_score = min(40.0, (ratio / 30.0) * 30.0)

    # B: Volume score (max 30 pts)
    # Questions with 500 - 50,000 followers are sweet spots
    if followers < 50:
        vol_score = 5.0
        notes.append("关注人数过少 (<50)，缺乏基本初始读者流量")
    elif followers < 300:
        vol_score = 15.0
        notes.append("小体量潜力问题，竞争较小但长尾起量较慢")
    elif followers <= 5000:
        vol_score = 30.0
        notes.append("黄金中体量问题 (300-5000)，插队容易且有足够曝光")
    elif followers <= 20000:
        vol_score = 25.0
        notes.append("大体量问题，头部答案票数较高，需要高密度证据破局")
    else:
        vol_score = 18.0
        notes.append("超级大热门，老答案固化严重，威尔逊插队难度极高")

    # C: Competition penalty / reward (max 30 pts)
    # Answers count: 5-50 is optimal; >200 is heavily saturated
    if answers < 3:
        comp_score = 25.0
        notes.append("新问题/极少回答，有首位优势但需观察热度发酵")
    elif answers <= 40:
        comp_score = 30.0
        notes.append("适度竞争区间 (3-40 回答)，易通过高赞同比进入前列")
    elif answers <= 120:
        comp_score = 20.0
        notes.append("较多回答竞争，需确保首屏前 100 字直接亮出高赞结论")
    else:
        comp_score = 10.0
        notes.append("严重饱和 (>120 回答)，长尾搜素依然有效但冷启动阻力大")

    total_score = round(ratio_score + vol_score + comp_score, 1)

    # Tier mapping
    if total_score >= 80:
        tier = "S (极度推荐：供需比极佳，威尔逊插队极易)"
    elif total_score >= 65:
        tier = "A (推荐介入：流量充沛，质量答案易脱颖而出)"
    elif total_score >= 50:
        tier = "B (可备选：属于常规长尾，适合垂直度积累)"
    else:
        tier = "C (不建议：供需失衡或竞争严重过饱和)"

    return {
        "title": title,
        "score": total_score,
        "tier": tier,
        "followers": followers,
        "answers": answers,
        "views": views,
        "follower_to_answer_ratio": round(ratio, 2),
        "views_per_answer": int(view_density),
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Zhihu Question Potential")
    parser.add_argument("--followers", "-f", type=int, required=True, help="Number of question followers")
    parser.add_argument("--answers", "-a", type=int, required=True, help="Number of existing answers")
    parser.add_argument("--views", "-v", type=int, default=0, help="Total view count of question")
    parser.add_argument("--title", "-t", default="", help="Question title string")
    args = parser.parse_args()

    res = evaluate_question(args.followers, args.answers, args.views, args.title)

    print("=" * 60)
    print(" Zhihu Question Traffic Potential Report")
    print("=" * 60)
    if res["title"]:
        print(f"[*] 评估问题: {res['title']}")
    print(f"[*] 综合潜力评分: {res['score']} / 100")
    print(f"[*] 推荐评级: {res['tier']}")
    print(f"[*] 供需比 (关注者/回答数): {res['follower_to_answer_ratio']}")
    if res["views"] > 0:
        print(f"[*] 平均每答曝光 (Views/Answer): {res['views_per_answer']}")

    print("\n[*] 机制推论与诊断:")
    for note in res["notes"]:
        print(f"  - {note}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
