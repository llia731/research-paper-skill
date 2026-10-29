---
name: research-paper
description: Evidence-driven research paper workflow in Codex, with literature verification, computational experiments, reproducible figures and manuscript review.
---
# Research Paper
该 Skill 用于科研任务路由、项目状态恢复和事实核验。按用户任务加载对应工作流，不按固定顺序运行全部阶段。
## 任务路由
- 研究选题与综述：`workflows/research.md`
- Zotero、DOI、PDF 与文献：`workflows/literature.md`
- 实验设计、执行及复现：`workflows/experiment.md`
- 图表制作：`workflows/figures.md`
- 论文撰写：`workflows/writing.md`
- 质量审查：`workflows/review.md`
## 通用要求
- 每次先读取研究项目中的 `.research/project.yaml` 和 `.research/workflow-state.yaml`。没有则初始化，禁止覆盖。
- 严格遵循 `references/research-integrity.md` 与 `references/evidence-contract.md`。
- 文献任务读取 `references/literature-rules.md`；实验和图表读取 `references/experiment-figure-rules.md` 和 `references/figure-standards.md`。
- 未运行的实验不可写成已完成。区分是否执行、数据来源、执行环境和验证范围。
- 不虚构 DOI、实验指标、工程实例、技术贡献。
- 本机 CLI 不等于本地模型，涉密资料须使用经批准的环境。
- 不修改原始数据，不将任务进度放在 Skill 安装目录。
