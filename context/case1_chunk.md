# 案例 1 的输入材料（实际粘贴给模型的全部内容）

> **注意**：本文件顶部的这段说明**没有**发给模型。实际发给 A/A2/B/C 四个会话的，只有下面 `<<ABS>>` 到最后一个 `<<END>>` 之间的锚点段落，不含本节说明、不含文末的对照表。
>
> 用途：四组实验收到的输入完全相同。除这份节选外，会话没有别的上下文，也不允许联网检索。
> 出处：Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang.
> *Lost in the Middle: How Language Models Use Long Contexts*. arXiv:2307.03172v3（2023-11-20 修订版），TACL 2023。
> 处理方式：原文为英文，按段落切分为带锚点的片段（锚点 → 原文位置见文末对照表）。为降低模型对这篇知名论文的先验记忆，发给模型的节选里不含题名与作者，只保留 arXiv 编号相关的正文内容；段落保留英文原文，仅做少量省略，省略处标 `[...]`。锚点由我添加，原文中不存在。

---

<<ABS>>
While recent language models have the ability to take long contexts as input, relatively little is known about how well they use longer context. We analyze the performance of language models on two tasks that require identifying relevant information in their input contexts: multi-document question answering and key-value retrieval. We find that performance can degrade significantly when changing the position of relevant information, indicating that current language models do not robustly make use of information in long input contexts. In particular, we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models. Our analysis provides a better understanding of how language models use their input context and provides new evaluation protocols for future long-context language models.
<<END>>

<<INTRO4>>
For example, when relevant information is placed in the middle of its input context, GPT-3.5-Turbo's performance on the multi-document question task is lower than its performance when predicting *without any documents* (i.e., the closed-book setting; 56.1%). Furthermore, we find that models often have identical performance to their extended-context counterparts, indicating that extended-context models are not necessarily better at using their input context.
<<END>>

<<S21P1>>
In the multi-document question answering task, the model inputs are (i) a question to answer and (ii) k documents (e.g., passages from Wikipedia), where *exactly one* of the documents contains the answer to the question and k-1 "distractor" documents do not. This task requires the model to access the document that contains the answer within its input context and use it to answer the question.
<<END>>

<<S21P2>>
We instantiate this task with data from NaturalQuestions-Open, [...] we take the 2655 queries where the annotated long answer is a paragraph (as opposed to a list or a table). We use passages (chunks of at most 100 tokens) from Wikipedia as documents within our input contexts. [...] To obtain a document that answers the question, we use the Wikipedia paragraph that contains the answer from the NaturalQuestions annotations. To collect k-1 distractor documents that do not contain the answer, we use a retrieval system (Contriever, fine-tuned on MS-MARCO) to retrieve the k-1 Wikipedia chunks that are most relevant to the query and do not contain any of the NaturalQuestions-annotated answers. [...] In the input context, the distractor documents are presented in order of decreasing relevance.
<<END>>

<<S21P3>>
Following Kandpal et al. (2022) and Mallen et al. (2023), we use accuracy as our primary evaluation metric, judging whether any of the correct answers (as taken from the NaturalQuestions annotations) appear in the predicted output.
<<END>>

<<S22P1>>
We analyze several state-of-the-art open and closed language models. We use greedy decoding when generating outputs and leave exploration of other decoding methods to future work. We use a standard set of prompts for each model. [...] We experiment with MPT-30B-Instruct, which has a maximum context length of 8192 tokens. [...] We also evaluate LongChat-13B (16K), which extends the LLaMA-13B context window from 2048 to 16384 tokens [...].
<<END>>

<<S22P2>>
We use the OpenAI API to experiment with GPT-3.5-Turbo and GPT-3.5-Turbo (16K). We use the 0613 OpenAI model versions. GPT-3.5-Turbo has a maximum context length of 4K tokens, and GPT-3.5-Turbo (16K) is a version with an extended maximum context length of 16K tokens. We evaluate Claude-1.3 and Claude-1.3 (100K) with the Anthropic API; Claude-1.3 has a maximum context length of 8K tokens, and Claude-1.3 (100K) has an extended context length of 100K tokens. We also evaluate GPT-4 (8K) on a subset of multi-document QA experiments, finding similar results and trends as other models (though GPT-4 has higher absolute performance). Evaluating GPT-4 on the full multi-document QA and key-value retrieval experiments would cost upwards of $6000.
<<END>>

<<S23P1>>
We experiment with input contexts containing 10, 20, and 30 total documents. [...] To contextualize model performance, we also evaluate on the closed-book and oracle settings (Table 1). In the closed-book setting, models are not given any documents in their input context, and must rely on their parametric memory to generate the correct answer. On the other hand, in the oracle setting, language models are given the single document that contains the answer and must use it to answer the question.
<<END>>

<<T1>>
Table 1: Closed-book and oracle accuracy of language models on the multi-document question answering task.

| Model | Closed-Book | Oracle |
| --- | --- | --- |
| LongChat-13B (16K) | 35.0% | 83.4% |
| MPT-30B-Instruct | 31.5% | 81.9% |
| GPT-3.5-Turbo | 56.1% | 88.3% |
| GPT-3.5-Turbo (16K) | 56.0% | 88.6% |
| Claude-1.3 | 48.3% | 76.1% |
| Claude-1.3 (100K) | 48.2% | 76.4% |
<<END>>

<<S23P2>>
As illustrated in Figure 5, changing the position of relevant information in the input context leads to substantial decreases in model performance. In particular, we see a distinctive U-shaped performance curve—models are often much better at using relevant information that occurs at the very beginning (primacy bias) and very end of contexts (recency bias), and suffer degraded performance when forced to use information within the middle of its input context. For example, GPT-3.5-Turbo's multi-document QA performance can drop by more than 20%—in the worst case, performance in 20- and 30-document settings is lower than performance without *any* input documents (i.e., closed-book performance; 56.1%). These results indicate that current models cannot effectively reason over their entire context window when prompted for downstream tasks.
<<END>>

<<S23P3>>
When the input context fits in the context window of both a model and its extended-context counterpart, we see that performance between them is nearly identical. For example, the 10- and 20-document settings both fit in the context window of GPT-3.5-Turbo and GPT-3.5-Turbo (16K), and we observe that their performance as a function of position of relative information is nearly superimposed [...]. These results indicate that extended-context models are not necessarily better than their non-extended counterparts at using their input context.
<<END>>

<<FIG5>>
Figure 5: The effect of changing the position of relevant information (document containing the answer) on multi-document question answering performance. Lower positions are closer to the start of the input context. Performance is highest when relevant information occurs at the very start or end of the context, and rapidly degrades when models must reason over information in the middle of its input context.
<<END>>

<<S3P1>>
Given that language models struggle to retrieve and use information from the middle of their input contexts in the multi-document question answering task, to what extent can they simply *retrieve* from input contexts? We study this question with a synthetic key-value retrieval task, which is designed to provide a minimal testbed for the basic ability to retrieve matching tokens from an input context.
<<END>>

<<FIG7>>
Figure 7: The effect of changing the input context length and the position of relevant information on key-value retrieval performance. Lower positions are closer to the start of the input context. Although some models show perfect accuracy on this synthetic task (e.g., Claude-1.3 and Claude-1.3 (100K)), we see again that performance is often highest when relevant information is occurs at the very start or end of the context, and rapidly degrades when models must retrieve from the middle of the input context.
<<END>>

<<S32P1>>
We experiment with input contexts containing 75, 140, and 300 key-value pairs (500 examples each). [...] Figure 7 presents key-value retrieval performance. Claude-1.3 and Claude-1.3 (100K) do nearly perfectly on all evaluated input context lengths, but other models struggle, especially when contexts have 140 or 300 key-value pairs—although the synthetic key-value retrieval task only requires identifying exact match within the input context, not all models achieve high performance.
<<END>>

<<S32P2>>
Similar to our multi-document QA results, GPT-3.5-Turbo, GPT-3.5-Turbo (16K), and MPT-30B-Instruct have the lowest performance when they must access key-value pairs in the middle of their input context. LongChat-13B (16K) exhibits a different trend in the 140 key-value setting; we qualitatively observe that when relevant information is placed at the start of the input context, LongChat-13B (16K) tends to generate code to retrieve the key, rather than outputting the value directly.
<<END>>

<<S41P3>>
When Flan-UL2 is evaluated on sequences within its 2048-token training-time context window (Figure 8; left subplot), its performance is relatively robust to changes in the position of relevant information within the input context (1.9% absolute difference between best- and worst-case performance). When evaluated on settings with sequences longer than 2048 tokens (Figure 8; center and right), Flan-UL2 performance begins to degrade when relevant information is placed in the middle. Flan-T5-XXL shows a similar trend, where longer input contexts result in a greater performance degradation when placing relevant information in the middle of the input context. We hypothesize that encoder-decoder models may make better use of their context windows because their bidirectional encoder allows processing each document in the context of future documents, potentially improving relative importance estimation between documents.
<<END>>

<<S43P2>>
Surprisingly, we see that both MPT-30B and MPT-30B-Instruct exhibit a U-shaped performance curve, where performance is highest when relevant information occurs at the very beginning or very end of the context. Although the absolute performance of MPT-30B-Instruct is uniformly higher than that of MPT-30B, their overall performance trends are similar. We also observe that instruction fine-tuning slightly reduces the worst-case performance disparity from nearly 10% between the base model best- and worst-case performance to around 4%.
<<END>>

<<S5P2>>
We use language models in a standard retriever-reader setup. A retrieval system (Contriever, fine-tuned on MS-MARCO) takes an input query from NaturalQuestions-Open and returns the k documents from Wikipedia with the highest relevance score. [...] We see that reader model performance saturates long before retriever performance saturates, indicating that readers are not effectively using the extra context. Using more than 20 retrieved documents only marginally improves reader performance (~1.5% for GPT-3.5-Turbo and ~1% for Claude-1.3), while significantly increasing the input context length (and thus latency and cost).
<<END>>

<<CONC>>
We empirically study how language models use long input contexts via a series of controlled experiments. We show that language model performance degrades significantly when changing the position of relevant information, indicating that models struggle to robustly access and use information in long input contexts. In particular, performance is often lowest when models must use information in the middle of long input contexts. We conduct a preliminary investigation of the role of (i) model architecture, (ii) query-aware contextualization, and (iii) instruction fine-tuning to better understand how they affect how language models use context. Finally, we conclude with a practical case study of open-domain question answering, finding that the performance of language model readers saturates far before retriever recall.
<<END>>

---

## 锚点 → 原文位置对照表

| 锚点 | 原文位置（arXiv:2307.03172v3） |
| --- | --- |
| ABS | Abstract |
| INTRO4 | §1 Introduction 第 4 段 |
| S21P1 | §2.1 Experimental Setup 第 1 段 |
| S21P2 | §2.1 Experimental Setup 第 2 段 |
| S21P3 | §2.1 Experimental Setup 第 4 段（指标定义） |
| S22P1 | §2.2 Models 第 1 段 + Open models |
| S22P2 | §2.2 Models 关闭模型段（含脚注 5、6 内容） |
| S23P1 | §2.3 Results and Discussion 第 1 段 |
| T1 | Table 1（§2.3） |
| S23P2 | §2.3 小节 "Model performance is highest ..." 第 1 段 |
| S23P3 | §2.3 小节 "Extended-context models are not necessarily better ..." |
| FIG5 | Figure 5 图注 |
| S3P1 | §3 开头第 1 段 |
| FIG7 | Figure 7 图注 |
| S32P1 | §3.2 Results and Discussion 第 1 段 |
| S32P2 | §3.2 Results and Discussion 第 2 段 |
| S41P3 | §4.1 Effect of Model Architecture 第 3 段 |
| S43P2 | §4.3 Effect of Instruction Fine-Tuning 第 2 段 |
| S5P2 | §5 Is More Context Always Better? 第 2 段 |
| CONC | §7 Conclusion |
