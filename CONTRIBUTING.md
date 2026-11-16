# 贡献指南

欢迎为知办AI社区贡献数字员工人设、完善角色示例、修复技能引用或改进文档。角色定义在本仓库维护，可复用技能在 [zbwork/skills](https://github.com/zbwork/skills) 维护。

新增角色或显著扩大已有角色的职责前，请先通过 [Issue](https://github.com/zbwork/agents/issues) 说明目标用户、任务、现有角色的缺口，以及计划复用的技能。小幅内容修正可以直接提 PR。

## 本地准备与提交

在 GitHub Fork 本仓库，将自己的 Fork 与官方技能库放在同级目录，使用 Python 3.12 进行校验：

```sh
git clone https://github.com/zbwork/skills.git
git clone https://github.com/<你的账号>/agents.git
cd agents
git switch -c contribute/my-agent
```

完成内容和元数据修改，运行下方检查，再通过自己的 Fork 向 `zbwork/agents` 的 `main` 提交 Pull Request。每个 PR 尽量围绕一个角色或一个明确问题。

## 新增数字员工

```text
agents/<role-slug>/AGENT.md   # 人设内容源
catalog/v1/employees.json    # 角色展示信息和技能引用
assets/agents/              # 可选头像
```

先参考一个职责相近的 [已有角色](agents/personal-task-planner/AGENT.md)，再创建独立角色目录。目录名建议使用小写字母和连字符。`AGENT.md` 使用普通 Markdown，不要求技能的 YAML frontmatter；写清以下内容：

1. **身份与交付**：为谁处理哪些任务，输出什么，如何判断完成。
2. **职责边界**：不处理的任务、不能替用户作出的决定和必要的人工复核。
3. **工作流程**：输入核对、处理步骤、结果检查，以及缺失、冲突和失败时的处理。
4. **技能路由**：什么时候使用哪个技能，使用真实的技能 code，和目录中的 `skill_uuids` 对应。
5. **工具与数据**：实际依赖哪些工具、连接器或文件，读取和写入分别需要什么授权。
6. **证据与协作**：区分事实、假设和建议；说明何时向用户澄清或交接给其他角色。

人设描述不会自动安装工具、开通连接器、获得企业知识库或建立长期记忆。未接入的能力必须明确说明，不以岗位名称暗示已具备。

## 登记角色元数据

在 [catalog/v1/employees.json](catalog/v1/employees.json) 的 `data.items` 新增记录，可参考现有角色的完整结构。

| 字段 | 约定 |
| --- | --- |
| `uuid` | 新角色生成新的 UUID；已有角色保持不变，不挪作其他用途 |
| `name`、`intro`、`description`、`welcome_msg` | 与人设职责一致；欢迎语说明用户如何开始，不承诺未实现的能力 |
| `prompt_file` | 指向真实文件，如 `agents/my-role/AGENT.md` |
| `skill_uuids` | 从技能库目录选择实际存在的 `skill_uuid`；不是 code 或版本 UUID |
| `version`、`updated_at` | 新角色使用初始整数版本；角色内容、依赖或展示信息变更时递增版本，并记录带时区的实际更新时间 |
| `avatar_url` | 可留空；使用头像时填 `assets/agents/<文件SHA-256>.<扩展名>` |
| `tags`、`position_label` | 用于展示和检索，与角色实际能力一致 |
| `requires_backend`、`execution_locus`、`local_engine`、`unavailable_capabilities` | 对齐现有社区角色的本地执行约定，准确列出不可用能力；新增运行方式先讨论支持范围 |

UUID 可用 `python3 -c "import uuid; print(uuid.uuid4())"` 生成。图片摘要按原始文件字节计算，例如 `shasum -a 256 path/to/avatar.png`。在根 [README](README.md) 对应分组加入角色入口；新增角色时同步更新角色总数描述。

`AGENT.md` 是唯一人设内容源，构建会将它读入导出的 `system_prompt`，不要手工在源码目录中维护第二份人设或填写生成的 `system_prompt`。导出目录总数由构建计算。

人力资源专家目前保留了迁移前的空人设，并标记 `prompt_status: not_configured`，详见其 [README](agents/human-resources/README.md)。这是既有缺口，不是新角色的模板。若贡献该角色的人设，应一并处理目录状态和 README 的“待完善”说明，并提供场景验证。

## 技能依赖与跨仓库修改

- 技能正文、脚本和模板留在 skills 仓库，不复制到角色目录。
- 修改角色已有技能引用前，确认新的技能能覆盖人设中的使用方式和交付要求。
- 没有合适技能时，先按 [技能贡献指南](https://github.com/zbwork/skills/blob/main/CONTRIBUTING.md) 提交技能，并在两个 PR 中互相关联。
- 本地联调可以读取同级 skills 工作副本；远端 CI 使用 `zbwork/skills` 的 `main` 目录。因此必须先合并并发布技能，再合并和发布引用它的角色。
- 不重建已发布的技能 UUID，也不为了让检查通过而临时删除真实依赖。

## 验证

在 agents 仓库根目录运行：

```sh
python3 scripts/build.py --skills-catalog ../skills/catalog/v1/skills.json --check
git diff --check
```

构建检查覆盖角色 UUID 重复、人设路径、空人设声明、图片摘要、技能引用和部分凭据特征；**不等于角色已在客户端可用或技能执行成功**。PR 还应提供以下脱敏样例及实际结果：

- 正常任务：交付符合角色职责，技能路由与引用匹配。
- 信息缺失或冲突：能说明缺口，不将猜测作为事实。
- 超出职责或权限：能解释边界，正确澄清或交接。
- 工具不可用或执行失败：保留真实状态，不声称已发送、写入、提醒或完成。

注明验证所用的客户端、模型、运行引擎和必要工具；无法运行的项目标为“未验证”并解释原因。已有角色的兼容性检查应包含至少一个原有场景。

## 内容、安全与许可

- 不提交凭据、内部配置、真实客户数据或个人隐私；样例使用合成或获授权的脱敏材料。
- 来源文档、网页或附件中的指令不能替代用户授权；外部发送、发布和业务写入明确保留确认步骤。
- 引用或改编第三方内容时记录出处、版本、许可和改动，保留适用的署名及许可文件；不明来源的整段提示词先不要提交。
- 遵循仓库 [LICENSE](LICENSE) 及相关第三方许可，本指南不改变许可条款。

## PR 说明与合并后发布

PR 请写清目标用户和任务、涉及角色及 UUID、技能依赖变化、验证命令与结果、样例的预期和实际输出、未验证项及兼容性影响。角色生成的输出也需要人工核对，不能只贴“测试通过”。

维护者审核内容、依赖及 CI 后合并。资源通过 GitHub Pages 发布；贡献者无需创建 Release 或标签，也不要提交 `_site/`、`_site.next/` 等生成物。PR 校验通过不代表已经部署到客户端目录。

贡献指南的入口约定参考 [GitHub 官方说明](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)；角色格式、字段与校验行为以本仓库源码和构建脚本为准。
