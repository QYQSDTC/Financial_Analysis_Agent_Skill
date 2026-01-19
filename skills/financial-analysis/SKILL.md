---
name: financial-analysis
description: 专业的上市公司财务报表分析技能。用于分析PDF格式的财务报告（季报、半年报、年报），提取三大报表数据，计算盈利能力、偿债能力、运营能力、现金流质量等多维度财务指标，进行深度财务分析，并生成投资评级和建议。支持生成Markdown和Excel格式的专业分析报告。当用户请求分析财报、计算ROE/ROA等财务指标、评估公司财务健康状况、生成投资建议时使用此技能。
---

# 财务报表分析技能

专业的上市公司财务报表分析工具，支持：
- 读取PDF财务报告并提取三大报表数据
- 计算20+核心财务指标（盈利、偿债、运营、现金流）
- 生成综合评分和投资评级
- 输出Markdown和Excel格式分析报告

## 分析流程

当用户提供财报PDF时，按以下流程执行：

1. **读取PDF** - 使用 Read 工具读取PDF文件内容
2. **提取数据** - 从文本中识别资产负债表、利润表、现金流量表数据
3. **计算指标** - 使用 `scripts/calculator.py` 计算财务指标
4. **深度分析** - 使用 `scripts/financial_analyzer.py` 进行专业分析
5. **生成报告** - 使用 `scripts/report_generator.py` 生成报告

## 核心脚本

### 指标计算器 (`scripts/calculator.py`)

```python
from scripts.calculator import FinancialIndicatorCalculator

calculator = FinancialIndicatorCalculator()
indicators = calculator.calculate_all_indicators(
    balance_sheet=balance_sheet_data,
    income_statement=income_statement_data,
    cashflow_statement=cashflow_statement_data,
    metadata={'company_name': '公司名称'}
)

# 获取评分摘要
summary = calculator.get_summary()
# 返回: {'综合评分': 85.5, '盈利能力评分': 90, '偿债能力评分': 80, ...}
```

### 财务分析器 (`scripts/financial_analyzer.py`)

```python
from scripts.financial_analyzer import FinancialAnalyzer

analyzer = FinancialAnalyzer()
analysis = analyzer.analyze_financial_health(
    company_name="公司名称",
    indicators=indicators,
    report_type="年报",
    report_period="2023-12-31"
)
# 返回: overall_rating, strengths, weaknesses, risks, opportunities, detailed_analysis

recommendation = analyzer.generate_investment_recommendation(
    analysis=analysis,
    indicators=indicators,
    stock_price=25.8,  # 可选
    target_investor_type="稳健型"
)
# 返回: rating, action, target_price, entry_price, stop_loss, reasons
```

### 报告生成器 (`scripts/report_generator.py`)

```python
from scripts.report_generator import AnalysisReportGenerator

generator = AnalysisReportGenerator()

# Markdown报告
generator.generate_markdown_report(
    company_name="公司名称",
    report_period="2023-12-31",
    report_type="年报",
    statement_data=data,
    indicators=indicators,
    analysis=analysis,
    recommendation=recommendation,
    output_path="分析报告.md"
)

# Excel报告
generator.generate_excel_report(
    company_name="公司名称",
    report_period="2023-12-31",
    statement_data=data,
    indicators=indicators,
    output_path="财务数据.xlsx"
)
```

## 数据结构

### 资产负债表 (balance_sheet)

```python
{
    'total_assets': 100000000,        # 总资产
    'current_assets': 50000000,       # 流动资产
    'cash_and_equivalents': 20000000, # 货币资金
    'accounts_receivable': 15000000,  # 应收账款
    'inventory': 10000000,            # 存货
    'total_liabilities': 40000000,    # 总负债
    'current_liabilities': 25000000,  # 流动负债
    'shareholders_equity': 60000000,  # 股东权益
}
```

### 利润表 (income_statement)

```python
{
    'operating_revenue': 80000000,  # 营业收入
    'operating_cost': 50000000,     # 营业成本
    'operating_profit': 25000000,   # 营业利润
    'net_profit': 20000000,         # 净利润
}
```

### 现金流量表 (cashflow_statement)

```python
{
    'operating_cashflow': 22000000,   # 经营活动现金流
    'investing_cashflow': -5000000,   # 投资活动现金流
    'financing_cashflow': -3000000,   # 筹资活动现金流
}
```

## 参考文档

- **详细代码示例**: 见 [references/code-examples.md](references/code-examples.md)
- **评分标准**: 见 [references/scoring-standards.md](references/scoring-standards.md)

## 依赖

```bash
pip install pandas numpy openpyxl matplotlib seaborn openai
```

## 注意事项

1. **数据准确性**: 解析结果依赖PDF质量，建议人工复核关键数据
2. **行业差异**: 不同行业的财务指标标准差异较大，分析时需考虑行业特点
3. **投资风险**: 本工具仅供参考，不构成投资建议
