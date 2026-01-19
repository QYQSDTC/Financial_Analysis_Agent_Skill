# Financial Analysis Skill 规范

## 1. 技能概述

### 1.1 技能标识

| 属性 | 值 |
|------|-----|
| 名称 | financial-analysis |
| 版本 | 1.0.0 |
| 类型 | 数据分析 / 金融 |
| 语言 | Python 3.9+ |

### 1.2 功能范围

此技能提供以下核心功能：

1. **PDF财报解析** - 从PDF格式的财务报告中提取结构化数据
2. **财务指标计算** - 计算盈利能力、偿债能力、运营能力、现金流质量等指标
3. **深度财务分析** - 基于AI进行专业财务健康评估
4. **投资建议生成** - 根据财务状况生成投资评级和操作建议
5. **报告生成** - 输出Markdown和Excel格式的专业分析报告

## 2. 数据结构

### 2.1 FinancialStatement

```python
@dataclass
class FinancialStatement:
    company_name: str      # 公司名称
    report_period: str     # 报告期 (YYYY-MM-DD)
    report_type: str       # 报告类型: 季报/半年报/年报
    balance_sheet: Dict[str, float]      # 资产负债表
    income_statement: Dict[str, float]   # 利润表
    cashflow_statement: Dict[str, float] # 现金流量表
    metadata: Dict[str, any]             # 元数据
```

### 2.2 资产负债表字段 (balance_sheet)

| 字段名 | 中文名 | 类型 |
|--------|--------|------|
| total_assets | 总资产 | float |
| current_assets | 流动资产 | float |
| cash_and_equivalents | 货币资金 | float |
| accounts_receivable | 应收账款 | float |
| inventory | 存货 | float |
| fixed_assets | 固定资产 | float |
| total_liabilities | 总负债 | float |
| current_liabilities | 流动负债 | float |
| short_term_debt | 短期借款 | float |
| accounts_payable | 应付账款 | float |
| long_term_debt | 长期借款 | float |
| shareholders_equity | 股东权益 | float |

### 2.3 利润表字段 (income_statement)

| 字段名 | 中文名 | 类型 |
|--------|--------|------|
| operating_revenue | 营业收入 | float |
| operating_cost | 营业成本 | float |
| operating_profit | 营业利润 | float |
| total_profit | 利润总额 | float |
| net_profit | 净利润 | float |
| net_profit_attributable | 归母净利润 | float |
| selling_expenses | 销售费用 | float |
| administrative_expenses | 管理费用 | float |
| financial_expenses | 财务费用 | float |
| rd_expenses | 研发费用 | float |
| basic_eps | 基本每股收益 | float |

### 2.4 现金流量表字段 (cashflow_statement)

| 字段名 | 中文名 | 类型 |
|--------|--------|------|
| operating_cashflow | 经营活动现金流净额 | float |
| investing_cashflow | 投资活动现金流净额 | float |
| financing_cashflow | 筹资活动现金流净额 | float |
| net_cashflow | 现金净增加额 | float |
| cash_from_sales | 销售收到的现金 | float |
| cash_for_purchases | 购买支付的现金 | float |

## 3. 财务指标定义

### 3.1 盈利能力指标 (profitability)

| 指标 | 计算公式 | 说明 |
|------|---------|------|
| gross_margin | (营业收入 - 营业成本) / 营业收入 × 100% | 毛利率 |
| operating_margin | 营业利润 / 营业收入 × 100% | 营业利润率 |
| net_margin | 净利润 / 营业收入 × 100% | 净利率 |
| roe | 净利润 / 股东权益 × 100% | 净资产收益率 |
| roa | 净利润 / 总资产 × 100% | 总资产收益率 |
| roic | 税后营业利润 / 投入资本 × 100% | 投入资本回报率 |

### 3.2 偿债能力指标 (solvency)

| 指标 | 计算公式 | 说明 |
|------|---------|------|
| current_ratio | 流动资产 / 流动负债 | 流动比率 |
| quick_ratio | (流动资产 - 存货) / 流动负债 | 速动比率 |
| cash_ratio | 货币资金 / 流动负债 | 现金比率 |
| debt_to_asset | 总负债 / 总资产 × 100% | 资产负债率 |
| debt_to_equity | 总负债 / 股东权益 × 100% | 产权比率 |
| interest_coverage | (利润总额 + 财务费用) / 财务费用 | 利息保障倍数 |
| equity_multiplier | 总资产 / 股东权益 | 权益乘数 |

### 3.3 运营能力指标 (operational)

| 指标 | 计算公式 | 说明 |
|------|---------|------|
| asset_turnover | 营业收入 / 总资产 | 总资产周转率 |
| receivables_turnover | 营业收入 / 应收账款 | 应收账款周转率 |
| receivables_days | 365 / 应收账款周转率 | 应收账款周转天数 |
| inventory_turnover | 营业成本 / 存货 | 存货周转率 |
| inventory_days | 365 / 存货周转率 | 存货周转天数 |
| payables_turnover | 营业成本 / 应付账款 | 应付账款周转率 |
| payables_days | 365 / 应付账款周转率 | 应付账款周转天数 |
| operating_cycle | 应收账款周转天数 + 存货周转天数 | 营业周期 |
| cash_conversion_cycle | 营业周期 - 应付账款周转天数 | 现金循环周期 |

### 3.4 现金流质量指标 (cashflow_quality)

| 指标 | 计算公式 | 说明 |
|------|---------|------|
| operating_cf_to_revenue | 经营现金流 / 营业收入 × 100% | 销售现金比率 |
| operating_cf_to_net_profit | 经营现金流 / 净利润 × 100% | 现金净利比 |
| free_cashflow | 经营现金流 + 投资现金流 | 自由现金流 |
| fcf_to_revenue | 自由现金流 / 营业收入 × 100% | 自由现金流比率 |

### 3.5 估值指标 (valuation)

| 指标 | 计算公式 | 说明 |
|------|---------|------|
| eps | 净利润 / 总股本 | 每股收益 |
| bvps | 股东权益 / 总股本 | 每股净资产 |

## 4. 评分体系

### 4.1 评分权重

| 维度 | 权重 |
|------|------|
| 盈利能力 | 35% |
| 偿债能力 | 25% |
| 运营能力 | 20% |
| 现金流质量 | 20% |

### 4.2 综合评级标准

| 综合评分 | 评级 |
|---------|------|
| ≥85 | 优秀 |
| 70-84 | 良好 |
| 60-69 | 一般 |
| 50-59 | 较差 |
| <50 | 差 |

### 4.3 投资评级标准

| 条件 | 投资评级 |
|------|---------|
| 综合评级=优秀 且 风险数≤1 | 强烈推荐 |
| 综合评级=优秀/良好 且 风险数≤2 | 推荐 |
| 综合评级=一般 或 (良好且风险数>2) | 中性 |
| 综合评级=较差 | 不推荐 |
| 综合评级=差 | 强烈不推荐 |

## 5. API接口

### 5.1 FinancialReportParser

```python
class FinancialReportParser:
    def parse_pdf(pdf_path: str) -> FinancialStatement
    def export_to_dataframe() -> pd.DataFrame
```

### 5.2 FinancialIndicatorCalculator

```python
class FinancialIndicatorCalculator:
    def calculate_all_indicators(
        balance_sheet: Dict,
        income_statement: Dict,
        cashflow_statement: Dict,
        metadata: Dict = None
    ) -> Dict[str, Dict]
    
    def calculate_profitability(...) -> Dict[str, float]
    def calculate_solvency(...) -> Dict[str, float]
    def calculate_operational_efficiency(...) -> Dict[str, float]
    def calculate_cashflow_quality(...) -> Dict[str, float]
    def calculate_valuation_metrics(...) -> Dict[str, float]
    def get_summary() -> Dict
```

### 5.3 FinancialAnalyzer

```python
class FinancialAnalyzer:
    def __init__(api_key: str = None)
    
    def analyze_financial_health(
        company_name: str,
        indicators: Dict,
        report_type: str,
        report_period: str
    ) -> Dict
    
    def generate_investment_recommendation(
        analysis: Dict,
        indicators: Dict,
        stock_price: float = None,
        target_investor_type: str = "稳健型"
    ) -> Dict
```

### 5.4 AnalysisReportGenerator

```python
class AnalysisReportGenerator:
    def generate_markdown_report(
        company_name: str,
        report_period: str,
        report_type: str,
        statement_data: Dict,
        indicators: Dict,
        analysis: Dict,
        recommendation: Dict,
        output_path: str = None
    ) -> str
    
    def generate_excel_report(
        company_name: str,
        report_period: str,
        statement_data: Dict,
        indicators: Dict,
        output_path: str
    ) -> None
    
    def generate_summary_dataframe(...) -> pd.DataFrame
```

## 6. 错误处理

### 6.1 常见错误

| 错误类型 | 原因 | 处理方式 |
|---------|------|---------|
| FileNotFoundError | PDF文件不存在 | 检查文件路径 |
| PDFParseError | PDF格式不支持 | 尝试转换格式 |
| APIKeyError | API密钥无效 | 使用基础分析模式 |
| DataExtractionError | 无法提取数据 | 检查PDF内容 |

### 6.2 降级策略

- 如果AI分析不可用（无API密钥），自动切换到基础分析模式
- 如果部分数据缺失，跳过相关指标计算
- 如果报表格式异常，返回部分解析结果

## 7. 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0.0 | 2025-01 | 初始版本，支持基本财报分析功能 |

## 8. 许可证

MIT License
