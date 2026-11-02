# 标准答案：这篇论文的结论"成立条件"清单

> 这份清单是我的工作（人工整理），不是模型的输出。用途：给 A/B/C 三组答案打分时提供固定的比对基准，避免"看到答案才想起来该有什么"。
> 整理方法：只从 `context/case1_chunk.md` 里已经收录的段落中取证据；每条都附英文原文引文与锚点，页码来自 `evidence/anchor_pages.md`（脚本机械定位）。凡我判断属于"原文没有"的内容，一律标为"材料未给出"，不补背景知识。

论文：Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang. *Lost in the Middle: How Language Models Use Long Contexts*. arXiv:2307.03172v3（2023-11-20），TACL 2023。许可：arXiv.org perpetual non-exclusive license。

---

## G1 任务定义：恰好一篇文档含答案

- 要求：说明这是**多文档问答**任务，且 k 篇文档中**恰好一篇**含答案，其余 k−1 篇是干扰文档。
- 原文（S21P1，p.3）：
  > "In the multi-document question answering task, the model inputs are (i) a question to answer and (ii) k documents (e.g., passages from Wikipedia), where *exactly one* of the documents contains the answer to the question and k-1 "distractor" documents do not."
- 为什么算限定：它决定了结论的适用面——这是"单针在多篇文档里挪位置"，不是开放域检索，也不是多跳推理。

## G2 数据与文档粒度

- 要求：NaturalQuestions-Open；2655 条长答案为段落的 query；文档是 ≤100 token 的 Wikipedia 片段；干扰文档用 Contriever（MS-MARCO 微调）按相关性取、且不含标注答案；干扰文档按相关性降序排列。
- 原文（S21P2，p.3）：
  > "We instantiate this task with data from NaturalQuestions-Open, [...] we take the 2655 queries where the annotated long answer is a paragraph (as opposed to a list or a table). We use passages (chunks of at most 100 tokens) from Wikipedia as documents within our input contexts."
  > "In the input context, the distractor documents are presented in order of decreasing relevance."
- 为什么算限定：单一数据集、单一来源、单段落粒度。跨语言、跨文档类型（表格/列表）是否同样成立，原文没有测。

## G3 评价指标与解码方式

- 要求：accuracy，判定标准是**标注答案字符串是否出现在输出中**；生成用 greedy decoding。
- 原文（S21P3，p.3）：
  > "we use accuracy as our primary evaluation metric, judging whether any of the correct answers (as taken from the NaturalQuestions annotations) appear in the predicted output."
- 原文（S22P1，p.4）：
  > "We use greedy decoding when generating outputs and leave exploration of other decoding methods to future work."
- 为什么算限定：这是"字符串命中"式打分，不是人工判分；换解码策略、换判分方式都可能改变幅度。

## G4 上下文规模

- 要求：10 / 20 / 30 篇文档三档。
- 原文（S23P1，p.5）：
  > "We experiment with input contexts containing 10, 20, and 30 total documents."
- 为什么算限定："中间"是相对于 10~30 篇文档、约 4K~6K/16K token 的上下文而言；在更长或更短上下文里"中间"的位置不同。

## G5 参与评测的模型范围

- 要求：至少列出 6 个主评测模型（LongChat-13B (16K)、MPT-30B-Instruct、GPT-3.5-Turbo、GPT-3.5-Turbo (16K)、Claude-1.3、Claude-1.3 (100K)），并指出 GPT-3.5 用的是 0613 版本、GPT-4 只跑了子集。
- 原文（S22P1，p.4 / S22P2，p.5）：
  > "We experiment with MPT-30B-Instruct, which has a maximum context length of 8192 tokens."
  > "We use the OpenAI API to experiment with GPT-3.5-Turbo and GPT-3.5-Turbo (16K). We use the 0613 OpenAI model versions."
  > "We also evaluate GPT-4 (8K) on a subset of multi-document QA experiments, finding similar results and trends as other models (though GPT-4 has higher absolute performance)."
- 为什么算限定：模型清单就是结论的样本框。少了这一条，"长上下文模型会忽略中间"会被读成对 2023 年之后所有模型的断言。

## G6 量级与对照基线

- 要求：给出可核对的幅度：GPT-3.5-Turbo 下降 **>20%**；最差情况**低于不给文档的 closed-book 56.1%**；并知道 oracle 上界（GPT-3.5-Turbo 88.3%）。
- 原文（S23P2，p.5）：
  > "GPT-3.5-Turbo's multi-document QA performance can drop by more than 20%—in the worst case, performance in 20- and 30-document settings is lower than performance without *any* input documents (i.e., closed-book performance; 56.1%)."
- 原文（T1，p.5）：GPT-3.5-Turbo closed-book 56.1% / oracle 88.3%。
- 为什么算限定：只给"显著下降"而不给量级，读者无法判断这与自己的场景差多远；只给百分比不给基线与上界，也无法判断"下降"是否已经跌破不用上下文的水平。

## G7 反例与例外（最关键的一条）

- 要求：指出至少一个与主结论不一致的个例：Claude-1.3 与 Claude-1.3 (100K) 在 key-value 检索上几乎全对；LongChat-13B (16K) 在 140 对设置下趋势不同（倾向于生成取 key 的代码）。
- 原文（S32P1，p.6）：
  > "Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths, but other models struggle, especially when contexts have 140 or 300 key-value pairs—although the synthetic key-value retrieval task only requires identifying exact match within the input context, not all models achieve high performance."
- 原文（S32P2，p.6）：
  > "LongChat-13B (16K) exhibits a different trend in the 140 key-value setting; we qualitatively observe that when relevant information is placed at the start of the input context, LongChat-13B (16K) tends to generate code to retrieve the key, rather than outputting the value directly."
- 为什么算限定：它把"普遍规律"降级为"多数模型、多数设置在统计上如此"。没有这一条，读者会把"位置效应"当成模型能力的上限。

## G8 长上下文模型未必更会用上下文

- 要求：指出扩展上下文版本与普通版本在同一窗口内表现几乎重合，因此"窗口更长"不等于"更会用"。
- 原文（S23P3，p.5）：
  > "When the input context fits in the context window of both a model and its extended-context counterpart, we see that performance between them is nearly identical."
- 为什么算限定：这条直接反驳了"上下文窗口越大越好"的产品叙事，也是这篇论文最常被误读的地方之一。

## G9 机制解释属于假设，不是实测结论

- 要求：把"encoder-decoder 更会用上下文"标注为作者的 hypothesis；并知道 Flan-UL2 只在 ≤2048 token 的训练窗口内才稳健（best-worst 差 1.9%），超出后才出现中间退化。
- 原文（S41P3，p.7）：
  > "When Flan-UL2 is evaluated on sequences within its 2048-token training-time context window (Figure 8; left subplot), its performance is relatively robust to changes in the position of relevant information within the input context (1.9% absolute difference between best- and worst-case performance)."
  > "We hypothesize that encoder-decoder models may make better use of their context windows because their bidirectional encoder allows processing each document in the context of future documents, potentially improving relative importance estimation between documents."
- 为什么算限定：实测的是"曲线形状"，推测的是"为什么"。把 hypothesis 写成结论，是 AI 读论文时最常见的一类越界。

---

## 完整度计分规则（人工判定用）

| 判定 | 含义 |
| --- | --- |
| 2 分 | 条件被明确写出，且细节与原文一致（模型名、数字、设置没有错） |
| 1 分 | 写到但缺细节，或只写了一半（例如只提"有例外"但没说是哪个模型） |
| 0 分 | 没写，或写错 |

满分 18（9 条 × 2）。这份计分是我对"读者读完这段回答，是否足以判断结论能不能用在自己场景里"的判断，不是论文作者的评分。A/B/C 的判定见 `verify/coverage_judgement.md`。
