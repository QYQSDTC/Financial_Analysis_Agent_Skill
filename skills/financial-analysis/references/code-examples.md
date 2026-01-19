# 代码示例参考

## 从 PDF 内容提取财务数据

```python
def parse_financial_data_from_text(pdf_text: str) -> dict:
    """
    从 PDF 提取的文本中解析财务数据
    
    Args:
        pdf_text: Claude 官方 pdf skill 提取的文本内容
        
    Returns:
        包含 balance_sheet, income_statement, cashflow_statement 的字典
    """
    import re
    
    # 定义关键财务项目的匹配模式
    patterns = {
        # 资产负债表
        'total_assets': r'总资产[：:]\s*([\d,，.]+)',
        'current_assets': r'流动资产[：:]\s*([\d,，.]+)',
        'cash_and_equivalents': r'货币资金[：:]\s*([\d,，.]+)',
        'accounts_receivable': r'应收账款[：:]\s*([\d,，.]+)',
        'inventory': r'存货[：:]\s*([\d,，.]+)',
        'total_liabilities': r'总负债[：:]\s*([\d,，.]+)',
        'current_liabilities': r'流动负债[：:]\s*([\d,，.]+)',
        'shareholders_equity': r'股东权益[：:]\s*([\d,，.]+)',
        
        # 利润表
        'operating_revenue': r'营业收入[：:]\s*([\d,，.]+)',
        'operating_cost': r'营业成本[：:]\s*([\d,，.]+)',
        'operating_profit': r'营业利润[：:]\s*([\d,，.]+)',
        'net_profit': r'净利润[：:]\s*([\d,，.]+)',
        
        # 现金流量表
        'operating_cashflow': r'经营活动.*?现金流量净额[：:]\s*([-\d,，.]+)',
        'investing_cashflow': r'投资活动.*?现金流量净额[：:]\s*([-\d,，.]+)',
        'financing_cashflow': r'筹资活动.*?现金流量净额[：:]\s*([-\d,，.]+)',
    }
    
    data = {'balance_sheet': {}, 'income_statement': {}, 'cashflow_statement': {}}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, pdf_text)
        if match:
            value_str = match.group(1).replace(',', '').replace('，', '')
            try:
                value = float(value_str)
                # 根据 key 分类存储
                if key in ['total_assets', 'current_assets', 'cash_and_equivalents', 
                           'accounts_receivable', 'inventory', 'total_liabilities',
                           'current_liabilities', 'shareholders_equity']:
                    data['balance_sheet'][key] = value
                elif key in ['operating_revenue', 'operating_cost', 'operating_profit', 'net_profit']:
                    data['income_statement'][key] = value
                else:
                    data['cashflow_statement'][key] = value
            except ValueError:
                pass
    
    return data
```

## 完整分析流程

```python
"""
完整的财务分析流程
"""
from scripts.calculator import FinancialIndicatorCalculator
from scripts.financial_analyzer import FinancialAnalyzer
from scripts.report_generator import AnalysisReportGenerator

def analyze_financial_report(
    pdf_content: str,  # 由 Claude 读取的 PDF 内容
    company_name: str,
    report_period: str,
    report_type: str = "年报",
    stock_price: float = None
):
    """
    完整的财务报表分析流程
    """
    
    # Step 1: 从 PDF 内容解析财务数据
    data = parse_financial_data_from_text(pdf_content)
    
    # Step 2: 计算财务指标
    calculator = FinancialIndicatorCalculator()
    indicators = calculator.calculate_all_indicators(
        balance_sheet=data['balance_sheet'],
        income_statement=data['income_statement'],
        cashflow_statement=data['cashflow_statement'],
        metadata={'company_name': company_name}
    )
    
    # Step 3: 专业财务分析
    analyzer = FinancialAnalyzer()
    analysis = analyzer.analyze_financial_health(
        company_name=company_name,
        indicators=indicators,
        report_type=report_type,
        report_period=report_period
    )
    
    # Step 4: 生成投资建议
    recommendation = analyzer.generate_investment_recommendation(
        analysis=analysis,
        indicators=indicators,
        stock_price=stock_price,
        target_investor_type="稳健型"
    )
    
    # Step 5: 生成报告
    report_generator = AnalysisReportGenerator()
    
    md_path = f"{company_name}_{report_period}_分析报告.md"
    report_generator.generate_markdown_report(
        company_name=company_name,
        report_period=report_period,
        report_type=report_type,
        statement_data=data,
        indicators=indicators,
        analysis=analysis,
        recommendation=recommendation,
        output_path=md_path
    )
    
    excel_path = f"{company_name}_{report_period}_数据.xlsx"
    report_generator.generate_excel_report(
        company_name=company_name,
        report_period=report_period,
        statement_data=data,
        indicators=indicators,
        output_path=excel_path
    )
    
    return {
        'data': data,
        'indicators': indicators,
        'analysis': analysis,
        'recommendation': recommendation,
        'report_path': md_path,
        'excel_path': excel_path
    }
```

## 直接使用已有数据

如果用户已经有提取好的财务数据（如从 Wind、同花顺等导出），可以直接传入：

```python
# 直接使用已有数据
balance_sheet = {
    'total_assets': 100000000,
    'current_assets': 50000000,
    'cash_and_equivalents': 20000000,
    'accounts_receivable': 15000000,
    'inventory': 10000000,
    'total_liabilities': 40000000,
    'current_liabilities': 25000000,
    'shareholders_equity': 60000000,
}

income_statement = {
    'operating_revenue': 80000000,
    'operating_cost': 50000000,
    'operating_profit': 25000000,
    'net_profit': 20000000,
}

cashflow_statement = {
    'operating_cashflow': 22000000,
    'investing_cashflow': -5000000,
    'financing_cashflow': -3000000,
}
```
