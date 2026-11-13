# 知办AI 官方数字员工

数字员工源码独立维护。每个角色一个目录，AGENT.md 是唯一人设内容源；头像和技能引用保留原稳定标识。

## 数字员工

| 角色 | 人设 | 状态 |
| --- | --- | --- |
| 个人任务规划专家 | [AGENT.md](agents/personal-task-planner/AGENT.md) | 已迁移 |
| 演示设计顾问 | [AGENT.md](agents/presentation-designer/AGENT.md) | 已迁移 |
| 商务写作顾问 | [AGENT.md](agents/business-writer/AGENT.md) | 已迁移 |
| 研究分析师 | [AGENT.md](agents/research-analyst/AGENT.md) | 已迁移 |
| 客服运营专家 | [AGENT.md](agents/customer-service-operations/AGENT.md) | 已迁移 |
| 软件测试工程师 | [AGENT.md](agents/software-tester/AGENT.md) | 已迁移 |
| 应收应付管理专家 | [AGENT.md](agents/accounts-receivable-payable/AGENT.md) | 已迁移 |
| 税务合规顾问 | [AGENT.md](agents/tax-compliance/AGENT.md) | 已迁移 |
| 财务核算专家 | [AGENT.md](agents/financial-accounting/AGENT.md) | 已迁移 |
| 高级产品经理 | [AGENT.md](agents/senior-product-manager/AGENT.md) | 已迁移 |
| 客户成功经理 | [AGENT.md](agents/customer-success-manager/AGENT.md) | 已迁移 |
| 投标管理专家 | [AGENT.md](agents/bid-manager/AGENT.md) | 已迁移 |
| 合同管理专家 | [AGENT.md](agents/contract-manager/AGENT.md) | 已迁移 |
| 采购管理专家 | [AGENT.md](agents/procurement-manager/AGENT.md) | 已迁移 |
| 经营分析师 | [AGENT.md](agents/business-analyst/AGENT.md) | 已迁移 |
| 内容策划专家 | [AGENT.md](agents/content-strategist/AGENT.md) | 已迁移 |
| 销售运营分析师 | [AGENT.md](agents/sales-operations-analyst/AGENT.md) | 已迁移 |
| 高级项目经理 | [AGENT.md](agents/senior-project-manager/AGENT.md) | 已迁移 |
| 会议管理专家 | [AGENT.md](agents/meeting-manager/AGENT.md) | 已迁移 |
| 人力资源专家 | [AGENT.md](agents/human-resources/AGENT.md) | 原目录未配置独立人设 |

## 目录

```text
agents/
  personal-task-planner/
    AGENT.md
  business-writer/
    AGENT.md
catalog/v1/employees.json   # 元数据、头像路径、技能 UUID、prompt_file
assets/agents/             # 原始头像
```

## 维护与校验

编辑对应角色的 AGENT.md；修改名称、介绍、头像或技能引用时更新目录元数据。UUID 保持稳定。技能只引用 [zbwork/skills](https://github.com/zbwork/skills) 的 skill_uuid，不在本仓复制技能内容。

```sh
python3 scripts/build.py --skills-catalog ../skills/catalog/v1/skills.json --check
```

CI 只检查角色完整性、图片摘要与技能引用，直接读取 skills 的 GitHub 源码目录，不依赖 Pages 或 Release。后续客户端接入单独处理。

Codex 只做本地提交，远端推送由仓库所有者执行。
