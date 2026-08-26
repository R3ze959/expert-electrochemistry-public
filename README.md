# Battery Evidence & Mechanism Audit

[English](#english) | [中文](#中文)

> An independent, community-maintained Codex skill. This project is not an official OpenAI product.

## English

Battery Evidence & Mechanism Audit is a privacy-safe Codex skill for non-trivial research judgments in battery and materials electrochemistry. It helps researchers test whether experimental data and literature actually support a comparison, mechanism, novelty statement, or manuscript claim.

Instead of selecting a preferred story first, the skill separates observations from interpretations, evaluates evidence quality, compares competing explanations, checks experimental comparability, and identifies the fastest experiment or search that could change the decision.

### What it does

- audits mechanism, causality, novelty, and performance claims;
- checks evidence directness, method validity, scope match, replication, consistency, and bias risk;
- detects misleading cross-paper comparisons caused by different cell formats, loadings, pressures, temperatures, protocols, or normalization bases;
- distinguishes independent experimental units from technical repeats and repeated cycles;
- proposes compact controls and decisive follow-up experiments;
- routes raw CV, GCD, GITT, EIS, diffraction, and DFT work to specialist workflows when available;
- supports an optional, user-supplied JSONL literature corpus without bundling or copying it.

### Privacy and source boundary

This repository contains no paper library, bibliography, paper text, DOI list, embedding index, private path, account identifier, or private connector. It never assumes that a local library exists and never scans personal folders by default.

When a literature-dependent request has no supplied sources, the skill asks once whether the user wants to connect a private library. The user may continue without one. Any supplied library remains outside the skill and is treated as read-only.

### Install

Download `expert-electrochemistry-public-v1.1.1.zip` from the latest GitHub Release and extract it into your Codex skills directory so that the final path contains:

```text
${CODEX_HOME:-$HOME/.codex}/skills/expert-electrochemistry-public/SKILL.md
```

OpenAI skill-capable workflows can also upload the skill directory or the release ZIP. See the [official OpenAI skill API reference](https://developers.openai.com/api/reference/python/resources/skills/methods/create).

Invoke it explicitly when needed:

```text
$expert-electrochemistry-public audit whether this battery-materials mechanism claim is supported.
```

### Scope

This skill is an evidence-and-claim-audit layer, not an all-in-one electrochemistry program. Raw-data parsing, plotting, curve fitting, Rietveld refinement, DFT execution, and primary literature retrieval should use appropriate specialist tools. This skill audits the interpretation and claim boundary after or alongside those workflows.

### Validate and build

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_release_privacy.py .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_release.py --output ../expert-electrochemistry-public-v1.1.1.zip
PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_release_privacy.py ../expert-electrochemistry-public-v1.1.1.zip
```

The release builder packages only allowlisted files, rejects symbolic links and unlisted files, creates deterministic ZIP metadata, and audits the completed archive. The privacy audit is a conservative release gate, not a mathematical proof that arbitrary content is non-sensitive.

## 中文

Battery Evidence & Mechanism Audit 是一个面向电池与材料电化学研究的 Codex 技能，重点解决“现有实验和文献是否真的支持这个结论”这类问题。它适合机理判断、论文故事线审查、跨论文性能比较、实验设计和审稿意见压力测试。

它不会先选择一个喜欢的机理再寻找证据，而是先区分实验观察、作者解释、跨来源推断和工作假设，再检查方法有效性、实验条件是否可比、独立重复和可能的替代解释，最后给出能够改变判断的最快验证方法。

### 主要功能

- 审查机理、因果、创新性和性能声称；
- 区分证据来源与证据质量；
- 检查半电池、全电池、液态和固态电池之间的适用边界；
- 识别载量、压力、温度、电解液量和归一化方式导致的不可比问题；
- 防止把循环数、光谱点或技术重复误当作独立样本；
- 比较多种竞争性解释，提出最小控制组和决定性实验；
- 可选连接用户自己提供的 JSONL 文献库，但不携带、复制或发布用户文献。

### 隐私边界

本项目不包含论文 PDF、论文全文、书目、DOI 列表、哈希索引、嵌入库、个人路径、账号标识或私有连接器。它不会默认搜索用户的主目录、Zotero、下载目录或科研硬盘。

当任务需要文献而用户尚未提供来源时，Skill 会询问一次是否需要连接私人文献库。用户可以直接选择不连接。任何用户文献库都保留在 Skill 目录之外，并以只读方式使用。

### 安装与使用

从 GitHub Releases 下载 `expert-electrochemistry-public-v1.1.1.zip`，解压到 Codex 的 Skills 目录，确保最终存在：

```text
${CODEX_HOME:-$HOME/.codex}/skills/expert-electrochemistry-public/SKILL.md
```

使用示例：

```text
$expert-electrochemistry-public 评估这个电池材料的机理结论是否被现有证据支持。
```

### 适用边界

它是一个“证据与结论审查层”，不是原始数据处理和计算引擎。CV、GCD、GITT、EIS 原始数据分析、作图和拟合，Rietveld 精修、DFT 计算以及主要文献检索应由相应的专用工具完成；本 Skill 负责审查这些结果是否真正支持最终结论。

## License / 许可证

Released under the [MIT License](LICENSE). The repository contains only original guidance and code; no third-party paper content is distributed.

本项目使用 [MIT License](LICENSE) 发布。仓库仅包含原创方法指南和代码，不发布任何第三方论文内容。
