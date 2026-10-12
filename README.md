# 知乎硬核开发者全流程运营 Skill (Zhihu Operations Skill)

[![Hermes Agent Skill](https://img.shields.io/badge/Hermes_Agent-Skill-blue.svg)](https://hermes-agent.nousresearch.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)
[![Tested with Unittest](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](zhihu-operations/tests)

面向 **软件工程师、AI 开发者、开源构建者与计算机技术创作者** 的知乎全流程运营与内容工程化 Skill。

沉淀自知乎算法底层机制逆向分析、实机反垃圾对抗测试与多 Agent 自动化流水线，旨在解决技术创作者在知乎面临的四大核心瓶颈：
1. **排名机制认知偏差**：误以为赞多就能排前，不知道知乎核心是「威尔逊置信区间下界」与「领域加权计票」，专业同行的一个反对票即可导致回答沉底；
2. **被瓦力系统打标「包含 AI 创作内容」折叠降权**：充满「不是A而是B」的二元说教、公文式小结、过度加粗清单，缺乏真实的工位细节；
3. **技术硬伤与伪造数据被撕穿**：凭空编造未经测量的伪精度数据（如「提升 3.8 倍」、「耗时 18.2 秒」），被高权重同行在评论区反驳；
4. **商业变现路径混乱**：误把好物推荐卡插到致知计划答案中，直接导致高额流量阅读现金分成归零。

---

## 🌟 核心能力架构

```
zhihu-operations/
├── SKILL.md                                 # Hermes Agent / Claude Code 技能标准规范
├── scripts/
│   ├── lint.py                              # 去 AI 感文本自查、AI 密度检测与跨回答指纹门禁
│   ├── guard.py                             # 发布节奏守卫 (日限 1-2 条、6h 最小间隔、夜间禁发)
│   └── question_evaluator.py                # 潜力问题多维打分器 (供需比、曝光密度、冷启动难度)
├── references/
│   ├── wilson_ranking_and_algorithm.md      # 威尔逊得分模型数学原理、加权投票与反对票机制
│   ├── multi_target_feed_and_search.md      # DNN 8 目标推荐模型、收藏权重与全网长尾搜索复利
│   ├── anti_ai_linter_and_fingerprint.md    # 三大检测路径、硬禁词库、格式密度与跨回答指纹规避
│   ├── three_tier_evidence_system.md        # 三级证据链体系：官方文档 -> 本地实测 -> 定性观察
│   ├── publishing_cadence_and_antiban.md    # 发布配额、三大黄金波峰与冷启动生死 2 小时定律
│   └── monetization_and_traffic_separation.md# 四大变现通道详解与 80/20 物理隔离铁律
└── templates/
    ├── answer_technical_deep_dive.md        # 深度技术排错与内核机制解答模版
    ├── answer_tool_evaluation.md            # 工具对比与大型代码库实测选型模版
    └── consulting_card_hook.md              # 商业咨询转化回答尾部合规留白模版
```

---

## 🚀 核心铁律与运作机制

### 1. 威尔逊置信区间下界与反对票毁灭性 (Wilson Ranking)
- **赞同比远大于赞数**：知乎采用威尔逊置信区间下界排序，小样本下压低偶然高赞同比，大样本下惩罚负反馈。20 赞 0 反对的回答排名往往高于 500 赞 80 反对。
- **同行高权重反对是致命伤**：专业领域的高权重专家投出的反对票带有高额乘数效应。技术内容必须经得起推敲，绝不写带有硬伤的技术断言。

### 2. 三级证据链门禁 (Three-Tier Evidence System)
- **Level 1 (官方文档事实)**：明确引用厂商 Release Notes 或官方白皮书规范；
- **Level 2 (可复现本地实测)**：本地具有真实测试代码与日志文件支持，真实给出硬件环境（如 M3 Pro 18GB）；**严禁伪造伪精度数据**；
- **Level 3 (个人定性观察)**：缺乏仪器或打点支持时，**必须诚实退回定性描述**（「响应明显顺畅」、「大文件偶发卡顿」），绝不编造假数字。

### 3. 去 AI 感与跨回答指纹消除 (Anti-AI & Fingerprinting)
- **黄金前 100 字法则**：开篇前 3 句直接亮出最终实测结论与环境版本，严禁背景铺垫与宏大公文体叙事。
- **格式密度门禁**：全文加粗文字比例严格控制在 **≤ 8%**（防止营销清单体感），列表项总数 **≤ 8 条**。
- **跨回答指纹消除**：同账号下的多篇回答禁止反复使用「日期+先说结论」或「你们…吗？」等对称模板开头/收尾。

### 4. 商业化 80/20 物理隔离铁律
- **致知计划 (纯流量分成)**：要求 Lv4+、100+ 粉丝，纯靠技术阅读时长结算现金。**严禁包含任何好物推荐卡或咨询卡**，否则收益清零。保持 80% 的回答为纯技术内容。
- **商业带货与咨询 (20% 专区)**：针对硬件评测与图书推荐插入好物推荐卡；针对环境排错提供 1 对 1 付费咨询。

---

## 🛠️ 快速上手与 CLI 工具使用

### 一键安装到 Hermes Agent / Claude Code
```bash
git clone https://github.com/ciyuan1234/zhihu-operations-skill.git
cd zhihu-operations-skill

# 安装到本地 Hermes Agent 技能目录 (~/.hermes/skills/social-media/)
./install.sh
```

Windows PowerShell 用户：
```powershell
.\install.ps1
```

### 1. 运行本地回答合规自查 (`lint.py`)
在提交回答前检查是否存在 AI 腔调、过度加粗或数据缺失：
```bash
python3 zhihu-operations/scripts/lint.py zhihu-operations/templates/answer_technical_deep_dive.md
```
输出示例：
```
============================================================
 Zhihu Answer Linter Report
============================================================
[*] 纯文本字数: 1599 字 (致知计划底线 500 字，推荐 800-2000 字)
[*] 具体数值/版本证据: 6 处

Result: LINT PASSED
```

### 2. 检查发布节奏与防封状态 (`guard.py`)
```bash
# 检查当前是否允许发布
python3 zhihu-operations/scripts/guard.py check

# 记录一次回答发布行为
python3 zhihu-operations/scripts/guard.py record-answer

# 触发 48 小时安全冷却期
python3 zhihu-operations/scripts/guard.py set-cooldown 48
```

### 3. 评估知乎潜力问题流量价值 (`question_evaluator.py`)
计算问题的关注人数、回答数与供需比，评估威尔逊插队成功率：
```bash
python3 zhihu-operations/scripts/question_evaluator.py --followers 1800 --answers 25 --views 65000 --title "如何优雅地在Python中管理并发子进程？"
```
输出示例：
```
============================================================
 Zhihu Question Traffic Potential Report
============================================================
[*] 评估问题: 如何优雅地在Python中管理并发子进程？
[*] 综合潜力评分: 85.0 / 100
[*] 推荐评级: S (极度推荐：供需比极佳，威尔逊插队极易)
[*] 供需比 (关注者/回答数): 72.0
[*] 平均每答曝光 (Views/Answer): 2600

[*] 机制推论与诊断:
  - 黄金中体量问题 (300-5000)，插队容易且有足够曝光
  - 适度竞争区间 (3-40 回答)，易通过高赞同比进入前列
```

---

## 🧪 单元测试

本项目提供完整的单元测试套件，覆盖禁词拦截、AI 密度计算、节奏防封逻辑与问题评分：
```bash
python3 -m unittest discover -s zhihu-operations/tests -p "test_*.py"
```

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 开源。欢迎 Star、Fork 并提交 PR！
