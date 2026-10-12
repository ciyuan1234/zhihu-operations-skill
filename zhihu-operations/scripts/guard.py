#!/usr/bin/env python3
"""Zhihu answer publishing cadence & risk guard.

Enforces account safety limits:
- Daily post caps (1-2 answers per day)
- Minimum interval gap between answers (>= 6 hours)
- Midnight blackout (00:00 - 07:00 CST)
- Weekly post ceiling (<= 10 answers per week)
- 48h abnormal risk cooldown
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

CST = timezone(timedelta(hours=8))

MAX_DAILY_ANSWERS = 2
MAX_WEEKLY_ANSWERS = 10
MIN_GAP_HOURS = 6

BLACKOUT_START = 0  # 00:00 CST
BLACKOUT_END = 7    # 07:00 CST

GOLDEN_WINDOWS = [
    (8, 0, 9, 0, "早通勤时隙"),
    (12, 0, 13, 30, "午间摸鱼/午休时隙"),
    (20, 0, 23, 0, "晚间深度阅读主力波峰"),
]


def get_default_state_path() -> Path:
    env_path = os.getenv("ZHIHU_GUARD_STATE")
    if env_path:
        return Path(env_path)
    home_dir = Path.home() / ".hermes" / "social_state"
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir / "zhihu_guard_state.json"


def load_state(state_file: Path) -> dict:
    if not state_file.exists():
        return {
            "answers": [],
            "interactions": [],
            "cooldown_until": None,
        }
    try:
        with open(state_file, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
    data.setdefault("answers", [])
    data.setdefault("interactions", [])
    data.setdefault("cooldown_until", None)
    return data


def save_state(state_file: Path, data: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = state_file.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, state_file)


def dedupe_timestamps(stamps: list[str]) -> list[str]:
    seen: set[str] = set()
    res: list[str] = []
    for s in stamps:
        key = s.split(".")[0]
        if key not in seen:
            seen.add(key)
            res.append(s)
    return res


def parse_dt(s: str) -> datetime:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CST)
    return dt.astimezone(CST)


def check_cadence(state_file: Path, target_time: datetime | None = None) -> dict:
    now = target_time or datetime.now(CST)
    state = load_state(state_file)

    reasons: list[str] = []
    wait_seconds = 0

    state["answers"] = dedupe_timestamps(state.get("answers", []))
    answers = [parse_dt(s) for s in state["answers"]]

    # 1. Abnormal risk cooldown check
    cd_str = state.get("cooldown_until")
    if cd_str:
        cd_dt = parse_dt(cd_str)
        if now < cd_dt:
            rem = int((cd_dt - now).total_seconds())
            reasons.append(f"账号处于安全风险冷却中，解禁时间: {cd_dt.strftime('%m-%d %H:%M')}")
            wait_seconds = max(wait_seconds, rem)

    # 2. Midnight blackout check (00:00 - 07:00 CST)
    if BLACKOUT_START <= now.hour < BLACKOUT_END:
        resume = now.replace(hour=BLACKOUT_END, minute=0, second=0, microsecond=0)
        rem = int((resume - now).total_seconds())
        reasons.append(f"处于夜间禁发时段 (00:00-07:00)，预计 {resume.strftime('%H:%M')} 恢复发布")
        wait_seconds = max(wait_seconds, rem)

    # 3. Daily limit check
    today = now.date()
    todays = [n for n in answers if n.date() == today]
    if len(todays) >= MAX_DAILY_ANSWERS:
        tomorrow = datetime.combine(today + timedelta(days=1), datetime.min.time(), CST) + timedelta(hours=BLACKOUT_END)
        rem = int((tomorrow - now).total_seconds())
        reasons.append(f"今日已发布 {len(todays)} 条回答，已达日上限 ({MAX_DAILY_ANSWERS} 条/天)")
        wait_seconds = max(wait_seconds, rem)

    # 4. Minimum interval gap check
    if answers:
        last = max(answers)
        gap_limit = timedelta(hours=MIN_GAP_HOURS)
        next_allowed = last + gap_limit
        if now < next_allowed:
            rem = int((next_allowed - now).total_seconds())
            reasons.append(f"距上条发布不足 {MIN_GAP_HOURS} 小时 (上条: {last.strftime('%m-%d %H:%M')})，需等待至 {next_allowed.strftime('%m-%d %H:%M')}")
            wait_seconds = max(wait_seconds, rem)

    # 5. Weekly limit check
    week_start = today - timedelta(days=today.weekday())
    this_week = [n for n in answers if n.date() >= week_start]
    if len(this_week) >= MAX_WEEKLY_ANSWERS:
        reasons.append(f"本周已发布 {len(this_week)} 条回答，已达周上限 ({MAX_WEEKLY_ANSWERS} 条/周)")

    # Find matching golden window
    current_golden = None
    for sh, sm, eh, em, label in GOLDEN_WINDOWS:
        start_time = now.replace(hour=sh, minute=sm, second=0)
        end_time = now.replace(hour=eh, minute=em, second=0)
        if start_time <= now <= end_time:
            current_golden = label
            break

    return {
        "allowed": len(reasons) == 0,
        "reasons": reasons,
        "wait_seconds": wait_seconds,
        "today_count": len(todays),
        "week_count": len(this_week),
        "golden_window": current_golden,
        "checked_at": now.isoformat(),
    }


def record_answer(state_file: Path, timestamp: str | None = None) -> dict:
    state = load_state(state_file)
    now = timestamp or datetime.now(CST).isoformat()
    state["answers"].append(now)
    state["answers"] = dedupe_timestamps(state["answers"])
    save_state(state_file, state)
    return {"status": "recorded", "timestamp": now, "total_answers": len(state["answers"])}


def main() -> int:
    parser = argparse.ArgumentParser(description="Zhihu Publishing Cadence Guard")
    parser.add_argument("--state", type=Path, default=get_default_state_path(), help="State json file path")
    subparsers = parser.add_subparsers(dest="cmd")

    subparsers.add_parser("check", help="Check if publishing is currently allowed")
    rec_parser = subparsers.add_parser("record-answer", help="Record an answer publish event")
    rec_parser.add_argument("--time", help="ISO format timestamp")

    cd_parser = subparsers.add_parser("set-cooldown", help="Set temporary risk cooldown (hours)")
    cd_parser.add_argument("hours", type=float, default=48.0)

    args = parser.parse_args()

    if args.cmd == "check" or not args.cmd:
        res = check_cadence(args.state)
        print("=" * 60)
        print(" Zhihu Cadence Guard Check")
        print("=" * 60)
        print(f"[*] 今日发布: {res['today_count']} 条 | 本周发布: {res['week_count']} 条")
        print(f"[*] 黄金窗口: {res['golden_window'] or '非主力波峰时段'}")
        if res["allowed"]:
            print("\n[+] ALLOWED: 节律正常，允许发布。")
            return 0
        else:
            print("\n[-] BLOCKED: 当前触发限频阻断：")
            for r in res["reasons"]:
                print(f"  - {r}")
            if res["wait_seconds"] > 0:
                mins = res["wait_seconds"] // 60
                print(f"\n[*] 建议等待睡眠时间: {res['wait_seconds']} 秒 (~{mins} 分钟)")
            return 1

    elif args.cmd == "record-answer":
        res = record_answer(args.state, args.time)
        print(f"[+] 记录成功: {res['timestamp']} (总记录: {res['total_answers']} 条)")
        return 0

    elif args.cmd == "set-cooldown":
        state = load_state(args.state)
        cd_dt = datetime.now(CST) + timedelta(hours=args.hours)
        state["cooldown_until"] = cd_dt.isoformat()
        save_state(args.state, state)
        print(f"[!] 触发安全冷却直至: {cd_dt.strftime('%Y-%m-%d %H:%M:%S CST')}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
