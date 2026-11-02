#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
style-<author> 自检测试脚本（模板）
由 style-distiller 生成。给定一篇用该风格写的稿子，校验是否达到风格基线。

用法: python3 selfcheck.py <稿件路径> [--json]

检查项（阈值可按风格在下方 CONFIG 调整）：
  1. 短句比例    : 长度<=15字的句子独立成段占比
  2. 括号不过长  : 括号旁白平均字数上限
  3. 书名号引用  : 《》出现次数下限
  4. 作者在场    : 作者直接对话读者的频率（每千字次数，下限）
  5. 收手边界    : 庄重/悲剧段落是否出现油滑黑名单词
"""

import argparse
import re
import sys
from pathlib import Path

# ===== 风格基线配置（蒸馏时按实际统计填入）=====
CONFIG = {
    "short_sentence_len": 15,        # 短句字数上限
    "short_para_ratio_min": 0.15,    # 短句成段占比下限（示例值，按需改）
    "bracket_avg_len_max": 15,       # 括号旁白平均字数上限
    "book_title_min": 3,             # 书名号《》最少次数
    "author_voice_per_kchar_min": 1.5,  # 每千字作者直接对话下限（示例值）
    # 作者跳出叙述直接对读者说话的标志（按需补充）
    "author_voice_markers": ["读者", "你看", "我们说", "其实", "各位"],
    # 庄重/悲剧场景禁止的油滑词黑名单（按需补充）
    "slip_blacklist": ["搞笑", "逗比", "嘻嘻", "哈哈", "戏精"],
    # 判定为庄重/悲剧段落的信号词
    "solemn_markers": ["牺牲", "死亡", "悲", "忠", "泪", "诀别"],
}


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def split_sentences(text: str):
    """按中英文标点切句，返回句子列表。"""
    parts = re.split(r"[。！？!?；;\n]", text)
    return [p.strip() for p in parts if p.strip()]


def count_chars(s: str) -> int:
    """统计非空白字符数（中文按字计）。"""
    return len(re.sub(r"\s", "", s))


def check(text: str):
    results = {}
    sentences = split_sentences(text)
    total = len(sentences)

    # 1 & 2: 短句成段 + 括号旁白
    short_paras = 0
    bracket_lengths = []
    for blk in re.split(r"\n\s*\n", text):
        blk = blk.strip()
        if not blk:
            continue
        # 单句成段且为短句
        if "\n" not in blk:
            sents = split_sentences(blk)
            if len(sents) == 1 and count_chars(sents[0]) <= CONFIG["short_sentence_len"]:
                short_paras += 1
        # 括号旁白
        for m in re.findall(r"[（(]([^（）()]{1,})[）)]", blk):
            bracket_lengths.append(count_chars(m))

    short_ratio = (short_paras / total) if total else 0.0
    bracket_avg = (sum(bracket_lengths) / len(bracket_lengths)) if bracket_lengths else 0.0
    results["short_para_ratio"] = round(short_ratio, 3)
    results["short_para_ratio_ok"] = short_ratio >= CONFIG["short_para_ratio_min"]
    results["bracket_count"] = len(bracket_lengths)
    results["bracket_avg_len"] = round(bracket_avg, 2)
    results["bracket_avg_len_ok"] = bracket_avg <= CONFIG["bracket_avg_len_max"]

    # 3: 书名号
    book_titles = len(re.findall(r"《[^》]*》", text))
    results["book_title_count"] = book_titles
    results["book_title_ok"] = book_titles >= CONFIG["book_title_min"]

    # 4: 作者在场
    chars = count_chars(text)
    voice_hits = sum(text.count(m) for m in CONFIG["author_voice_markers"])
    per_k = (voice_hits / chars * 1000) if chars else 0.0
    results["author_voice_per_kchar"] = round(per_k, 2)
    results["author_voice_ok"] = per_k >= CONFIG["author_voice_per_kchar_min"]

    # 5: 收手边界（庄重段落出现油滑词）
    slip_violations = []
    for blk in re.split(r"\n\s*\n", text):
        if any(sm in blk for sm in CONFIG["solemn_markers"]):
            for w in CONFIG["slip_blacklist"]:
                if w in blk:
                    slip_violations.append((w, blk[:30]))
    results["slip_violations"] = slip_violations
    results["slip_ok"] = len(slip_violations) == 0

    passed = all([
        results["short_para_ratio_ok"],
        results["bracket_avg_len_ok"],
        results["book_title_ok"],
        results["author_voice_ok"],
        results["slip_ok"],
    ])
    results["PASS"] = passed
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="稿件文件路径")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = ap.parse_args()

    if not Path(args.path).exists():
        print(f"文件不存在: {args.path}", file=sys.stderr)
        sys.exit(2)

    text = read_text(args.path)
    res = check(text)

    if args.json:
        import json
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("=== 风格自检结果 ===")
        for k, v in res.items():
            if k == "PASS":
                continue
            print(f"  {k}: {v}")
        print("=>", "PASS ✅" if res["PASS"] else "FAIL ❌")

    sys.exit(0 if res["PASS"] else 1)


if __name__ == "__main__":
    main()
