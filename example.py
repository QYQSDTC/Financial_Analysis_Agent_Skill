#!/usr/bin/env python3
"""
财务报表分析完整示例
演示如何使用财务分析助手分析上市公司财报
"""

import os
from financial_analyzer import (
    FinancialReportParser,
    FinancialIndicatorCalculator,
    FinancialAnalyzer,
    AnalysisReportGenerator
)


def analyze_financial_report(pdf_path: str, stock_price: float = None, api_key: str = None):
    """
    完整的财务报表分析流程

    Args:
        pdf_path: PDF财报路径
        stock_price: 当前股价（可选）
        api_key: Anthropic API密钥（可选，用于AI深度分析）
    """
    print("=" * 60)
    print("财务报表智能分析系统 v1.0")
    print("=" * 60)

    # Step 1: 解析PDF财报
    print("\n[1/5] 正在解析PDF财报...")
    parser = FinancialReportParser()
    statement = parser.parse_pdf(pdf_path)
    print(f"✓ 解析完成: {statement.company_name}")
    print(f"  - 报告期: {statement.report_period}")
    print(f"  - 报告类型: {statement.report_type}")

    # Step 2: 计算财务指标
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
    print(f"\n  各维度评分（满分100）:")
    print(f"  - 盈利能力评分: {summary.get('盈利能力评分', 'N/A'):.1f}")
    print(f"  - 偿债能力评分: {summary.get('偿债能力评分', 'N/A'):.1f}")
    print(f"  - 运营能力评分: {summary.get('运营能力评分', 'N/A'):.1f}")
    print(f"  - 现金流质量评分: {summary.get('现金流质量评分', 'N/A'):.1f}")
    print(f"  - 综合评分: {summary.get('综合评分', 'N/A'):.1f}")

    # 显示关键指标
    print(f"\n  关键财务指标:")
    if 'profitability' in indicators:
        prof = indicators['profitability']
        print(f"  - ROE: {prof.get('roe', 0):.2f}%")
        print(f"  - 毛利率: {prof.get('gross_margin', 0):.2f}%")
        print(f"  - 净利率: {prof.get('net_margin', 0):.2f}%")

    if 'solvency' in indicators:
        solv = indicators['solvency']
        print(f"  - 流动比率: {solv.get('current_ratio', 0):.2f}")
        print(f"  - 资产负债率: {solv.get('debt_to_asset', 0):.2f}%")

    # Step 3: 专业财务分析
    print("\n[3/5] 正在进行专业财务分析...")
    analyzer = FinancialAnalyzer(api_key=api_key)
    analysis = analyzer.analyze_financial_health(
        company_name=statement.company_name,
        indicators=indicators,
        report_type=statement.report_type,
        report_period=statement.report_period
    )
    print(f"✓ 分析完成")
    print(f"\n  财务健康状况评估:")
    print(f"  - 综合评级: {analysis['overall_rating']}")
    print(f"  - 发现 {len(analysis['strengths'])} 项优势")
    print(f"  - 发现 {len(analysis['weaknesses'])} 项劣势")
    print(f"  - 识别 {len(analysis['risks'])} 项风险")

    if analysis['strengths']:
        print(f"\n  主要优势:")
        for i, strength in enumerate(analysis['strengths'][:3], 1):
            print(f"    {i}. {strength}")

    if analysis['risks']:
        print(f"\n  主要风险:")
        for i, risk in enumerate(analysis['risks'][:3], 1):
            print(f"    {i}. ⚠️  {risk}")

    # Step 4: 生成投资建议
    print("\n[4/5] 正在生成投资建议...")
    recommendation = analyzer.generate_investment_recommendation(
        analysis=analysis,
        indicators=indicators,
        stock_price=stock_price,
        target_investor_type="稳健型"
    )
    print(f"✓ 投资建议生成完成")
    print(f"\n  投资建议:")
    print(f"  - 投资评级: {recommendation['rating']}")
    print(f"  - 操作建议: {recommendation['action']}")
    print(f"  - 目标投资者: {recommendation['target_investor']}")

    if stock_price and recommendation.get('target_price'):
        print(f"\n  价格参考:")
        print(f"  - 当前价格: {stock_price:.2f} 元")
        print(f"  - 目标价: {recommendation['target_price']:.2f} 元")
        print(f"  - 建议买入价: {recommendation['entry_price']:.2f} 元")
        print(f"  - 止损价: {recommendation['stop_loss']:.2f} 元")

        upside = ((recommendation['target_price'] - stock_price) / stock_price) * 100
        print(f"  - 上涨空间: {upside:.2f}%")

    # Step 5: 生成分析报告
    print("\n[5/5] 正在生成分析报告...")
    report_generator = AnalysisReportGenerator()

    # 生成Markdown报告
    md_filename = f"{statement.company_name}_{statement.report_period}_分析报告.md"
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
        output_path=md_filename
    )

    # 生成Excel报告
    excel_filename = f"{statement.company_name}_{statement.report_period}_财务数据.xlsx"
    report_generator.generate_excel_report(
        company_name=statement.company_name,
        report_period=statement.report_period,
        statement_data={
            'balance_sheet': statement.balance_sheet,
            'income_statement': statement.income_statement,
            'cashflow_statement': statement.cashflow_statement,
        },
        indicators=indicators,
        output_path=excel_filename
    )

    print(f"✓ 报告生成完成")
    print(f"\n  输出文件:")
    print(f"  - Markdown报告: {md_filename}")
    print(f"  - Excel数据: {excel_filename}")

    print("\n" + "=" * 60)
    print("分析完成！请查看生成的报告文件。")
    print("=" * 60)

    return {
        'statement': statement,
        'indicators': indicators,
        'analysis': analysis,
        'recommendation': recommendation
    }


def batch_analysis_example():
    """批量分析多期财报示例"""
    print("\n批量分析示例：分析公司多个季度的财报")
    print("-" * 60)

    # 模拟多期财报文件
    report_files = [
        ("2023Q1_report.pdf", "2023-03-31"),
        ("2023Q2_report.pdf", "2023-06-30"),
        ("2023Q3_report.pdf", "2023-09-30"),
        ("2023Q4_report.pdf", "2023-12-31"),
    ]

    results = []

    for pdf_file, period in report_files:
        print(f"\n正在分析 {period} 财报...")

        # 这里演示数据结构，实际使用时需要真实的PDF文件
        # result = analyze_financial_report(pdf_file)
        # results.append(result)

    print("\n多期对比分析完成！")
    print("可以使用pandas进行趋势分析和可视化")


if __name__ == "__main__":
    print("""
    财务报表分析助手 - 使用示例

    使用方法:
    1. 准备PDF格式的财报文件
    2. （可选）设置ANTHROPIC_API_KEY环境变量以启用AI深度分析
    3. 运行本脚本

    示例命令:
    python example.py
    """)

    # 检查是否有API密钥
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n⚠️  提示: 未检测到ANTHROPIC_API_KEY环境变量")
        print("将使用基础分析模式。如需AI深度分析，请设置API密钥。\n")

    # 示例1: 单个财报分析
    print("\n" + "=" * 60)
    print("示例 1: 单个财报分析")
    print("=" * 60)

    # 注意：这里需要替换为实际的PDF文件路径
    # result = analyze_financial_report(
    #     pdf_path="示例公司_2023年报.pdf",
    #     stock_price=25.8,
    #     api_key=api_key
    # )

    print("\n请将上述代码中的PDF路径替换为实际文件路径后运行。")

    # 示例2: 批量分析
    # batch_analysis_example()

    print("\n" + "=" * 60)
    print("更多使用方法请参考 README.md")
    print("=" * 60)
