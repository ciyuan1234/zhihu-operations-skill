# Contributing to Zhihu Operations Skill

欢迎对本项目做出贡献！为了保持高质、专业与技术严谨性，请遵守以下贡献准则：

## 提交准则 (Contribution Standards)

1. **三级证据链铁律**：所有提及的参数指标必须基于真实环境下的官方文档或本地压测日志，严禁凭空捏造无依据的虚假数字（如未经测量的伪精度耗时或倍率）。
2. **零说教与去 AI 腔**：坚决封杀「不是A而是B」、「综上所述」、「在AI飞速发展的今天」等模式化公文体与爹味说教。保持平级技术同侪交流的视角。
3. **算法与机制求真**：所有针对知乎威尔逊模型、多目标 DNN 推荐及致知计划激励规则的探讨，需基于官方公布资料或严密可复现的实测归纳。
4. **代码与单测覆盖**：修改 `scripts/` 下的脚本（`lint.py`、`guard.py`、`question_evaluator.py` 等）需同步完善 `tests/` 中的单元测试，确保 `python3 -m unittest` 全部通过。
5. **路径中立性**：严禁在代码或文档中硬编码个人本地绝对路径。

## 提交流程 (Pull Request Workflow)

1. Fork 本仓库并新建分支：`git checkout -b feature/your-feature-name`
2. 运行自动化检查与单元测试：
   ```bash
   python3 -m unittest discover -s zhihu-operations/tests -p "test_*.py"
   ```
3. 提交变更并推送：`git commit -m "feat: add ..."`
4. 发起 Pull Request，详细描述修改动机与实测验证结果。
