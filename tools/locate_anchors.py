#!/usr/bin/env python3
"""把带锚点的论文节选映射回 PDF 的页码。

为什么需要这个脚本：本仓库的正文用 S23P2 / T1 / FIG5 这样的锚点引用原文。读者要核对
"这句话在第几页"，不能靠我凭印象写。脚本用机械的词块（shingle）匹配把锚点定位到页，
并把覆盖率与低置信度条目一并列出，避免把猜出来的页码当成事实。

算法（可复现、无模型参与）：
1. 用 pypdf 逐页抽取文本，归一键 = 只保留小写字母和数字。
   PDF 抽取会把 "GPT-3.5" 拆成 "GPT-\\n3.5"、把破折号抽成乱码，去掉标点后两种版式
   才会落到同一个键上。
2. 把锚点段落切成句子，每句再切成 5 个词的词块（shingle）。
3. 对每页统计"该锚点的词块有多大比例出现在这一页"，取覆盖率最高的一页。
4. 覆盖率 < 0.6 的标 low-confidence，交给人工核对，不写成确定页码。

依赖：pypdf。论文 PDF 需读者自行从 arXiv 下载（本仓库不附带全文，见 NOTICE.md）。

用法：
    python tools/locate_anchors.py --pdf paper.pdf --chunk context/case1_chunk.md \
        --out evidence/anchor_pages.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    sys.exit("需要 pypdf：pip install pypdf")

SPAN_RE = re.compile(r"<<([A-Z0-9]+)>>\n(.*?)\n<<END>>", re.S)
SHINGLE = 5
LOW_CONF = 0.60


def words(text: str) -> list[str]:
    """切成词并逐词归一（去标点、转小写）。

    逐词归一是关键：PDF 的行末断词 "multi-\\ndocument" 与 HTML 的 "multi-document"
    都会得到 ["multi", "document"]，不必猜这个连字符是不是断词。
    """
    text = text.replace("[...]", " ").replace("*", " ")
    out = []
    for token in re.split(r"\s+", text):
        key = re.sub(r"[^a-z0-9]+", "", token.lower())
        if key:
            out.append(key)
    return out


def shingles(tokens: list[str], k: int = SHINGLE) -> list[str]:
    if len(tokens) < k:
        return ["".join(tokens)] if tokens else []
    return ["".join(tokens[i : i + k]) for i in range(len(tokens) - k + 1)]


def load_spans(chunk_path: Path) -> dict[str, str]:
    raw = chunk_path.read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in SPAN_RE.finditer(raw)}


def page_token_join(pdf_path: Path) -> tuple[list[str], str]:
    reader = PdfReader(str(pdf_path))
    pages = ["".join(words(page.extract_text() or "")) for page in reader.pages]
    return pages, "".join(pages)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--chunk", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    spans = load_spans(args.chunk)
    pages, joined = page_token_join(args.pdf)

    rows = []
    for anchor, span in spans.items():
        body = re.sub(r"^\s*(Formula|Table|Figure)\s*\d+[:.]\s*", " ", span)
        sh = shingles(words(body))
        if not sh:
            rows.append({"anchor": anchor, "page": None, "cov": 0.0, "n": 0})
            continue
        # 每页命中数（同一词块在一页里出现多次只算一次）
        best_page, best_cov = None, 0.0
        for page_no, page_text in enumerate(pages, start=1):
            hit = sum(1 for s in sh if s in page_text)
            cov = hit / len(sh)
            if cov > best_cov:
                best_page, best_cov = page_no, cov
        # 跨页兜底：整段被页边界切开时，合并文本上的命中率
        hit_all = sum(1 for s in sh if s in joined)
        cov_all = hit_all / len(sh)
        rows.append(
            {
                "anchor": anchor,
                "page": best_page,
                "cov": round(best_cov, 3),
                "n": len(sh),
                "cov_all": round(cov_all, 3),
            }
        )

    ok = [r for r in rows if r["page"] and r["cov"] >= LOW_CONF]
    low = [r for r in rows if r["page"] and r["cov"] < LOW_CONF]
    none = [r for r in rows if not r["page"]]

    lines = [
        "# 锚点 → PDF 页码（脚本输出，未经人工修改）",
        "",
        f"- 输入 PDF：`{args.pdf.name}`（共 {len(pages)} 页）",
        f"- 输入节选：`{args.chunk.as_posix()}`",
        f"- 词块长度：{SHINGLE} 词；置信阈值：覆盖率 ≥ {LOW_CONF}",
        f"- 锚点 {len(rows)} 个：高置信 {len(ok)}，低置信 {len(low)}，未定位 {len(none)}",
        "",
        "| 锚点 | 页码 | 页面覆盖率 | 词块数 | 判定 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        cov = r["cov"]
        verdict = "ok" if (r["page"] and cov >= LOW_CONF) else ("low-confidence" if r["page"] else "未定位")
        lines.append(
            f"| {r['anchor']} | {('p.' + str(r['page'])) if r['page'] else '—'} | "
            f"{cov:.2f} | {r['n']} | {verdict} |"
        )
    lines += [
        "",
        "说明：覆盖率 = 该锚点切出的 5 词词块中，出现在该页的比例。"
        "不取 1.00 的常见原因是节选里的 `[...]` 省略、引用括号被删、图注被图例文字打断。"
        "低置信条目不应当作确定页码使用，正文引用页码时以本表 ok 行为准。",
        "",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.out}: ok={len(ok)} low={len(low)} none={len(none)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
