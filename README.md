# 财务报表分析助手 - Agent Skill

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-blue)](https://github.com/anthropics/skills)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

专业的上市公司财务报表分析工具，支持季报、半年报和年报的智能解析与投资分析。

**此仓库遵循 [anthropics/skills](https://github.com/anthropics/skills) 规范，可直接在 Claude Code 中作为 Agent Skill 使用。**

---

## 🚀 在 Claude Code 中使用

### 方法1: 作为插件安装（推荐）

```bash
# 在 Claude Code 中运行
/plugin install /path/to/agent_skills
```

安装后，直接在对话中说：
```
"帮我分析这份财报：/path/to/report.pdf"
```

Claude 会自动调用 financial-analysis 技能进行分析。

### 方法2: 将技能复制到 Claude 技能目录

将 `skills/financial-analysis/SKILL.md` 复制到 Claude 的技能目录。

### 方法3: 手动调用

在 Claude Code 对话中直接引用技能：
```
使用 financial-analysis 技能分析 ~/Downloads/某公司年报.pdf
```

---

## 功能特性

### 1. 智能PDF解析
- 自动识别并提取PDF格式财报中的关键数据
- 支持资产负债表、利润表、现金流量表三大报表
- 智能识别公司名称、报告期、报告类型等元数据

### 2. 多维度财务指标计算
- **盈利能力分析**: ROE、ROA、ROIC、毛利率、净利率等
- **偿债能力分析**: 流动比率、速动比率、资产负债率、利息保障倍数等
- **运营能力分析**: 资产周转率、应收账款周转率、存货周转率、现金循环周期等
- **现金流质量分析**: 销售现金比率、现金净利比、自由现金流等
- **估值指标**: EPS、每股净资产等

### 3. 专业财务分析
- AI驱动的深度财务分析（基于Claude）
- 自动识别公司优势、劣势、风险和机会
- 综合评分系统（盈利能力、偿债能力、运营能力、现金流质量）
- 行业对比分析能力

### 4. 投资建议生成
- 基于财务指标的投资评级（强烈推荐/推荐/中性/不推荐/强烈不推荐）
- 针对不同风险偏好投资者的定制化建议
- 目标价、建议买入价、止损价计算

### 5. 多格式报告输出
- Markdown格式专业分析报告
- Excel格式数据导出
- 便于多期对比的DataFrame格式

---

## 📁 项目结构

```
agent_skills/
├── .claude-plugin/              # Claude Code 插件配置
│   └── manifest.json            # 插件清单
├── skills/                      # Agent Skills 定义
│   └── financial-analysis/      # 财务分析技能
│       └── SKILL.md             # 技能说明文件
├── spec/                        # 规范文档
│   ├── SPECIFICATION.md         # 技能规范
│   └── AGENT_SKILLS_FORMAT.md   # 格式说明
├── financial_analyzer/          # 核心分析模块
│   ├── __init__.py
│   ├── analyzers/               # 分析器
│   │   └── financial_analyzer.py
│   ├── indicators/              # 指标计算
│   │   └── calculator.py
│   ├── parsers/                 # PDF解析
│   │   └── pdf_parser.py
│   └── reports/                 # 报告生成
│       └── report_generator.py
├── example.py                   # 使用示例
├── analyze-report               # 命令行工具
├── requirements.txt             # Python依赖
├── README.md                    # 项目说明
└── USAGE.md                     # 使用指南
```

---

## 安装依赖

```bash
pip install -r requirements.txt
```

requirements.txt:
```
PyPDF2>=3.0.0
pdfplumber>=0.10.0
pandas>=2.0.0
numpy>=1.24.0
anthropic>=0.18.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.1.0
```

---

## 快速开始

### 基本用法

```python
from financial_analyzer import (
    FinancialReportParser,
    FinancialIndicatorCalculator,
    FinancialAnalyzer,
    AnalysisReportGenerator
)

# 1. 解析PDF财报
parser = FinancialReportParser()
statement = parser.parse_pdf("财报.pdf")

# 2. 计算财务指标
calculator = FinancialIndicatorCalculator()
indicators = calculator.calculate_all_indicators(
    balance_sheet=statement.balance_sheet,
    income_statement=statement.income_statement,
    cashflow_statement=statement.cashflow_statement,
    metadata=statement.metadata
)

# 3. 专业财务分析
analyzer = FinancialAnalyzer(api_key="your_anthropic_api_key")
analysis = analyzer.analyze_financial_health(
    company_name=statement.company_name,
    indicators=indicators,
    report_type=statement.report_type,
    report_period=statement.report_period
)

# 4. 生成投资建议
recommendation = analyzer.generate_investment_recommendation(
    analysis=analysis,
    indicators=indicators,
    stock_price=25.8,  # 当前股价（可选）
    target_investor_type="稳健型"
)

# 5. 生成分析报告
report_generator = AnalysisReportGenerator()
markdown_report = report_generator.generate_markdown_report(
    company_name=statement.company_name,
    report_period=statement.report_period,
    report_type=statement.report_type,
    statement_data={
        'balance_sheet': statement.balance_sheet,
        'income_statement': statement.income_statement,
        'cashflow_statement': statement.cashflow_statement,
    },
    indicators=indicators,
    analysis=analysis,
    recommendation=recommendation,
    output_path="财务分析报告.md"
)

print(markdown_report)
```

### 命令行使用

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

---

## 完整示例

```python
#!/usr/bin/env python3
"""完整的财务分析流程示例"""

import os
from financial_analyzer import (
    FinancialReportParser,
    FinancialIndicatorCalculator,
    FinancialAnalyzer,
    AnalysisReportGenerator
)

def analyze_financial_report(pdf_path: str, stock_price: float = None):
    """完整的财务报表分析流程"""
    print("=" * 60)
    print("财务报表智能分析系统")
    print("=" * 60)

    # Step 1: 解析PDF
    print("\n[1/5] 正在解析PDF财报...")
    parser = FinancialReportParser()
    statement = parser.parse_pdf(pdf_path)
    print(f"✓ 解析完成: {statement.company_name} - {statement.report_period}")

    # Step 2: 计算指标
    print("\n[2/5] 正在计算财务指标...")
    calculator = FinancialIndicatorCalculator()
    indicators = calculator.calculate_all_indicators(
        balance_sheet=statement.balance_sheet,
        income_statement=statement.income_statement,
        cashflow_statement=statement.cashflow_statement,
        metadata=statement.metadata
    )

    # 获取评分摘要
    summary = calculator.get_summary()
    print(f"✓ 指标计算完成")
    print(f"  - 盈利能力评分: {summary.get('盈利能力评分', 'N/A')}")
    print(f"  - 偿债能力评分: {summary.get('偿债能力评分', 'N/A')}")
    print(f"  - 运营能力评分: {summary.get('运营能力评分', 'N/A')}")
    print(f"  - 现金流质量评分: {summary.get('现金流质量评分', 'N/A')}")
    print(f"  - 综合评分: {summary.get('综合评分', 'N/A')}")

    # Step 3: 专业分析
    print("\n[3/5] 正在进行专业财务分析...")
    analyzer = FinancialAnalyzer()  # API密钥从环境变量读取
    analysis = analyzer.analyze_financial_health(
        company_name=statement.company_name,
        indicators=indicators,
        report_type=statement.report_type,
        report_period=statement.report_period
    )
    print(f"✓ 分析完成")
    print(f"  - 综合评级: {analysis['overall_rating']}")
    print(f"  - 发现 {len(analysis['strengths'])} 项优势")
    print(f"  - 发现 {len(analysis['weaknesses'])} 项劣势")
    print(f"  - 识别 {len(analysis['risks'])} 项风险")

    # Step 4: 生成投资建议
    print("\n[4/5] 正在生成投资建议...")
    recommendation = analyzer.generate_investment_recommendation(
        analysis=analysis,
        indicators=indicators,
        stock_price=stock_price,
        target_investor_type="稳健型"
    )
    print(f"✓ 投资建议生成完成")
    print(f"  - 投资评级: {recommendation['rating']}")
    print(f"  - 操作建议: {recommendation['action']}")
    if recommendation.get('target_price'):
        print(f"  - 目标价: {recommendation['target_price']} 元")

    # Step 5: 生成报告
    print("\n[5/5] 正在生成分析报告...")
    report_generator = AnalysisReportGenerator()

    # 生成Markdown报告
    md_path = f"{statement.company_name}_{statement.report_period}_分析报告.md"
    report_generator.generate_markdown_report(
        company_name=statement.company_name,
        report_period=statement.report_period,
        report_type=statement.report_type,
        statement_data={
            'balance_sheet': statement.balance_sheet,
            'income_statement': statement.income_statement,
            'cashflow_statement': statement.cashflow_statement,
        },
        indicators=indicators,
        analysis=analysis,
        recommendation=recommendation,
        output_path=md_path
    )

    # 生成Excel报告
    excel_path = f"{statement.company_name}_{statement.report_period}_财务数据.xlsx"
    report_generator.generate_excel_report(
        company_name=statement.company_name,
        report_period=statement.report_period,
        statement_data={
            'balance_sheet': statement.balance_sheet,
            'income_statement': statement.income_statement,
            'cashflow_statement': statement.cashflow_statement,
        },
        indicators=indicators,
        output_path=excel_path
    )

    print(f"✓ 报告生成完成")
    print(f"  - Markdown报告: {md_path}")
    print(f"  - Excel数据: {excel_path}")

    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)

    return {
        'statement': statement,
        'indicators': indicators,
        'analysis': analysis,
        'recommendation': recommendation
    }

if __name__ == "__main__":
    # 分析财报
    result = analyze_financial_report(
        pdf_path="示例公司_2023年报.pdf",
        stock_price=25.8
    )
```

---

## 高级用法

### 多期对比分析

```python
from financial_analyzer import FinancialReportParser, FinancialIndicatorCalculator
import pandas as pd

# 解析多期财报
periods = ['2023Q1', '2023Q2', '2023Q3', '2023Q4']
results = []

for period_file in ['Q1.pdf', 'Q2.pdf', 'Q3.pdf', 'Q4.pdf']:
    parser = FinancialReportParser()
    statement = parser.parse_pdf(period_file)

    calculator = FinancialIndicatorCalculator()
    indicators = calculator.calculate_all_indicators(
        balance_sheet=statement.balance_sheet,
        income_statement=statement.income_statement,
        cashflow_statement=statement.cashflow_statement
    )

    results.append({
        'period': statement.report_period,
        'roe': indicators['profitability'].get('roe', 0),
        'net_margin': indicators['profitability'].get('net_margin', 0),
        'current_ratio': indicators['solvency'].get('current_ratio', 0),
    })

# 对比分析
df = pd.DataFrame(results)
print(df)

# 计算增长率
df['roe_growth'] = df['roe'].pct_change() * 100
print(f"\nROE同比增长率:\n{df[['period', 'roe_growth']]}")
```

### 自定义评分标准

```python
from financial_analyzer.indicators import FinancialIndicatorCalculator

class CustomIndicatorCalculator(FinancialIndicatorCalculator):
    """自定义评分标准"""

    def _score_profitability(self):
        """根据行业特点自定义盈利能力评分"""
        # 例如：对科技行业使用更高的ROE标准
        prof = self.indicators['profitability']
        score = 0

        roe = prof.get('roe', 0)
        if roe >= 25:  # 科技行业高标准
            score += 30
        elif roe >= 18:
            score += 25
        # ... 其他评分逻辑

        return score

# 使用自定义计算器
calculator = CustomIndicatorCalculator()
indicators = calculator.calculate_all_indicators(...)
```

---

## 核心模块说明

### 1. FinancialReportParser
PDF财报解析器，负责从PDF中提取结构化数据。

**主要方法**:
- `parse_pdf(pdf_path)`: 解析PDF财报
- `export_to_dataframe()`: 导出为DataFrame

### 2. FinancialIndicatorCalculator
财务指标计算器，计算各类财务比率和指标。

**主要方法**:
- `calculate_all_indicators()`: 计算所有指标
- `calculate_profitability()`: 计算盈利能力指标
- `calculate_solvency()`: 计算偿债能力指标
- `calculate_operational_efficiency()`: 计算运营能力指标
- `calculate_cashflow_quality()`: 计算现金流质量指标
- `get_summary()`: 获取评分摘要

### 3. FinancialAnalyzer
专业财务分析器，基于AI进行深度分析。

**主要方法**:
- `analyze_financial_health()`: 综合分析财务健康状况
- `generate_investment_recommendation()`: 生成投资建议

### 4. AnalysisReportGenerator
分析报告生成器，输出多种格式报告。

**主要方法**:
- `generate_markdown_report()`: 生成Markdown报告
- `generate_excel_report()`: 生成Excel报告
- `generate_summary_dataframe()`: 生成摘要DataFrame

---

## 环境变量配置

```bash
# Anthropic API密钥（用于AI深度分析）
export ANTHROPIC_API_KEY="your_api_key_here"
```

如果不配置API密钥，系统将使用基础分析模式，不影响核心功能。

---

## 注意事项

1. **PDF格式兼容性**: 目前支持标准格式的上市公司财报PDF，对于扫描版或特殊格式的PDF可能需要额外处理
2. **数据准确性**: 解析结果依赖PDF质量，建议人工复核关键数据
3. **行业差异**: 不同行业的财务指标标准差异较大，建议根据行业特点调整评分标准
4. **投资风险**: 本工具仅供参考，不构成投资建议，投资需谨慎

---

## 未来规划

- [ ] 支持更多PDF格式和布局
- [ ] 增加OCR支持以处理扫描版PDF
- [ ] 添加行业对比数据库
- [ ] 支持批量分析和趋势预测
- [ ] 增加可视化图表生成
- [ ] 支持实时股价数据接入
- [ ] 添加更多估值模型（DCF、DDM等）

---

## 许可证

MIT License

---

## 相关链接

- [Agent Skills 官方规范](https://agentskills.io)
- [anthropics/skills GitHub](https://github.com/anthropics/skills)
- [Claude Code 文档](https://claude.ai/docs)

---

## 联系方式

如有问题或建议，欢迎反馈。
