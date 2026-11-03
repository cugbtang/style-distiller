# style-distiller · 风格蒸馏器

把任意作者 / 文本语料「蒸馏」成可复用的写作规律，并自动生成一份可直接安装使用的**写作风格 skill**。

> 灵感来源：一篇公众号文章《我用 WorkBuddy 把 375 章〈明朝那些事儿〉蒸成 43 条写作规律，做成一个历史故事 skill》。本文档把作者的方法论抽离成一套**对任意作者可复用**的蒸馏流程，而非只复刻明朝那一份。

## 核心铁律

**学的是动作，不是抄句子。** 只记录语句背后的规律，不记录原句、原比喻、原绰号。每条规律标注出处（章节 / 行号）以便核对。

## 蒸馏流程（八步）

1. **语料准入与清洗** —— 剔除序言 / 代序 / 注释 / 他人增补，做作者归属校验。
2. **八维扫描** —— 对清洗后语料全量统计，产出八个维度的硬数字（非读后感）。
3. **印记 / 偶然二分** —— 多章重复出现 = 可移用的「印记」；仅一次 = 不硬套的「偶然」。
4. **强度分级** —— 每条打 `硬 / 中 / 软`：全量统计撑得住为硬，多章交叉为中，仅 1–2 例为软（备用）。
5. **分层归档** —— 第一层管句子、第二层搭文章（核心「定梁」）、第三层何时收手、第四层整书布局 + 心法。
6. **生成风格 skill** —— 复制 `assets/style-skill-template/` 填入规律，得到可安装 skill。
7. **自检测试** —— 用 `scripts/selfcheck.py` 验收稿子是否达标。
8. **避坑自检** —— 声明覆盖率、列出剔除项、标软单例、维护版本修正对照表。

## 八维画像

句式节奏 · 段落结构 · 词汇偏好 · 叙事视角 · 情感温度 · 论证逻辑 · 修辞手法 · 整体基因

## 目录结构

```
style-distiller/
├── SKILL.md                       # 蒸馏主流程
├── README.md                      # 本文件
├── references/
│   └── distillation-guide.md      # 八维细则、强度标准、避坑、自检测试规范
├── assets/
│   └── style-skill-template/      # 生成的写作风格 skill 标准骨架
│       ├── SKILL.md
│       └── scripts/selfcheck.py
└── examples/
    └── style-mingchao/            # 第一个生成的风格 skill 示例（当年明月 / 明朝那些事儿）
        ├── SKILL.md
        ├── scripts/selfcheck.py
        └── realrun/               # 真实运行的产物（真实样本扫描+规律+避坑）
            ├── corpus-sample.txt   # 公开可获取的原文片段（引子+童年，1949字）
            ├── scan.py             # 真实八维扫描脚本
            ├── scan-result.json    # 真实统计结果
            ├── eight-dim-scan.md   # 八维真实统计（含覆盖率声明）
            ├── rules.md            # 规律清单（真实样本+强度分级）
            └── excluded-material.md# 剔除的非作者内容（演示避坑）
```

## 第一个示例：style-mingchao

`examples/style-mingchao/` 是用本 skill 产出的第一个「写作风格 skill」（当年明月 / 《明朝那些事儿》风格）。
- `SKILL.md` + `scripts/selfcheck.py`：可安装试用的风格 skill。数值融合「原博主全本报告值」与「真实样本印证」，已标注覆盖率。
- `realrun/`：**真实跑过一遍**的产物——对公开可获取的原文「引子+童年」做了真实八维扫描（括号旁白实测均长 5.6 字、史料书名号密集等），并演示了「剔除编辑导语/毛佩琦序言」的避坑。

提供全本 txt 后可经 `style-distiller` 重蒸补全，把标「软」的项升级为「硬/中」。
可直接安装试用：复制 `examples/style-mingchao/`（去掉 realrun 或保留均可）到 `~/.workbuddy/skills/style-mingchao/`。

## 安装到 WorkBuddy

将 `style-distiller/` 放入以下任一位置：
- 用户级：`~/.workbuddy/skills/style-distiller/`
- 项目级：`<项目>/.workbuddy/skills/style-distiller/`

重启 / 刷新后，用自然语言触发，例如：「帮我把《XXX》的写作手法拆成能复用的规则」。

## 真正有用的地方

蒸馏任何一本大部头只是实验样本。真正有价值的是这套方法论本身——八维画像 + 恒定/偶然二分 + 全量统计 + 强度分级。今天分析金庸，明天分析任意博主，路径都一样。
