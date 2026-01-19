# Agent Skills 格式规范

本文档描述了此仓库遵循的 Agent Skills 标准格式，兼容 [anthropics/skills](https://github.com/anthropics/skills) 规范。

## 目录结构

```
agent_skills/
├── .claude-plugin/           # Claude Code 插件配置
│   └── manifest.json         # 插件清单文件
├── skills/                   # 技能定义目录
│   └── financial-analysis/   # 财务分析技能
│       └── SKILL.md          # 技能说明文件
├── spec/                     # 规范文档
│   ├── SPECIFICATION.md      # 技能规范
│   └── AGENT_SKILLS_FORMAT.md # 格式说明
├── financial_analyzer/       # 核心代码
│   ├── __init__.py
│   ├── analyzers/
│   ├── indicators/
│   ├── parsers/
│   └── reports/
├── requirements.txt          # Python依赖
└── README.md                 # 项目说明
```

## SKILL.md 格式

每个技能都需要一个 `SKILL.md` 文件，包含：

### 1. YAML Frontmatter

```yaml
---
name: skill-name           # 技能标识符（小写，用连字符分隔）
description: 技能描述      # 完整描述技能用途和使用场景
---
```

### 2. Markdown 内容

SKILL.md 的主体内容应包含：

1. **概述** - 技能功能简介
2. **何时使用** - 触发此技能的场景描述
3. **核心功能** - 功能模块说明和代码示例
4. **使用方法** - 详细的使用教程
5. **参数说明** - API参数文档
6. **示例** - 典型使用场景
7. **注意事项** - 限制和警告

## manifest.json 格式

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "插件描述",
  "displayName": "显示名称",
  "author": "作者",
  "license": "MIT",
  "keywords": ["关键词"],
  "plugins": [
    {
      "id": "skill-id",
      "name": "Skill Name",
      "description": "技能描述",
      "skillsDir": "skills/skill-folder"
    }
  ],
  "requirements": {
    "python": ">=3.9",
    "packages": ["package>=version"]
  }
}
```

## 在 Claude Code 中使用

### 方法1: 通过插件市场安装

```bash
# 添加插件市场
/plugin marketplace add your-username/agent_skills

# 安装技能
/plugin install financial-analysis@your-marketplace
```

### 方法2: 直接安装

```bash
/plugin install path/to/agent_skills
```

### 方法3: 手动加载

将技能文件夹添加到 Claude Code 的技能目录中。

## 技能触发

安装技能后，Claude Code 会根据用户请求自动识别并使用相应技能：

- 用户说 "分析这份财报" → 自动触发 financial-analysis 技能
- 用户说 "计算ROE和ROA" → 自动触发财务指标计算功能

## 最佳实践

1. **技能描述要精确** - 帮助Claude准确判断何时使用此技能
2. **提供丰富示例** - 包含多种使用场景的代码示例
3. **错误处理文档化** - 说明可能的错误和处理方式
4. **保持模块化** - 每个技能专注于特定领域
5. **版本管理** - 使用语义化版本号

## 参考资料

- [Agent Skills 官方文档](https://agentskills.io)
- [anthropics/skills GitHub](https://github.com/anthropics/skills)
- [Claude Code 文档](https://claude.ai/docs)
