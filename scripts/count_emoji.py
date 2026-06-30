#!/usr/bin/env python3
"""emoji / 装饰符计数助手。

quality_check.sh 与 quality_check.ps1 共用它来检测 emoji——shell 端 `grep -P` 仅 GNU 可用、
BSD/macOS 会静默跳过，两脚本会语义不一致。统一委托给这个 Python 实现后，两端在所有平台上
结果一致；任一端缺 Python 时都同样跳过，保持平价。

用法：python count_emoji.py <file>   # 打印文件中 emoji/装饰符的数量
"""
from __future__ import annotations

import re
import sys

# 覆盖主流 emoji 区段 + 杂项符号 / 箭头；CJK（U+4E00–9FFF）不在范围内，避免误伤正文
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿←-⇿⬀-⯿]")


def count_emoji(text: str) -> int:
    return len(EMOJI_RE.findall(text))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(0)
        return 0
    try:
        text = open(argv[1], encoding="utf-8").read()
    except OSError:
        print(0)
        return 0
    print(count_emoji(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
