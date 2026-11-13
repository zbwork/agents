# 知办AI 官方数字员工

独立仓库：公开简介、人设、头像、欢迎语和技能关联。技能源码与包在 zbwork/skills，只引用稳定 skill_uuid，不复制技能。

- catalog/v1/employees.json：员工模板；UUID 为已有客户端关联标识，保持稳定。
- assets/agents/：SHA-256 命名的真实头像。

```sh
python3 scripts/build.py --skills-catalog ../skills/catalog/v1/skills.json --check
python3 scripts/build.py --skills-catalog ../skills/catalog/v1/skills.json
```

先发布 skills，再推送 agents。工作流读取 GitHub 已发布技能目录，引用缺失就拒绝发布，不回源旧服务器；员工目录/头像由 Pages 提供。Codex 仅本地提交，不执行 push。
