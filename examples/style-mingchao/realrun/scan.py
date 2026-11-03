#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实八维扫描（style-distiller 步骤2）
对 corpus-sample.txt 做全量统计，产出八个维度的硬数字。
仅依赖标准库。
"""
import re
from pathlib import Path

TEXT = Path(__file__).parent / "corpus-sample.txt"
raw = TEXT.read_text(encoding="utf-8")

def count_chars(s: str) -> int:
    return len(re.sub(r"\s", "", s))

# 按空行分段
blocks = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]

# 句子切分（中英文句末）
def split_sentences(text: str):
    return [p.strip() for p in re.split(r"[。！？!?；;]", text) if p.strip()]

total_chars = count_chars(raw)
all_sentences = split_sentences(raw)
total_sentences = len(all_sentences)

# 1. 句式节奏：短句（<=15字）数量与占比
short_sents = [s for s in all_sentences if count_chars(s) <= 15]
short_sent_ratio = len(short_sents) / total_sentences if total_sentences else 0
avg_sent_len = total_chars / total_sentences if total_sentences else 0

# 2. 段落结构：单句成段（独立成段的短句）数量
single_line_short_paras = 0
for b in blocks:
    if "\n" not in b:
        ss = split_sentences(b)
        if len(ss) == 1 and count_chars(ss[0]) <= 15:
            single_line_short_paras += 1

# 3. 词汇偏好：书名号《》次数
book_titles = re.findall(r"《[^》]*》", raw)

# 4. 叙事视角：作者直接在场的标志词频率（每千字）
voice_markers = ["读者", "你看", "我们说", "其实", "各位", "要知道", "可以说", "我们这里", "大家好"]
voice_hits = sum(raw.count(m) for m in voice_markers)
voice_per_k = voice_hits / total_chars * 1000 if total_chars else 0

# 7. 修辞手法：括号旁白（中英文括号）
bracket_inner = []
for m in re.findall(r"[（(]([^（）()]{1,})[）)]", raw):
    bracket_inner.append(count_chars(m))
bracket_count = len(bracket_inner)
bracket_avg = sum(bracket_inner) / bracket_count if bracket_count else 0

# 5. 情感温度：抒情/反讽信号（粗统计）
tender_markers = ["其实", "希望", "幸福向往", "精彩", "光芒万丈", "命运之神"]
tender_hits = sum(raw.count(m) for m in tender_markers)

# 6. 论证逻辑：转折/铺垫词
logic_markers = ["然而", "于是", "但是", "当然", "因为", "所以"]
logic_hits = sum(raw.count(m) for m in logic_markers)

# 8. 整体基因：定梁（本样本梁=朱元璋/朱重八）；悬念钩子（段末问句/未完）
suspense_hooks = len(re.findall(r"[？?]\s*$", raw, flags=re.M))
beam = "朱元璋 / 朱重八（人物作梁）"

print("=" * 50)
print("真实八维扫描结果（样本：引子 + 第一章 童年）")
print("=" * 50)
print(f"语料总字数(去空白)      : {total_chars}")
print(f"总句数                 : {total_sentences}")
print(f"平均句长(字/句)         : {avg_sent_len:.1f}")
print(f"[1] 短句(<=15字)数/占比 : {len(short_sents)} / {short_sent_ratio:.3f}")
print(f"[2] 单句成段(短句)数    : {single_line_short_paras}")
print(f"[3] 书名号《》次数      : {len(book_titles)}  -> {book_titles}")
print(f"[4] 作者在场标记/千字   : {voice_hits} 次 / {voice_per_k:.2f} 每千字")
print(f"[7] 括号旁白 次数/均长  : {bracket_count} 次 / 均 {bracket_avg:.1f} 字")
print(f"[5] 抒情/温度信号次数   : {tender_hits}")
print(f"[6] 转折/铺垫词次数     : {logic_hits}")
print(f"[8] 悬念钩子(段末问号)  : {suspense_hooks}")
print(f"[8] 本样本梁            : {beam}")
print("=" * 50)

# 输出为机器可读，便于写 eight-dim-scan.md
out = {
    "total_chars": total_chars,
    "total_sentences": total_sentences,
    "avg_sent_len": round(avg_sent_len, 1),
    "short_sents": len(short_sents),
    "short_sent_ratio": round(short_sent_ratio, 3),
    "single_line_short_paras": single_line_short_paras,
    "book_titles": len(book_titles),
    "book_title_list": book_titles,
    "voice_hits": voice_hits,
    "voice_per_k": round(voice_per_k, 2),
    "bracket_count": bracket_count,
    "bracket_avg": round(bracket_avg, 1),
    "tender_hits": tender_hits,
    "logic_hits": logic_hits,
    "suspense_hooks": suspense_hooks,
    "beam": beam,
}
import json
(Path(__file__).parent / "scan-result.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("已写出 scan-result.json")
