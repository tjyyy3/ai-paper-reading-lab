#!/usr/bin/env python3
"""机械核查：A/B/C 三组答案里的每一条"逐字引文"是否真的出现在它所声称的锚点里。

为什么需要它：模型在"证据绑定"格式下会写出很像原文的引文，读者肉眼很难分辨
"这句确实在第 5 页第 2 段"和"这句是把两段拼起来后的产物"。这个脚本只做一件
很笨但可复现的事：

  把引文和锚点段落都归一成"只保留小写字母数字"的键，然后判断包含关系。

判定分三类：
  ok          —— 引文（去掉 [...] 省略号后）是该锚点段落的连续子串；
  wrong_anchor—— 引文不在这条锚点里，但在别的一条锚点里（引文对、锚点错）；
  not_verbatim—— 引文不在任何锚点里（改写、拼接、翻译或凭空生成）。

另外做两项辅助检查：
  number_unsupported —— 结论里的数字在它引用的那段原文里找不到；
  该行引文为空。

用法：
    python verify/check_answers.py --chunk context/case1_chunk.md \
        --answers outputs/A_naive.md outputs/B_evidence.md outputs/C_conditions.md \
        --outdir verify
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SPAN_RE = re.compile(r"<<([A-Z0-9]+)>>\n(.*?)\n<<END>>", re.S)
ANCHOR_IN_CELL = re.compile(r"<?<?\s*([A-Z][A-Z0-9]*)\s*>?>?")


def canon(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def load_spans(chunk_path: Path) -> dict[str, str]:
    raw = chunk_path.read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in SPAN_RE.finditer(raw)}


def split_row(line: str) -> list[str]:
    """按未转义的 | 切单元格（GFM 里表格内的竖线写作 \\|）。"""
    cells, buf, i = [], "", 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            buf += "|"
            i += 2
            continue
        if ch == "|":
            cells.append(buf)
            buf = ""
            i += 1
            continue
        buf += ch
        i += 1
    cells.append(buf)
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.strip() for c in cells]


def extract_tables(md: str) -> list[dict]:
    """抽出所有含 '锚点' 与 '逐字引文' 列的 markdown 表格。"""
    lines = md.splitlines()
    tables = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and "锚点" in lines[i] and "逐字引文" in lines[i]:
            header = split_row(lines[i].strip())
            idx = {name: header.index(name) for name in header if name}
            i += 1
            if i < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i].strip()):
                i += 1
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = split_row(lines[i].strip())
                if len(cells) >= len(header) - 1:
                    rows.append(cells)
                i += 1
            tables.append({"header": header, "idx": idx, "rows": rows})
            continue
        i += 1
    return tables


def quotes_in_cell(cell: str) -> list[str]:
    """取单元格里的引文。

    优先取成对英文引号包住的内容（模型常用这种写法）；没有引号就把整格当引文。
    """
    found = re.findall(r"[\"“]([^\"”]{12,})[\"”]", cell)
    if found:
        return found
    stripped = cell.strip().strip('"“”')
    return [stripped] if len(stripped) >= 12 else []


def verify_quote(quote: str, anchors: list[str], spans: dict[str, str]) -> tuple[str, str]:
    """返回 (verdict, detail)。[...] 省略号处允许断开，逐段都必须命中。

    一行可能引用多个锚点（例如 S21P3 + S22P1），此时只要每个引文片段能被
    "所引用锚点中的某一个"完整包含，就算通过；命中非引用锚点则算锚点错配。
    """
    fragments = [f for f in re.split(r"\[\.\.\.\]", quote) if len(canon(f)) >= 12]
    if not fragments:
        return "empty", "引文过短，未检查"
    cited = [(a, canon(spans[a])) for a in anchors if a in spans]
    if all(any(canon(f) in text for _, text in cited) for f in fragments):
        return "ok", ""
    for other, text in spans.items():
        if other in anchors:
            continue
        if all(canon(f) in canon(text) for f in fragments):
            return "wrong_anchor", other
    return "not_verbatim", ""


def numbers_in(text: str) -> list[str]:
    return re.findall(r"\d+(?:\.\d+)?%?", text)


def check_file(path: Path, spans: dict[str, str]) -> dict:
    md = path.read_text(encoding="utf-8")
    tables = extract_tables(md)
    results = []
    for table in tables:
        for row in table["rows"]:
            idx = table["idx"]
            anchor_cell = row[idx["锚点"]] if "锚点" in idx and idx["锚点"] < len(row) else ""
            quote_cell = row[idx["逐字引文"]] if "逐字引文" in idx and idx["逐字引文"] < len(row) else ""
            claim = row[idx["结论"]] if "结论" in idx and idx["结论"] < len(row) else ""
            anchors = [a for a in ANCHOR_IN_CELL.findall(anchor_cell) if a in spans]
            anchor = ", ".join(anchors) if anchors else None
            quotes = quotes_in_cell(quote_cell)
            if anchor is None:
                results.append(
                    {
                        "claim": claim,
                        "anchor": anchor_cell,
                        "quote": quote_cell,
                        "verdict": "unknown_anchor",
                        "detail": "锚点不在节选中",
                        "bad_numbers": [],
                    }
                )
                continue
            verdicts = []
            detail = ""
            for q in quotes:
                verdict, det = verify_quote(q, anchors, spans)
                verdicts.append(verdict)
                if det:
                    detail = det
            if "not_verbatim" in verdicts:
                verdict = "not_verbatim"
            elif "wrong_anchor" in verdicts:
                verdict = "wrong_anchor"
            elif verdicts and set(verdicts) == {"empty"}:
                verdict = "empty"
            else:
                verdict = "ok"

            span_canon = "".join(canon(spans[a]) for a in anchors)
            bad_numbers = [n for n in numbers_in(claim) if canon(n) not in span_canon]
            results.append(
                {
                    "claim": claim,
                    "anchor": anchor,
                    "quote": quote_cell,
                    "verdict": verdict,
                    "detail": detail,
                    "bad_numbers": bad_numbers,
                }
            )
    return {"file": path.name, "tables": len(tables), "rows": results}


def render(report: dict, spans: dict[str, str], out: Path) -> None:
    rows = report["rows"]
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    total = len(rows)
    ok = counts.get("ok", 0)
    lines = [
        f"# 核查报告：`outputs/{report['file']}`",
        "",
        "> 本文件由 `verify/check_answers.py` 生成，未经人工修改。判定规则见脚本头部注释。",
        "",
        f"- 解析到的证据表：{report['tables']} 个",
        f"- 证据行：{total} 行",
        f"- 通过（引文=所引锚点的连续子串）：{ok} 行",
        f"- 锚点错配（引文在别的锚点里）：{counts.get('wrong_anchor', 0)} 行",
        f"- 非逐字（任何锚点里都没有）：{counts.get('not_verbatim', 0)} 行",
        f"- 锚点无法解析：{counts.get('unknown_anchor', 0)} 行",
        f"- 空引文：{counts.get('empty', 0)} 行",
        f"- 结论中的数字在所引锚点里找不到：{sum(1 for r in rows if r['bad_numbers'])} 行",
        "",
    ]
    flagged = [r for r in rows if r["verdict"] != "ok" or r["bad_numbers"]]
    if flagged:
        lines += [
            "## 需要人看的部分",
            "",
            "| # | 结论（截断） | 锚点 | 判定 | 说明 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for i, r in enumerate(flagged, 1):
            note = r["detail"] or ("数字未在所引段落出现：" + "、".join(r["bad_numbers"]) if r["bad_numbers"] else "")
            claim = (r["claim"][:46] + "…") if len(r["claim"]) > 46 else r["claim"]
            claim = claim.replace("|", "\\|")
            lines.append(f"| {i} | {claim} | {r['anchor']} | {r['verdict']} | {note} |")
        lines.append("")
    else:
        lines += ["全部证据行通过机械校验。", ""]
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", required=True, type=Path)
    ap.add_argument("--answers", nargs="+", required=True, type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    args = ap.parse_args()

    spans = load_spans(args.chunk)
    args.outdir.mkdir(parents=True, exist_ok=True)
    summary = [
        "# A/B/C 机械核查汇总",
        "",
        "> 由 `verify/check_answers.py` 生成。只判断「引文是否在所引段落里」，不判断观点对错。",
        "",
        "| 答案文件 | 证据行 | 通过 | 锚点错配 | 非逐字 | 无锚点 | 数字无支撑 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for path in args.answers:
        report = check_file(path, spans)
        out = args.outdir / f"report_{path.stem}.md"
        render(report, spans, out)
        rows = report["rows"]
        c: dict[str, int] = {}
        for r in rows:
            c[r["verdict"]] = c.get(r["verdict"], 0) + 1
        summary.append(
            f"| `{path.name}` | {len(rows)} | {c.get('ok', 0)} | {c.get('wrong_anchor', 0)} | "
            f"{c.get('not_verbatim', 0)} | {c.get('unknown_anchor', 0)} | "
            f"{sum(1 for r in rows if r['bad_numbers'])} |"
        )
        print(f"{path.name}: rows={len(rows)} ok={c.get('ok', 0)} wrong_anchor={c.get('wrong_anchor', 0)} "
              f"not_verbatim={c.get('not_verbatim', 0)} unknown={c.get('unknown_anchor', 0)}")
    summary.append("")
    (args.outdir / "report_all.md").write_text("\n".join(summary), encoding="utf-8")
    print(f"wrote {args.outdir/'report_all.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
