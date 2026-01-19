# 财务分析工具使用指南

## 安装

### 1. 安装依赖
```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Development/agent_skills
pip install -r requirements.txt
```

### 2. 添加到 PATH（可选，方便全局使用）
```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加：
export PATH="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Development/agent_skills:$PATH"

# 然后重新加载配置
source ~/.zshrc  # 或 source ~/.bashrc
```

## 使用方式

### 方式 1: 在 Claude Code 对话中直接使用

在 Claude Code 中直接说：
```
"帮我分析这个财报：/path/to/report.pdf，当前股价是 25.8 元"
```

我会自动调用 financial_analyzer 工具完成分析。

### 方式 2: 使用命令行工具

```bash
# 基本用法
./analyze-report 财报.pdf

# 指定股价
./analyze-report 财报.pdf --price 25.8

# 指定投资者类型
./analyze-report 财报.pdf --price 25.8 --investor-type 稳健型

# 指定输出目录
./analyze-report 财报.pdf --output-dir ./reports
```

### 方式 3: 在 Python 代码中使用

```python
from financial_analyzer import (
    FinancialReportParser,
    FinancialIndicatorCalculator,
    FinancialAnalyzer,
    AnalysisReportGenerator
)

# 解析PDF
parser = FinancialReportParser()
statement = parser.parse_pdf("财报.pdf")

# 计算指标
calculator = FinancialIndicatorCalculator()
indicators = calculator.calculate_all_indicators(
    statement.balance_sheet,
    statement.income_statement,
    statement.cashflow_statement,
    statement.metadata
)

# 分析
analyzer = FinancialAnalyzer()
analysis = analyzer.analyze_financial_health(
    statement.company_name,
    indicators,
    statement.report_type,
    statement.report_period
)

# 投资建议
recommendation = analyzer.generate_investment_recommendation(
    analysis, indicators, stock_price=25.8
)
```

## 环境变量配置

### 启用 AI 深度分析（可选）
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

如果不设置，工具会使用基础分析模式，仍然可以正常工作。

## 示例

```bash
# 分析某公司2023年报
./analyze-report ~/Downloads/某公司_2023年报.pdf --price 28.5

# 输出示例：
# 🔍 开始分析财务报表...
# [1/5] 解析PDF财报
# [2/5] 计算财务指标
# [3/5] 进行专业分析
# [4/5] 生成投资建议
# [5/5] 生成分析报告
#
# ✅ 分析完成！
# 📊 某公司 - 年报
# 💯 综合评分: 78.5/100
# ⭐ 综合评级: 良好
# 📈 投资评级: 推荐
# 💡 操作建议: 买入
```

## 在 Claude Code 中的典型对话示例

```
你: "我有一份贵州茅台的2023年报PDF，帮我分析一下"

Claude: "好的，我来帮你分析贵州茅台的2023年报。
请提供PDF文件路径，我会：
1. 提取财务数据
2. 计算关键指标
3. 进行专业分析
4. 给出投资建议
5. 生成详细报告"

你: "文件在 ~/Downloads/贵州茅台_2023年报.pdf"

Claude: [自动调用工具进行分析，并返回详细结果]
```

## 文件说明

- `analyze-report` - 命令行快捷工具
- `financial_analyzer/` - 核心分析模块
- `example.py` - 完整使用示例
- `README.md` - 详细文档
- `requirements.txt` - 依赖包列表
