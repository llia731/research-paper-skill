# Research Paper Skill V0.3

用于 Codex 的证据驱动科研论文工作框架。一个主 Skill、六个按需读取的工作流，以及可恢复的文献、实验和图表证据记录。

## V0.2 文献管理

本地导入 Zotero CSV、JSON；DOI 标准化、去重；**可选**使用 Crossref 核对 DOI 题名。页级 PDF 文本提取需安装 PyMuPDF。默认不联网。

## V0.3 实验与科研绘图

运行已经审查的实验命令并保存日志、源码 Commit 和数据哈希；从 CSV 生成折线或柱状 PDF 图表；通过哈希验证源数据和生成文件是否变更。**不自动判断统计方法正确性**，也不保证投稿期刊格式达标。

## 安装 Codex

```bash
git clone https://github.com/llia731/research-paper-skill.git ~/.codex/research-paper-repo
mkdir -p ~/.codex/skills
ln -s ../research-paper-repo ~/.codex/skills/research-paper
python -m pip install pymupdf matplotlib numpy
```

重新启动 Codex 后，在真实科研项目中使用：`$research-paper 请根据项目资料建立科研状态，并列出待核实的研究证据。`

## 命令

```bash
python scripts/init_project.py /path/to/research-project
python scripts/check_project.py /path/to/research-project
python scripts/literature.py zotero.csv --output /path/to/research-project/.research/literature-index.json
python scripts/pdf_notes.py paper.pdf --output notes/paper.json
python scripts/run_experiment.py /path/to/research-project --input data/test.csv --result experiment/results.csv -- python experiment/evaluate.py
python scripts/plot_results.py generate experiment/results.csv --x epoch --y score --output figures/score.pdf
python scripts/plot_results.py verify figures/score.pdf.json
python -m unittest discover -s tests -v
```

请勿提交包含商业秘密、个人信息或未公开技术的研究项目材料；仅在经批准的环境内处理涉密数据。本框架不代表已完成端到端科研验证。
