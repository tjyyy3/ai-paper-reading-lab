# 第一步：结论成立所必需的实验条件

**A. 任务与数据**
- A1 多文档 QA：输入 = 1 个问题 + k 篇文档，*恰好一篇*含答案，k−1 篇为干扰文档（<<S21P1>>）。
- A2 数据：NaturalQuestions-Open，取"标注长答案为段落（非列表/表格）"的 2655 条 query（<<S21P2>>）。
- A3 文档单位：Wikipedia passages，每块至多 100 tokens（<<S21P2>>）。
- A4 干扰文档：Contriever（MS-MARCO 微调）检索"与 query 最相关且不含任何 NaturalQuestions 标注答案"的 k−1 个 chunk（<<S21P2>>）。
- A5 干扰文档按相关性降序排列（<<S21P2>>）。
- A6 KV retrieval：合成任务，75/140/300 组 key-value，每组 500 例（<<S32P1>>）。
- A7 检索-阅读器案例：Contriever（MS-MARCO 微调）返回 k 篇 Wikipedia 文档给 reader（<<S5P2>>）。

**B. 上下文规模**
- B1 多文档 QA：10、20、30 篇文档（<<S23P1>>）。
- B2 KV：75、140、300 对（<<S32P1>>）。
- B3 窗口：MPT-30B-Instruct 8192；LongChat-13B (16K) 由 2048 扩至 16384；GPT-3.5-Turbo 4K；GPT-3.5-Turbo (16K) 16K；Claude-1.3 8K；Claude-1.3 (100K) 100K（<<S22P1>>/<<S22P2>>）。
- B4 Flan-UL2 训练时上下文窗口 2048 tokens，另测更长序列（<<S41P3>>）。

**C. 参与评测的模型**
MPT-30B-Instruct、LongChat-13B (16K)、GPT-3.5-Turbo、GPT-3.5-Turbo (16K)（0613 版本）、Claude-1.3、Claude-1.3 (100K)、GPT-4 (8K)（仅多文档 QA 子集）、MPT-30B、Flan-UL2、Flan-T5-XXL（<<S22P1>>/<<S22P2>>/<<S43P2>>/<<S41P3>>）。解码：greedy（<<S22P1>>）。

**D. 评价指标**
多文档 QA：accuracy，判断预测输出中是否出现任一正确答案（<<S21P3>>）。KV retrieval 的指标名称与定义：材料未给出。检索案例中 reader/retriever "饱和"的具体指标：材料未给出。

**E. 对照基线**
- E1 closed-book：不给任何文档，仅靠参数记忆（<<S23P1>>，<<T1>>）。
- E2 oracle：只给含答案的单篇文档（<<S23P1>>，<<T1>>）。
- E3 扩展上下文模型 vs 其非扩展对应模型（<<S23P3>>）。
- E4 retriever 性能作为 reader 性能的对照（<<S5P2>>）。

# 第二步：逐条核对

| # | 结论 | 锚点 | 逐字引文 | 该结论的适用边界（依据原文） |
| --- | --- | --- | --- | --- |
| 1 | 改变相关信息位置会显著降低性能，曲线呈 U 型：开头/结尾好、中部差 | <<S23P2>> | "we see a distinctive U-shaped performance curve—models are often much better at using relevant information that occurs at the very beginning (primacy bias) and very end of contexts (recency bias), and suffer degraded performance when forced to use information within the middle of its input context" | 多文档 QA；10/20/30 篇文档；限于所测模型；原文用 "often"、"can"，非全称 |
| 2 | 最差情况下 GPT-3.5-Turbo 低于不给文档的 closed-book（56.1%） | <<S23P2>> | "GPT-3.5-Turbo's multi-document QA performance can drop by more than 20%—in the worst case, performance in 20- and 30-document settings is lower than performance without *any* input documents (i.e., closed-book performance; 56.1%)." | GPT-3.5-Turbo；20/30 篇设置；比较基准为 closed-book 56.1%（<<T1>>） |
| 3 | 输入同时装进两者窗口时，扩展版与非扩展版表现几乎相同 | <<S23P3>> | "When the input context fits in the context window of both a model and its extended-context counterpart, we see that performance between them is nearly identical." | 仅当输入同时落入两者窗口；例证为 GPT-3.5-Turbo 与其 16K 版的 10/20 篇设置 |
| 4 | 扩展上下文模型不一定更会用输入上下文 | <<S23P3>> | "These results indicate that extended-context models are not necessarily better than their non-extended counterparts at using their input context." | 所测扩展/非扩展配对；KV 任务中 Claude 系近乎满分属例外（见第三步） |
| 5 | 位置效应在 KV 检索上同样出现 | <<FIG7>> | "we see again that performance is often highest when relevant information is occurs at the very start or end of the context, and rapidly degrades when models must retrieve from the middle of the input context" | KV retrieval；75/140/300 对；原文用 "often"，且同句承认部分模型满分 |
| 6 | Claude-1.3 与 Claude-1.3 (100K) 在 KV 上近乎全对，其他模型吃力 | <<S32P1>> | "Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths, but other models struggle, especially when contexts have 140 or 300 key-value pairs—although the synthetic key-value retrieval task only requires identifying exact match within the input context, not all models achieve high performance." | KV 任务全部评测长度；"nearly" 非严格 100% |
| 7 | GPT-3.5-Turbo、GPT-3.5-Turbo (16K)、MPT-30B-Instruct 在 KV 中部最差 | <<S32P2>> | "Similar to our multi-document QA results, GPT-3.5-Turbo, GPT-3.5-Turbo (16K), and MPT-30B-Instruct have the lowest performance when they must access key-value pairs in the middle of their input context." | 仅这三个模型；KV 任务 |
| 8 | Flan-UL2 在 2048 token 训练窗口内对位置相对鲁棒（最好/最差差 1.9%） | <<S41P3>> | "When Flan-UL2 is evaluated on sequences within its 2048-token training-time context window (Figure 8; left subplot), its performance is relatively robust to changes in the position of relevant information within the input context (1.9% absolute difference between best- and worst-case performance)." | 仅限不超过 2048 tokens 的序列 |
| 9 | 序列超过 2048 tokens 后，中部放置开始退化 | <<S41P3>> | "When evaluated on settings with sequences longer than 2048 tokens (Figure 8; center and right), Flan-UL2 performance begins to degrade when relevant information is placed in the middle." | Flan-UL2；序列长于 2048 tokens 的设置 |
| 10 | MPT-30B 与 MPT-30B-Instruct 同呈 U 型；指令微调把最差差距从近 10% 缩到约 4% | <<S43P2>> | "We also observe that instruction fine-tuning slightly reduces the worst-case performance disparity from nearly 10% between the base model best- and worst-case performance to around 4%." | MPT-30B 系列；"slightly"；差距指 best- 与 worst-case 之差 |
| 11 | reader 性能远早于 retriever 性能饱和；超过 20 篇仅边际提升 | <<S5P2>> | "We see that reader model performance saturates long before retriever performance saturates, indicating that readers are not effectively using the extra context. Using more than 20 retrieved documents only marginally improves reader performance (~1.5% for GPT-3.5-Turbo and ~1% for Claude-1.3), while significantly increasing the input context length (and thus latency and cost)." | 检索-阅读器设置；~1.5%/~1% 为 GPT-3.5-Turbo 与 Claude-1.3；>20 篇 |
| 12 | 评价指标为 accuracy（答案出现即算对），且用 greedy 解码 | <<S21P3>>、<<S22P1>> | "we use accuracy as our primary evaluation metric, judging whether any of the correct answers (as taken from the NaturalQuestions annotations) appear in the predicted output."；"We use greedy decoding when generating outputs and leave exploration of other decoding methods to future work." | 多文档 QA 的 accuracy；其他解码方法未探索 |
| 13 | GPT-4 (8K) 仅子集实验，趋势类似但绝对性能更高 | <<S22P2>> | "We also evaluate GPT-4 (8K) on a subset of multi-document QA experiments, finding similar results and trends as other models (though GPT-4 has higher absolute performance)." | 仅多文档 QA 子集；未做全量（成本"upwards of $6000"） |

# 第三步：反例与例外

1. **Claude-1.3 / Claude-1.3 (100K)（KV 任务）**：与"中部必退化"的主结论不一致。<<FIG7>>："Although some models show perfect accuracy on this synthetic task (e.g., Claude-1.3 and Claude-1.3 (100K))"；<<S32P1>>："Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths"。
2. **LongChat-13B (16K)（140 对 KV 设置）**：趋势与其他模型不同。<<S32P2>>："LongChat-13B (16K) exhibits a different trend in the 140 key-value setting; we qualitatively observe that when relevant information is placed at the start of the input context, LongChat-13B (16K) tends to generate code to retrieve the key, rather than outputting the value directly."
3. **Flan-UL2（≤2048 tokens）**：在中部并不明显退化，与"中部退化"不一致，但只在其训练窗口内成立。<<S41P3>>："its performance is relatively robust to changes in the position of relevant information within the input context (1.9% absolute difference between best- and worst-case performance)"。
4. **扩展版并不优于非扩展版**：与"更长窗口应更强"的直觉相反。<<S23P3>>："performance between them is nearly identical"。
5. **MPT-30B（基座）也呈 U 型**，并非只有 instruct 模型如此。<<S43P2>>："both MPT-30B and MPT-30B-Instruct exhibit a U-shaped performance curve"。
6. "有模型在中部表现优于两端"这一反例：**材料中未见**（原文只写 "often highest"，未给出反向个例）。

# 第四步：实测结果 vs 作者推测

**实测结果（有数据/图表支撑）**
- Table 1：closed-book / oracle 准确率——LongChat-13B (16K) 35.0%/83.4%；MPT-30B-Instruct 31.5%/81.9%；GPT-3.5-Turbo 56.1%/88.3%；GPT-3.5-Turbo (16K) 56.0%/88.6%；Claude-1.3 48.3%/76.1%；Claude-1.3 (100K) 48.2%/76.4%（<<T1>>）。
- 位置曲线（图 5、图 7、图 8）呈 U 型；GPT-3.5-Turbo 最差场景比 closed-book 低、降幅可超 20%（<<S23P2>>）。
- 扩展版与非扩展版在共同窗口内"nearly identical"（<<S23P3>>）。
- KV：Claude 系近乎全对；GPT-3.5 两版与 MPT-30B-Instruct 中部最差；LongChat-13B (16K) 在 140 对设置异常并"生成代码"（<<S32P1>>、<<S32P2>>）。
- Flan-UL2 在 2048 内 1.9% 绝对差，超出后中部开始退化（<<S41P3>>）。
- MPT-30B/Instruct 均 U 型；指令微调把最差差距从近 10% 降到约 4%（<<S43P2>>）。
- reader 饱和：>20 篇后 GPT-3.5-Turbo 约 +1.5%、Claude-1.3 约 +1%（<<S5P2>>）。
- GPT-4 (8K) 子集：趋势类似、绝对值更高（<<S22P2>>）。

**hypothesis / 非实测推断**
- **hypothesis（作者明确标注）**：编码器-解码器模型可能更会用上下文，因为双向编码器可"在后续文档的语境中处理每篇文档"，从而改善文档相对重要性估计。<<S41P3>>："We hypothesize that encoder-decoder models may make better use of their context windows because their bidirectional encoder allows processing each document in the context of future documents, potentially improving relative importance estimation between documents."
- **hypothesis（作者由实测外推，原文未标 hypothesis）**："扩展上下文模型不一定更会用上下文"是从"共同窗口内几乎相同"外推到更大窗口（<<S23P3>>）；材料未给出超过共同窗口时的实测对照。
- **hypothesis（外推）**："current models cannot effectively reason over their entire context window when prompted for downstream tasks"（<<S23P2>>）——由多文档 QA 单一任务族外推到"downstream tasks"整体。
- **hypothesis（展望，无数据）**："Our analysis provides ... new evaluation protocols for future long-context language models."（<<ABS>>）
- **非 hypothesis，仅为定性观察且未验证机制**：LongChat-13B (16K) 在开头位置"tends to generate code"，材料未给出原因（<<S32P2>>）。

# 存疑（表格中无法用原文支撑或材料缺失）

1. **KV retrieval 的量化指标**：材料只说"do nearly perfectly""struggle"，指标名称/判分规则：材料未给出，故第 6、7 条只能以定性表述成立。
2. **query-aware contextualization**：<<CONC>> 称对其做了"preliminary investigation"，但节选中没有任何对应锚点、设置或数据：材料未给出，不能进表。
3. **"even for explicitly long-context models" 的全称量化**：所测显式长上下文模型仅 LongChat-13B (16K)、GPT-3.5-Turbo (16K)、Claude-1.3 (100K)，且 Claude 系在 KV 上近乎满分，全称表述的覆盖范围受限（<<ABS>>、<<S32P1>>）。
4. **具体数值（>20%、1.9%、~1.5%、~1%）的原始曲线/表格**：节选只给文字与图注，未给 Figure 5/7/8 的数据点：材料未给出，无法复核。
5. **Flan-UL2、Flan-T5-XXL、MPT-30B 的 closed-book/oracle 基线**：<<T1>> 只含六个模型，上述模型无对应基线：材料未给出。
6. **GPT-4 全量结论**：仅子集、未跑全量（成本"upwards of $6000"），不能把趋势推广到 GPT-4 的全部设置（<<S22P2>>）。
7. **"所有模型/所有任务都呈 U 型"**：原文用 "often"，且存在 Flan-UL2（≤2048）与 Claude 系 KV 两处不一致，不能写成全称结论。
