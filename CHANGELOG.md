# Changelog / 更新日志

## 2.0.0 — 2026-09-10

### English

This release adds an adaptive, independently reviewed research workflow for Astra and other capable models. It preserves the public package's optional user-supplied corpus interface and privacy boundaries.

**Added**

- Bounded subagent assignments for primary-source verification, alternative explanations, quantitative checks, and prior-art searches. The main agent retains synthesis and rechecks decisive sources; agent agreement is not experimental replication.
- Minimal-context independent review, explicit source/condition handoffs, shared-file ownership, failure handling, and sequential fallback when collaboration tools are unavailable.
- Claim checks for historical C-rate definitions, normalization, EIS/DRT acceptance, GITT assumptions, phase-detection limits, defect attribution, and the different scopes of DFT energies and phonon results.
- Six synthetic evaluation scenarios for current normalization, incomplete EIS controls, useful delegation, unavailable agents, limited novelty/DFT evidence, and reviewer disagreement.

**Changed**

- Research depth follows the decision and evidence gaps. Simple questions remain direct; focused, deep, and near-systematic modes load references as needed.
- Inspection status, relevance, method validity, and source independence remain separate. Corpus-only or metadata evidence is not promoted to original-source verification.
- Hypotheses need discriminating predictions and counterevidence. Removed fixed explanation-count targets; unresolved alternatives remain unresolved.
- Optional library setup can proceed alongside useful research. Previously supplied authorization is preserved, and actual risk or missing information determines whether clarification is needed.
- Completion depends on verified decisive evidence and explicit scope limits, rather than paper counts or answer length.

**Fixed**

- Checkout-based reproducibility tests now use a clean copy without root Git metadata. Strict release auditing still rejects Git metadata and all other unlisted files.
- Build instructions export the committed release tree before auditing and packaging. The allowlist includes all new guidance and this changelog.

**Compatibility and validation**

- The skill name, JSONL format, recall CLI, and MIT license remain unchanged. No private library, project data, credentials, or local machine paths are included.
- The Python suite checks code, archive reproducibility, privacy rules, and evaluation-file structure. It does not run models or establish scientific accuracy.
- The packaged skill received bounded independent trials using synthetic inputs; these do not quantify accuracy improvements or token savings.
- Complex tasks using subagents can consume more total tokens. Simple tasks may use less overhead; no fixed cost multiplier is claimed. The skill does not change the active model, context window, or reasoning budget.

### 中文

本版加入适配 Astra 及其他具备相应能力模型的分级研究与独立复核流程，保留公开版的可选语料接口和隐私边界。

**新增**

- 子代理可分别核查原始证据、竞争解释、关键数值和最接近的已有研究；主代理负责综合判断并回查决定结论的来源。
- 独立复核尽量使用原始输入，减少已有结论的影响；补充分工范围、证据交接、文件所有权、失败处理和无子代理工具时的顺序回退。
- 加强历史倍率基准、单位与归一化、EIS/DRT 验收、GITT 假设、物相检测限、缺陷归因以及 DFT 能量与声子结果的证据边界。
- 增加六个合成评估场景，覆盖数值计算、缺失控制、子代理协作及不可用回退、创新性/DFT 过度推断和评审分歧。

**调整**

- 按问题和证据缺口选择研究深度，参考文件按需读取；简单问题不强制检索或调用子代理。
- 分开记录实际检查深度、体系相关性、方法有效性和来源独立性。
- 竞争解释需要可区分的预测和反证，不再为凑数量列举假设；无法区分时保留不确定性。
- 连接私人文献库是可选项，可与其他有效工作并行；尊重已有授权，按实际缺失信息和风险决定是否追问。
- 以关键证据核验和结论边界作为完成条件。

**修复**

- 修复 Git checkout 中的仓库元数据导致可复现构建测试失败的问题；发布审计仍拒绝仓库元数据及所有清单外文件。
- 更新从已提交代码导出干净目录的构建说明，并补齐发布清单与更新日志。

**兼容性与验证范围**

- 技能名称、JSONL 格式、检索命令和 MIT 许可证保持兼容，不包含私人语料、研究数据、凭据或本机路径。
- 自动测试覆盖代码行为、可复现打包、隐私规则与评估案例格式；不会执行模型或证明科研准确率。
- 对公开包进行了基于合成输入的有限独立试用，尚未量化准确率或 token 收益。
- 使用子代理的复杂任务可能消耗更多总 token；简单任务可能减少流程开销。本版不改变所用模型、上下文窗口或推理预算。

## 1.1.1 — 2026-08-26

Initial public release: evidence and mechanism auditing, battery comparison checks, an optional read-only JSONL corpus adapter, a bilingual README, MIT licensing, synthetic evaluation cases, and an allowlisted deterministic ZIP builder with source/archive privacy checks.

首次公开发布：证据与机理审查、电池性能比较检查、可选只读 JSONL 语料适配器、中英文说明、MIT 许可证、合成评估案例，以及带源码和归档隐私检查的白名单确定性 ZIP 构建流程。
