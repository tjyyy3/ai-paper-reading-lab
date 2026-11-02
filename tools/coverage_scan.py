#!/usr/bin/env python3
"""覆盖度扫描：把 G1–G9 九条限定条件在 A/B/C 答案里"是否被提到"机械地标出来。

这不是打分器。它只负责把候选证据句捞出来、给出命中/未命中，以及命中的原句，
方便人工判定（真正的 0/1/2 分是人在 `verify/coverage_judgement.md` 里给的）。
把这一步自动化，是为了让"漏了哪条"这件事可复核：读者可以换关键词、换答案重跑。

用法：
    python tools/coverage_scan.py --answers outputs/A_naive.md outputs/B_evidence.md \
        outputs/C_conditions.md --out verify/coverage_scan.md
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

# 每条条件给出若干"线索正则"。命中任一即视为"提到"，是否"讲对"仍由人判断。
CONDITIONS: list[tuple[str, str, list[str]]] = [
    ("G1", "任务定义：k 篇里恰好一篇含答案", [r"exactly one", r"恰好一篇", r"恰有一篇", r"只有一篇[^。\n]{0,12}(含|有)答案"]),
    ("G2", "数据与文档粒度（NQ-Open / 2655 / ≤100 token / Contriever）", [r"NaturalQuestions", r"2655", r"100 ?token", r"Contriever"]),
    ("G3", "指标：accuracy 判定方式 / greedy 解码", [r"accuracy", r"准确率", r"greedy", r"贪心"]),
    ("G4", "上下文规模：10/20/30 篇文档", [r"10[、,/ ]{0,3}20[、,/ ]{0,3}30", r"10 篇", r"30 篇", r"20 篇"]),
    ("G5", "模型清单与版本（0613 / Claude-1.3 / MPT-30B / LongChat）", [r"Claude-1\.3", r"MPT-30B", r"LongChat", r"0613"]),
    ("G6", "量级与基线（>20% / closed-book 56.1% / oracle 88.3%）", [r"20\s?%", r"56\.1", r"88\.3"]),
    ("G7", "反例与例外（Claude KV 近乎全对 / LongChat 140 对趋势不同）", [r"nearly perfect", r"近乎(全对|满分|完美)", r"140", r"趋势不同", r"different trend"]),
    ("G8", "扩展上下文模型未必更好（nearly identical / 几乎重合）", [r"nearly identical", r"几乎(相同|重合)", r"不一定(更|优于)", r"not necessarily better"]),
    ("G9", "机制是假设（hypothesize / 推测）+ Flan-UL2 1.9% 边界", [r"hypothes", r"推测", r"假设", r"1\.9"]),
]


def snippets(md: str, pattern: str, width: int = 90) -> list[str]:
    out = []
    for m in re.finditer(pattern, md, flags=re.I):
        start = max(0, m.start() - width // 2)
        snippet = md[start : m.end() + width // 2].replace("\n", " ")
        out.append(re.sub(r"\s+", " ", snippet).strip())
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", nargs="+", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    docs = {p.name: p.read_text(encoding="utf-8") for p in args.answers}
    lines = [
        "# 覆盖度扫描（机械命中，供人工判定）",
        "",
        "> 由 `tools/coverage_scan.py` 生成。命中只代表「提到了相关线索」，不代表讲对了。",
        "> 人工判定见 `verify/coverage_judgement.md`。",
        "",
    ]
    for cid, desc, pats in CONDITIONS:
        lines.append(f"## {cid} {desc}")
        lines.append("")
        lines.append("| 答案 | 命中 | 命中原句（截断） |")
        lines.append("| --- | --- | --- |")
        for name, md in docs.items():
            hits: list[str] = []
            for pat in pats:
                hits.extend(snippets(md, pat))
            uniq = list(dict.fromkeys(hits))[:3]
            lines.append(
                f"| {name} | {'是' if hits else '否'} | "
                + ("；".join(s.replace('|', '\\|')[:110] for s in uniq) if uniq else "—")
                + " |"
            )
        lines.append("")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
