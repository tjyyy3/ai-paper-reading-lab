# 覆盖度扫描（机械命中，供人工判定）

> 由 `tools/coverage_scan.py` 生成。命中只代表「提到了相关线索」，不代表讲对了。
> 人工判定见 `verify/coverage_judgement.md`。

## G1 任务定义：k 篇里恰好一篇含答案

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 否 | — |
| A2_naive_nolimit.md | 是 | ument question answering）**：输入是一个问题和 k 篇文档，其中恰好一篇包含答案，k−1 篇是干扰文档。模型必须在上下文中定位到那篇文档并用它作答。 2. **键 |
| B_evidence.md | 是 | ents (e.g., passages from Wikipedia), where *exactly one* of the documents contains the answer to the；nce; 56.1%). \| \| 5 \| 任务（实验设置之一）：多文档问答——k 篇文档中恰有一篇含答案，其余为干扰文档 \| S21P1 \| In the multi-document q |
| C_conditions.md | 是 | **A. 任务与数据** - A1 多文档 QA：输入 = 1 个问题 + k 篇文档，*恰好一篇*含答案，k−1 篇为干扰文档（<<S21P1>>）。 - A2 数据：NaturalQu |

## G2 数据与文档粒度（NQ-Open / 2655 / ≤100 token / Contriever）

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 否 | — |
| A2_naive_nolimit.md | 是 | ## 三、实验是怎么做的 ### 3.1 多文档问答的构造 - **数据来源**：NaturalQuestions-Open，取标注的"长答案"为**段落**（而非列表或表格）的 **2655** 条查询；维基百科段落切块，每块不超过 **100 token**。 - **含答案文档**：使用 NaturalQuestions 标注中包含答案的那个维基百科段落。 - **干扰文档**：用检索系统（Contrieve；：输入上下文分别包含 **10、20、30** 篇文档。 - **指标**：准确率，判定 NaturalQuestions 标注的任一正确答案是否出现在模型输出中（沿用 Kandpal et al. 2022、M |
| B_evidence.md | 是 | -1 "distractor" documents do not. \| \| 6 \| 数据：NaturalQuestions-Open 中长答案为段落的 2655 条查询；文档为 ≤100 token 的 Wiki；P2 \| We instantiate this task with data from NaturalQuestions-Open, [...] we take the 2655 queries where t；ny of the correct answers (as taken from the NaturalQuestions annotations) appear in the predicted output. |
| C_conditions.md | 是 | 篇文档，*恰好一篇*含答案，k−1 篇为干扰文档（<<S21P1>>）。 - A2 数据：NaturalQuestions-Open，取"标注长答案为段落（非列表/表格）"的 2655 条 query（<<S21；档：Contriever（MS-MARCO 微调）检索"与 query 最相关且不含任何 NaturalQuestions 标注答案"的 k−1 个 chunk（<<S21P2>>）。 - A5 干扰文档按相关性；ny of the correct answers (as taken from the NaturalQuestions annotations) appear in the predicted output. |

## G3 指标：accuracy 判定方式 / greedy 解码

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 是 | 门的扩展上下文模型也如此。GPT-3.5-Turbo在20/30篇文档的设置下，中间位置的准确率可比最佳位置下降20%以上，甚至低于无文档的闭卷水平（56.1%）。16K、100K等扩展 |
| A2_naive_nolimit.md | 是 | 的程度 以 GPT-3.5-Turbo 的多文档问答为例：把含答案文档放到上下文中部时，准确率相比最好情况可**下降 20 个百分点以上**；在最坏情况下（20 篇和 30 篇文档设置；*下降 20 个百分点以上**；在最坏情况下（20 篇和 30 篇文档设置），带文档回答的准确率**低于完全不给任何文档的闭卷表现（56.1%）**。 也就是说，给了模型 20~30；**规模**：输入上下文分别包含 **10、20、30** 篇文档。 - **指标**：准确率，判定 NaturalQuestions 标注的任一正确答案是否出现在模型输出中（沿用 K |
| B_evidence.md | 是 | in order of decreasing relevance. \| \| 8 \| 指标：accuracy，判定标准为预测输出中是否出现任一标注正确答案 \| S21P3 \| Following K；al. (2022) and Mallen et al. (2023), we use accuracy as our primary evaluation metric, judging wh；分 \| FIG7 \| Although some models show perfect accuracy on this synthetic task (e.g., Claude-1.3 and |
| C_conditions.md | 是 | >）。解码：greedy（<<S22P1>>）。 **D. 评价指标** 多文档 QA：accuracy，判断预测输出中是否出现任一正确答案（<<S21P3>>）。KV retrieval 的指；-3.5-Turbo 与 Claude-1.3；>20 篇 \| \| 12 \| 评价指标为 accuracy（答案出现即算对），且用 greedy 解码 \| <<S21P3>>、<<S22P1>>；且用 greedy 解码 \| <<S21P3>>、<<S22P1>> \| "we use accuracy as our primary evaluation metric, judging wh |

## G4 上下文规模：10/20/30 篇文档

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 否 | — |
| A2_naive_nolimit.md | 是 | ，系统性地扫描位置即可得到"性能—位置"曲线。 - **规模**：输入上下文分别包含 **10、20、30** 篇文档。 - **指标**：准确率，判定 NaturalQuestions 标注的任；6K，Claude-1.3 8K vs. 100K）。当输入长度同时落在两者窗口内时（如 10 篇、20 篇文档设置），两条"性能—位置"曲线**几乎完全重合**——扩展上下文只是扩大了"；文中部时，准确率相比最好情况可**下降 20 个百分点以上**；在最坏情况下（20 篇和 30 篇文档设置），带文档回答的准确率**低于完全不给任何文档的闭卷表现（56.1%）**。 也 |
| B_evidence.md | 是 | the predicted output. \| \| 9 \| 文档规模设置：输入上下文含 10、20、30 篇文档 \| S23P1 \| We experiment with input conte；redicted output. \| \| 9 \| 文档规模设置：输入上下文含 10、20、30 篇文档 \| S23P1 \| We experiment with input context；：retriever-reader 设置下，阅读器性能远早于检索器召回饱和；检索文档超过 20 篇只带来约 1.5%（GPT-3.5-Turbo）/约 1%（Claude-1.3）的提升 |
| C_conditions.md | 是 | reader（<<S5P2>>）。 **B. 上下文规模** - B1 多文档 QA：10、20、30 篇文档（<<S23P1>>）。 - B2 KV：75、140、300 对（<<S32P1；in the middle of its input context" \| 多文档 QA；10/20/30 篇文档；限于所测模型；原文用 "often"、"can"，非全称 \| \| 2 \| 最差情；r（<<S5P2>>）。 **B. 上下文规模** - B1 多文档 QA：10、20、30 篇文档（<<S23P1>>）。 - B2 KV：75、140、300 对（<<S32P1>> |

## G5 模型清单与版本（0613 / Claude-1.3 / MPT-30B / LongChat）

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 否 | — |
| A2_naive_nolimit.md | 是 | 近期的语言模型已经可以把很长的文本作为输入（GPT-3.5-Turbo 4K/16K、Claude-1.3 8K/100K、LongChat-13B 16K、MPT-30B-Instruct 8K；者对比了同一模型的普通版与扩展上下文版（GPT-3.5-Turbo 4K vs. 16K，Claude-1.3 8K vs. 100K）。当输入长度同时落在两者窗口内时（如 10 篇、20 篇文档设置；型间差异很大 键值检索（75、140、300 个键值对，各 500 例）上： - **Claude-1.3 与 Claude-1.3（100K）**在所有测试长度上几乎满分，说明任务本身可解； - |
| B_evidence.md | 是 | 13 OpenAI model versions. \| \| 14 \| 模型（API 侧）：Claude-1.3（8K）与 Claude-1.3 (100K)；GPT-4 (8K) 只跑了多文档问答的子；versions. \| \| 14 \| 模型（API 侧）：Claude-1.3（8K）与 Claude-1.3 (100K)；GPT-4 (8K) 只跑了多文档问答的子集 \| S22P2 \| We a；value pairs (500 examples each). \| \| 19 \| 例外：Claude-1.3 与 Claude-1.3 (100K) 在所有评测长度上几乎满分，即 U 形退化并非所有 |
| C_conditions.md | 是 | 384；GPT-3.5-Turbo 4K；GPT-3.5-Turbo (16K) 16K；Claude-1.3 8K；Claude-1.3 (100K) 100K（<<S22P1>>/<<S22P2>；rbo 4K；GPT-3.5-Turbo (16K) 16K；Claude-1.3 8K；Claude-1.3 (100K) 100K（<<S22P1>>/<<S22P2>>）。 - B4 Flan-；)、GPT-3.5-Turbo、GPT-3.5-Turbo (16K)（0613 版本）、Claude-1.3、Claude-1.3 (100K)、GPT-4 (8K)（仅多文档 QA 子集）、MPT |

## G6 量级与基线（>20% / closed-book 56.1% / oracle 88.3%）

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 是 | 此。GPT-3.5-Turbo在20/30篇文档的设置下，中间位置的准确率可比最佳位置下降20%以上，甚至低于无文档的闭卷水平（56.1%）。16K、100K等扩展上下文版本与原版在原窗；30篇文档的设置下，中间位置的准确率可比最佳位置下降20%以上，甚至低于无文档的闭卷水平（56.1%）。16K、100K等扩展上下文版本与原版在原窗口内表现几乎重合，说明加长上下文窗口不等 |
| A2_naive_nolimit.md | 是 | 结果，是值得借鉴的做法。 ### 需要说明的边界 节选只给出了定性描述与少数具体数字（20% 以上的下降、56.1% 的闭卷、1.9% 的 Flan-UL2 差距、约 1.5%/1%；下（20 篇和 30 篇文档设置），带文档回答的准确率**低于完全不给任何文档的闭卷表现（56.1%）**。 也就是说，给了模型 20~30 篇文档、其中一篇明确写着答案，它反而不如凭参；Instruct \| 31.5% \| 81.9% \| \| GPT-3.5-Turbo \| 56.1% \| 88.3% \| \| GPT-3.5-Turbo (16K) \| 56.0% \| 8 |
| B_evidence.md | 是 | 1%). \| \| 4 \| 位置效应幅度：GPT-3.5-Turbo 多文档问答可下降超过 20%，20/30 文档设置的最差位置低于 closed-book \| S23P2 \| For；ocument QA performance can drop by more than 20%—in the worst case, performance in 20- and 30；与 U 形曲线（Figure 5、Figure 7）；GPT-3.5-Turbo 下降 >20% 且最差位置低于 closed-book 56.1%；扩展与非扩展上下文模型曲线几乎重合； |
| C_conditions.md | 是 | ocument QA performance can drop by more than 20%—in the worst case, performance in 20- and 30；呈 U 型；GPT-3.5-Turbo 最差场景比 closed-book 低、降幅可超 20%（<<S23P2>>）。 - 扩展版与非扩展版在共同窗口内"nearly identica；分，全称表述的覆盖范围受限（<<ABS>>、<<S32P1>>）。 4. **具体数值（>20%、1.9%、~1.5%、~1%）的原始曲线/表格**：节选只给文字与图注，未给 Figur |

## G7 反例与例外（Claude KV 近乎全对 / LongChat 140 对趋势不同）

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 否 | — |
| A2_naive_nolimit.md | 是 | 是两件不同的事。 ### 4. 合成任务上同样复现，但模型间差异很大 键值检索（75、140、300 个键值对，各 500 例）上： - **Claude-1.3 与 Claude；100K）**在所有测试长度上几乎满分，说明任务本身可解； - 其他模型明显吃力，尤其在 140 和 300 对的设置下； - **GPT-3.5-Turbo、GPT-3.5-Turbo；uct** 依然是在中间位置表现最差； - **LongChat-13B（16K）**在 140 对设置下趋势不同：定性观察发现，相关信息在开头时它倾向于**生成一段取 key 的代码* |
| B_evidence.md | 是 | S32P1 \| Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths, bu；ens from an input context. \| \| 18 \| 任务二设置：75、140、300 个 key-value 对，每种 500 个样例；位置效应仍出现（开头/结尾好、；xperiment with input contexts containing 75, 140, and 300 key-value pairs (500 examples each) |
| C_conditions.md | 是 | 2P1>> \| "Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths, bu；S32P1>>："Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths"。 2；文支撑或材料缺失） 1. **KV retrieval 的量化指标**：材料只说"do nearly perfectly""struggle"，指标名称/判分规则：材料未给出，故第 6、7 条只能以定性表述 |

## G8 扩展上下文模型未必更好（nearly identical / 几乎重合）

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 是 | 至低于无文档的闭卷水平（56.1%）。16K、100K等扩展上下文版本与原版在原窗口内表现几乎重合，说明加长上下文窗口不等于更会用上下文。检索器—阅读器实验进一步显示，阅读器性能远早于检索 |
| A2_naive_nolimit.md | 是 | 距巨大，说明定位/检索是主要瓶颈；其二，同一模型的普通版与扩展版在闭卷和 oracle 上几乎相同，再次说明扩展窗口没有改变模型本身的能力。 ### 3.4 键值检索的设置 - 输入上 |
| B_evidence.md | 是 | nce). \| \| 15 \| 扩展上下文模型未必更会用上下文：上下文同时装得下时，两者表现几乎相同 \| S23P3 \| These results indicate that extend；，GPT-3.5-Turbo 与 GPT-3.5-Turbo (16K) 的位置-性能曲线几乎重合 \| S23P3 \| For example, the 10- and 20-docume；>20% 且最差位置低于 closed-book 56.1%；扩展与非扩展上下文模型曲线几乎重合；Table 1 的 closed-book/oracle 数值；Claude-1.3 系 |
| C_conditions.md | 是 | art, we see that performance between them is nearly identical." \| 仅当输入同时落入两者窗口；例证为 GPT-3.5-Turbo 与其 16K 版的；的直觉相反。<<S23P3>>："performance between them is nearly identical"。 5. **MPT-30B（基座）也呈 U 型**，并非只有 instruct 模型如；book 低、降幅可超 20%（<<S23P2>>）。 - 扩展版与非扩展版在共同窗口内"nearly identical"（<<S23P3>>）。 - KV：Claude 系近乎全对；GPT-3.5 两版与 M |

## G9 机制是假设（hypothesize / 推测）+ Flan-UL2 1.9% 边界

| 答案 | 命中 | 命中原句（截断） |
| --- | --- | --- |
| A_naive.md | 否 | — |
| A2_naive_nolimit.md | 是 | 档在"看到后续文档"的情况下被编码，从而更好地估计文档间的相对重要性。这是全文少见的机制性推测，作者明确把它当作假设而非结论。 ### 6. 指令微调：抬高整体水位、压缩最坏差距，但；Flan-T5-XXL 趋势类似：上下文越长，把信息放中间造成的损失越大。 作者给出的假设是：编码器—解码器的**双向编码器**能让每篇文档在"看到后续文档"的情况下被编码，从而更；情况下被编码，从而更好地估计文档间的相对重要性。这是全文少见的机制性推测，作者明确把它当作假设而非结论。 ### 6. 指令微调：抬高整体水位、压缩最坏差距，但不改变形状 对比 M |
| B_evidence.md | 是 | the NaturalQuestions annotations. \| **作者推测（hypothesis）vs. 实测结果** 作者的推测/假设：①编码器-解码器架构可能因双向编码器能"看；-解码器架构可能因双向编码器能"看到后文文档"而更好地利用上下文窗口——原文明写 "We hypothesize"（S41P3 末句）；②"primacy bias"/"recency bias"；rom the NaturalQuestions annotations. \| **作者推测（hypothesis）vs. 实测结果** 作者的推测/假设：①编码器-解码器架构可能 |
| C_conditions.md | 是 | ）。 - GPT-4 (8K) 子集：趋势类似、绝对值更高（<<S22P2>>）。 **hypothesis / 非实测推断** - **hypothesis（作者明确标注）**：编码器-解码器；对值更高（<<S22P2>>）。 **hypothesis / 非实测推断** - **hypothesis（作者明确标注）**：编码器-解码器模型可能更会用上下文，因为双向编码器可"在后续文档；在后续文档的语境中处理每篇文档"，从而改善文档相对重要性估计。<<S41P3>>："We hypothesize that encoder-decoder models may make bett |
