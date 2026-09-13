# Battery Evidence & Mechanism Audit

<details>
<summary>☕ 支持作者</summary>

如果这个项目对你有帮助，欢迎自愿赞赏，支持后续维护。感谢你的支持！

使用微信扫描下方收款码：

<img src="https://raw.githubusercontent.com/R3ze959/eis-drt-batch-analysis-skill/main/.github/assets/wechat-pay.jpg" alt="微信赞赏收款码" width="280" />

</details>

[English](#english) | [中文](#中文)

> An independent, community-maintained Codex skill. This project is not an official OpenAI product.

## English

Battery Evidence & Mechanism Audit is a privacy-safe Codex skill for non-trivial research judgments in battery and materials electrochemistry. It helps researchers test whether experimental data and literature actually support a comparison, mechanism, novelty statement, or manuscript claim.

Instead of selecting a preferred story first, the skill separates observations from interpretations, evaluates evidence quality, compares competing explanations, checks experimental comparability, and identifies the fastest experiment or search that could change the decision.

### Version 2.0.0

This version adds adaptive research depth and independent subagent checks, informed by [official Astra guidance](https://developers.openai.com/api/docs/guides/latest-model#gpt-6-astra-behavior). It also works sequentially when collaboration tools are unavailable. Read the [full changelog](CHANGELOG.md).

The skill inherits the active model and settings. It does not increase context or reasoning limits. Complex delegated work can use more total tokens; simple tasks avoid unnecessary research overhead. No fixed token savings or measured scientific-accuracy increase is claimed.

### What it does

- audits mechanism, causality, novelty, and performance claims;
- checks evidence directness, method validity, scope match, replication, consistency, and bias risk;
- detects misleading cross-paper comparisons caused by different cell formats, loadings, pressures, temperatures, protocols, or normalization bases;
- distinguishes independent experimental units from technical repeats and repeated cycles;
- proposes compact controls and decisive follow-up experiments;
- delegates bounded source, quantitative, or alternative-explanation checks when useful, with the main agent rechecking decisive evidence;
- preserves historical current definitions and separates EIS/DRT, structure, and DFT evidence from stronger claims;
- routes raw CV, GCD, GITT, EIS, diffraction, and DFT work to specialist workflows when available;
- supports an optional, user-supplied JSONL literature corpus without bundling or copying it.

### Privacy and source boundary

This repository contains no paper library, bibliography, paper text, DOI list, embedding index, private path, account identifier, or private connector. It never assumes that a local library exists and never scans personal folders by default.

When a literature-dependent request has no supplied sources, the skill asks once whether the user wants to connect a private library. The user may continue without one; optional library setup does not block useful work with available sources. Any supplied library remains outside the skill and is treated as read-only.

### Install

Download `expert-electrochemistry-public-v2.0.0.zip` from the latest GitHub Release and extract it into your Codex skills directory so that the final path contains:

```text
${CODEX_HOME:-$HOME/.codex}/skills/expert-electrochemistry-public/SKILL.md
```

For upgrades, back up an existing installation and replace only this skill directory after reviewing local changes. Keep user corpora outside it. The JSONL format and recall command remain compatible with version 1.1.1.

Invoke it explicitly when needed:

```text
$expert-electrochemistry-public audit whether this battery-materials mechanism claim is supported.
```

### Scope

This skill is an evidence-and-claim-audit layer, not an all-in-one electrochemistry program. Raw-data parsing, plotting, curve fitting, Rietveld refinement, DFT execution, and primary literature retrieval should use appropriate specialist tools. This skill audits the interpretation and claim boundary after or alongside those workflows.

### Validate and build

From a clean Git checkout, run the Python tests. They use synthetic inputs and include code behavior, deterministic builds, privacy rules, and evaluation-case schema checks; they do not run model evaluations.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The release auditor deliberately rejects Git metadata and all unlisted files. Commit the intended release changes first, then export that exact commit into a clean directory for the source audit and build:

```bash
release_version="$(cat VERSION)"
release_work="$(mktemp -d)"
release_root="$release_work/expert-electrochemistry-public"
mkdir "$release_root"
git archive --format=tar HEAD | tar -xf - -C "$release_root"
PYTHONDONTWRITEBYTECODE=1 python3 "$release_root/scripts/audit_release_privacy.py" "$release_root"
PYTHONDONTWRITEBYTECODE=1 python3 "$release_root/scripts/build_release.py" --root "$release_root" --output "$release_work/expert-electrochemistry-public-v$release_version.zip"
PYTHONDONTWRITEBYTECODE=1 python3 "$release_root/scripts/audit_release_privacy.py" "$release_work/expert-electrochemistry-public-v$release_version.zip"
```

For an extracted release ZIP, run the audit/build directly from its package directory instead. The builder packages only allowlisted files, rejects symbolic links and unlisted files, uses deterministic ZIP metadata, and audits the completed archive. The audit is a conservative release gate, not proof that arbitrary content is non-sensitive. Keep published checksum files alongside the ZIP, outside the skill package.

The scenarios in `evals/behavior-cases.json` are synthetic prompts for manual or model-based evaluation. To evaluate behavior, supply the prompt and permitted inputs to an independent run, inspect the actual response, and compare it with the listed criteria. Schema-test success alone is not a model pass.

## 中文

Battery Evidence & Mechanism Audit 是一个面向电池与材料电化学研究的 Codex 技能，重点解决“现有实验和文献是否真的支持这个结论”这类问题。它适合机理判断、论文故事线审查、跨论文性能比较、实验设计和审稿意见压力测试。

它不会先选择一个喜欢的机理再寻找证据，而是先区分实验观察、作者解释、跨来源推断和工作假设，再检查方法有效性、实验条件是否可比、独立重复和可能的替代解释，最后给出能够改变判断的最快验证方法。

### 2.0.0 版本

新增分级研究深度与子代理独立复核，参考 Astra 的官方行为建议设计。缺少协作工具时可顺序完成检查。详见[完整更新日志](CHANGELOG.md)。

技能继承当前模型及设置，不扩大上下文或推理预算。复杂任务使用子代理时总 token 可能增加，简单任务则避免不必要的研究流程；目前未量化 token 节省或科研准确率提升。

### 主要功能

- 审查机理、因果、创新性和性能声称；
- 区分证据来源与证据质量；
- 检查半电池、全电池、液态和固态电池之间的适用边界；
- 识别载量、压力、温度、电解液量和归一化方式导致的不可比问题；
- 防止把循环数、光谱点或技术重复误当作独立样本；
- 比较多种竞争性解释及其可区分预测，提出最小控制组和决定性实验；
- 按需分派文献、数值或竞争解释复核，主代理回查关键证据；
- 保留历史倍率定义，明确 EIS/DRT、结构表征和 DFT 的证据边界；
- 可选连接用户自己提供的 JSONL 文献库，但不携带、复制或发布用户文献。

### 隐私边界

本项目不包含论文 PDF、论文全文、书目、DOI 列表、哈希索引、嵌入库、个人路径、账号标识或私有连接器。它不会默认搜索用户的主目录、Zotero、下载目录或科研硬盘。

当任务需要文献而用户尚未提供来源时，Skill 会询问一次是否需要连接私人文献库。用户可以直接选择不连接；可选的文献库连接不会阻塞使用现有来源开展的有效工作。任何用户文献库都保留在 Skill 目录之外，并以只读方式使用。

### 安装与使用

从 GitHub Releases 下载 `expert-electrochemistry-public-v2.0.0.zip`，解压到 Codex 的 Skills 目录，确保最终存在：

```text
${CODEX_HOME:-$HOME/.codex}/skills/expert-electrochemistry-public/SKILL.md
```

升级前请备份已有安装并检查本地修改，再替换本技能目录；用户语料应始终保存在技能目录之外。JSONL 格式和检索命令与 1.1.1 兼容。

使用示例：

```text
$expert-electrochemistry-public 评估这个电池材料的机理结论是否被现有证据支持。
```

### 适用边界

它是一个“证据与结论审查层”，不是原始数据处理和计算引擎。CV、GCD、GITT、EIS 原始数据分析、作图和拟合，Rietveld 精修、DFT 计算以及主要文献检索应由相应的专用工具完成；本 Skill 负责审查这些结果是否真正支持最终结论。

### 验证与打包

上方英文部分给出了可直接执行的命令。Git checkout 中先运行测试，再从已提交版本导出干净目录进行审计和构建；不要把 `.git` 加入发布清单。源码和最终 ZIP 均须通过审计。

自动测试检查代码和案例格式，不运行模型。`evals/behavior-cases.json` 中的合成场景需要独立执行并检查实际回答，才能判断行为是否符合预期。

## License / 许可证

Released under the [MIT License](LICENSE). The repository contains only original guidance and code; no third-party paper content is distributed.

本项目使用 [MIT License](LICENSE) 发布。仓库仅包含原创方法指南和代码，不发布任何第三方论文内容。
