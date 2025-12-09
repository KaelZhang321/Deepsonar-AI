[根目录](../../../CLAUDE.md) > [.spec-workflow](../../) > **templates**

# 模板系统模块

## 模块职责

负责提供标准化的软件开发文档模板，涵盖从需求分析到技术实现的完整开发流程。每个模板都经过精心设计，确保团队能够高效、一致地创建高质量的项目文档。

## 入口与启动

### 模板加载机制
- **默认位置**：`.spec-workflow/templates/` 目录
- **加载优先级**：用户自定义模板 > 默认模板
- **模板发现**：基于文件名模式匹配

### 核心文件清单
```
templates/
├── requirements-template.md    # 需求文档模板
├── design-template.md         # 设计文档模板
├── tasks-template.md          # 任务分解模板
├── product-template.md        # 产品概述模板
├── tech-template.md           # 技术栈模板
└── structure-template.md      # 项目结构模板
```

## 对外接口

### 模板选择接口
- **需求文档**：`requirements-template.md` - 用户故事和验收条件
- **设计文档**：`design-template.md` - 技术架构和组件设计
- **任务规划**：`tasks-template.md` - 开发任务分解和 AI 辅助提示
- **产品规划**：`product-template.md` - 产品愿景和成功指标
- **技术决策**：`tech-template.md` - 技术栈选择和架构约束
- **结构规范**：`structure-template.md` - 代码组织和命名规范

## 关键依赖与配置

### 依赖关系
- **无外部依赖**：纯 Markdown 文档，可独立使用
- **Markdown 解析器**：需要支持标准 Markdown 语法的解析器
- **模板引擎**：支持变量替换的模板处理系统

### 配置项
- **模板变量**：`{{projectName}}`, `{{featureName}}`, `{{date}}`, `{{author}}`
- **章节标记**：使用 Markdown 标题层级（H1-H4）
- **代码块**：支持语法高亮的代码示例
- **Mermaid 图表**：集成图表支持可视化架构

## 数据模型

### 模板元数据
```markdown
template_metadata:
  name: "模板名称"
  version: "1.0.0"
  description: "模板用途描述"
 适用阶段: ["需求分析", "技术设计", "开发规划"]
  支持变量: ["projectName", "featureName", "date", "author"]
```

### 内容结构
每个模板遵循统一的章节结构：
- **概述章节**：项目背景和目标
- **详细章节**：具体内容和要求
- **指导性内容**：填写示例和最佳实践
- **非功能性要求**：质量、性能、安全等约束

## 测试与质量

### 模板完整性检查
- **结构验证**：确保所有必需章节存在
- **语法检查**：验证 Markdown 语法正确性
- **链接完整性**：检查内部链接和引用的有效性

### 内容质量评估
- **实用性**：模板是否提供足够的指导信息
- **可读性**：文档结构和语言表达的清晰度
- **一致性**：模板间格式和风格的统一性

### 用户接受度测试
- **易用性测试**：新用户能否快速上手使用
- **效率提升**：使用模板后文档编写效率的改善
- **质量改善**：模板对文档质量的提升效果

## 常见问题 (FAQ)

### Q: 如何创建自定义模板？
A: 在 `user-templates/` 目录创建同名文件，即可覆盖默认模板。

### Q: 模板变量如何工作？
A: 使用双花括号语法 `{{variableName}}`，在生成文档时会被替换为实际值。

### Q: 可以嵌套使用模板吗？
A: 模板设计为独立使用，但可以在不同阶段使用不同的模板来构建完整的项目文档集。

### Q: 如何提交模板改进建议？
A: 通过项目的 issue 系统提交改进建议，或直接在用户模板目录创建改进版本。

## 相关文件清单

### 核心模板文件
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/.spec-workflow/templates/requirements-template.md`
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/.spec-workflow/templates/design-template.md`
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/.spec-workflow/templates/tasks-template.md`
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/.spec-workflow/templates/product-template.md`
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/.spec-workflow/templates/tech-template.md`
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/.spec-workflow/templates/structure-template.md`

### 配置和文档
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/.spec-workflow/user-templates/README.md`
- `/Users/kael/WorkSpaces/MyProjects/Deepsonar-AI/CLAUDE.md`

## 变更记录 (Changelog)

### 2025-12-09 - 模块初始化
- 完成模板系统模块的架构分析
- 创建模块级 CLAUDE.md 文档
- 识别核心模板文件和功能
- 建立质量检查和测试策略

---

*本文档由 AI 架构师自动生成，基于 2025-12-09 08:49:52 的项目状态分析*