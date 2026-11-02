# 来源、许可与本次个人贡献

## 1. 被阅读的论文

- 题名：*Lost in the Middle: How Language Models Use Long Contexts*
- 作者：Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
- 版本：arXiv:2307.03172v3（2023-11-20 修订），共 18 页；同时被 TACL 2023 接收
- 稳定标识：https://arxiv.org/abs/2307.03172v3 ，DOI 10.48550/arXiv.2307.03172
- 许可：arXiv.org perpetual non-exclusive license（**不是** CC-BY）
- 本仓库怎么用它：只收录**为核查关键解读所必需**的短段原文摘录（约 1200 词，占全文很小一部分），逐段标注锚点、章节与页码；此外只保留论文的**数据性内容**（Table 1 的数值、图注文字），用于核对数字。
- **没有**收录论文 PDF、LaTeX 源或全文 HTML：该许可不允许转载全文，因此 `context/` 里只有合法摘录。想复现全文级操作，请自行从上面的 arXiv 地址下载 PDF（`tools/locate_anchors.py` 接受任何本地 PDF 路径）。
- 摘录中的英文原文未改写；删节处标 `[...]`。锚点标记（`<<S23P2>>` 这种）是我加的，原文没有。

## 2. 谁做了什么

| 内容 | 来源 |
| --- | --- |
| 论文原文、Table 1 数值、图注 | 论文作者（引用见上） |
| 阅读问题、锚点划分、`context/case1_chunk.md` 的切分与标注 | 本次工作 |
| 三组提示词（A / B / C / A2） | 本次工作 |
| `outputs/` 里的四份答案 | 由四个互相隔离的 AI 会话生成，**未经我改写**；每个会话只看到提示词与同一份节选 |
| G1–G9 限定条件清单（`evidence/ground_truth.md`） | 本次工作（人工整理，逐条附原文引文） |
| 覆盖度 0/1/2 判定（`verify/coverage_judgement.md`） | 本次工作（人工判定） |
| `verify/check_answers.py`、`tools/*.py` 与它们的输出 | 本次工作 |
| 页码映射（`evidence/anchor_pages.md`） | `tools/locate_anchors.py` 机械生成，未人工修改 |

## 3. 模型与工具

- 被测模型：DeepSeek Harness 会话内的 `deepseek-flash`。**具体版本号、温度等采样参数在会话侧不可见，我无法提供**，也不臆造。
- 调用方式：不是 API 调用，而是四个独立的 agent 会话；每个会话只收到提示词 + 节选，被明确要求不读文件、不联网、不使用先验记忆。会话隔离能减少污染，但**不能消除**：这篇论文很知名，模型可能本来就"记得"它，见 README 的局限一节。
- 抽取与核查工具：Python 3 + pypdf（`pip install pypdf`）。没有任何向量库、RAG 框架或 GPU 依赖。

## 4. 使用与再分发

- 本仓库的文字、脚本、判定表：可自由转载，注明出处即可。
- 论文摘录的版权属于原作者，按"引用 + 评论/核查"的有限使用收录；再分发前请自行确认适用法律与期刊政策。
- 未包含任何个人数据、访问凭据或 API key。`outputs/` 中的答案由模型生成，可能包含错误，不构成对论文内容的权威转述。
