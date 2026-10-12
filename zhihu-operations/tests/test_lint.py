#!/usr/bin/env python3
"""Unit tests for Zhihu answer linter."""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from lint import check_text


class TestZhihuLinter(unittest.TestCase):
    def test_clean_technical_answer_passes(self):
        good_text = """先直接给实测结论：在 macOS 与 Linux 生产环境下，如果脚本涉及到并发执行与大量输出捕获，直接无脑用 subprocess.run 会在缓冲区写满 64KB 时发生死锁阻塞。

这个问题我们在本地运行流水线时踩过整整两次坑。下面把复现条件、底层内核机制和我们最终跑通的规避方案完整摊开。

很多同学在写自动化脚本时习惯这么调用：
res = subprocess.run(["pytest", "-v", "tests/"], capture_output=True)

表面看逻辑很清晰，但标准库底层实现藏着一个管道陷阱：
1. capture_output 本质是在系统底层创建了两个无名管道对接 stdout 和 stderr。
2. 操作系统内核为管道分配的缓冲区大小有限，在 Linux 和 macOS 下默认通常只有 64KB。
3. 当子进程打印的测试日志超过 64KB 时，内核管道缓冲区被填满，子进程的 write 系统调用会被挂起等待父进程读取。
4. 但此时父进程还在等待子进程退出，双方互相等待，直接形成死锁。

为了定位这个问题，我们在本地写了一个测试脚本，连续生成 100KB 的输出数据。实测在本地 M3 机器上运行，进程状态一直卡在 wait4 系统调用上，CPU 占用率为 0%，内存停滞在 14MB。

这套排查命令与无冗余的管道封装脚本已经整理在本地开源仓库里，需要的同学可去主页自取备查。大三日常在终端写代码实测，平时折腾 AI 编程与工作流提效，后续踩坑日志与脚本持续更新在主页。
"""
        res = check_text(good_text)
        self.assertTrue(res["passed"], f"Expected pass but got fails: {res['fails']}")

    def test_hard_banned_phrases_fail(self):
        text_with_bans = """这不是一个普通的工具，而是颠覆性的神器！作为一名程序员，在AI飞速发展的今天，让我们拭目以待。
对此你怎么看？如果觉得有用请点赞关注我。
"""
        res = check_text(text_with_bans)
        self.assertFalse(res["passed"])
        fails_str = " ".join(res["fails"])
        self.assertIn("不是A而是B", fails_str)
        self.assertIn("借身份压人", fails_str)
        self.assertIn("反问求互动", fails_str)
        self.assertIn("乞赞乞关注", fails_str)

    def test_too_short_fails(self):
        short_text = "字数太少，只有这一行。"
        res = check_text(short_text)
        self.assertFalse(res["passed"])
        self.assertTrue(any("字数严重不足" in f for f in res["fails"]))


if __name__ == "__main__":
    unittest.main()
