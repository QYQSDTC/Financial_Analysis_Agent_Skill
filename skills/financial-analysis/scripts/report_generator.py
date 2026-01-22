"""
分析报告生成器
生成专业的投资分析报告（支持Markdown、PDF、Excel等格式）
"""

from typing import Dict, Optional, List
from datetime import datetime
import pandas as pd


class AnalysisReportGenerator:
    """分析报告生成器"""

    def __init__(self):
        """初始化报告生成器"""
        pass

    def generate_markdown_report(
        self,
        company_name: str,
        report_period: str,
        report_type: str,
        statement_data: Dict,
        indicators: Dict,
        analysis: Dict,
        recommendation: Dict,
        output_path: Optional[str] = None,
        dupont_analysis: Dict = None,
        trend_analysis: Dict = None
    ) -> str:
        """
        生成Markdown格式的分析报告

        Args:
            company_name: 公司名称
            report_period: 报告期
            report_type: 报告类型
            statement_data: 报表数据
            indicators: 财务指标
            analysis: 分析结果
            recommendation: 投资建议
            output_path: 输出路径
            dupont_analysis: 杜邦分析结果（可选）
            trend_analysis: 趋势分析结果（可选）

        Returns:
            Markdown格式的报告内容
        """
        report = f"""# {company_name} 财务分析报告

**报告期**: {report_period} ({report_type})
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**综合评级**: {analysis.get('overall_rating', 'N/A')}

---

## 一、财务数据概览

### 1.1 资产负债表（单位：万元）
"""
        # 添加资产负债表数据
        if 'balance_sheet' in statement_data:
            bs = statement_data['balance_sheet']
            report += f"""
| 项目 | 金额 |
|------|------|
| 总资产 | {bs.get('total_assets', 0):,.2f} |
| 流动资产 | {bs.get('current_assets', 0):,.2f} |
| 货币资金 | {bs.get('cash_and_equivalents', 0):,.2f} |
| 应收账款 | {bs.get('accounts_receivable', 0):,.2f} |
| 存货 | {bs.get('inventory', 0):,.2f} |
| 总负债 | {bs.get('total_liabilities', 0):,.2f} |
| 流动负债 | {bs.get('current_liabilities', 0):,.2f} |
| 股东权益 | {bs.get('shareholders_equity', 0):,.2f} |
"""

        report += """
### 1.2 利润表（单位：万元）
"""
        # 添加利润表数据
        if 'income_statement' in statement_data:
            is_data = statement_data['income_statement']
            report += f"""
| 项目 | 金额 |
|------|------|
| 营业收入 | {is_data.get('operating_revenue', 0):,.2f} |
| 营业成本 | {is_data.get('operating_cost', 0):,.2f} |
| 营业利润 | {is_data.get('operating_profit', 0):,.2f} |
| 净利润 | {is_data.get('net_profit', 0):,.2f} |
| 归母净利润 | {is_data.get('net_profit_attributable', 0):,.2f} |
"""

        report += """
### 1.3 现金流量表（单位：万元）
"""
        # 添加现金流量表数据
        if 'cashflow_statement' in statement_data:
            cf = statement_data['cashflow_statement']
            report += f"""
| 项目 | 金额 |
|------|------|
| 经营活动现金流 | {cf.get('operating_cashflow', 0):,.2f} |
| 投资活动现金流 | {cf.get('investing_cashflow', 0):,.2f} |
| 筹资活动现金流 | {cf.get('financing_cashflow', 0):,.2f} |
| 现金净增加额 | {cf.get('net_cashflow', 0):,.2f} |
"""

        report += """
---

## 二、关键财务指标分析

"""
        # 添加盈利能力指标
        if 'profitability' in indicators:
            report += "### 2.1 盈利能力指标\n\n"
            prof = indicators['profitability']
            report += "| 指标 | 数值 | 评价 |\n|------|------|------|\n"

            roe = prof.get('roe', 0)
            roe_eval = "优秀" if roe >= 15 else "良好" if roe >= 10 else "一般" if roe >= 5 else "较差"
            report += f"| 净资产收益率(ROE) | {roe:.2f}% | {roe_eval} |\n"

            gross_margin = prof.get('gross_margin', 0)
            gm_eval = "优秀" if gross_margin >= 40 else "良好" if gross_margin >= 30 else "一般" if gross_margin >= 20 else "较低"
            report += f"| 毛利率 | {gross_margin:.2f}% | {gm_eval} |\n"

            net_margin = prof.get('net_margin', 0)
            nm_eval = "优秀" if net_margin >= 15 else "良好" if net_margin >= 10 else "一般" if net_margin >= 5 else "较低"
            report += f"| 净利率 | {net_margin:.2f}% | {nm_eval} |\n"

            if 'roa' in prof:
                report += f"| 总资产收益率(ROA) | {prof['roa']:.2f}% | - |\n"

            report += "\n"

        # 添加偿债能力指标
        if 'solvency' in indicators:
            report += "### 2.2 偿债能力指标\n\n"
            solv = indicators['solvency']
            report += "| 指标 | 数值 | 评价 |\n|------|------|------|\n"

            current_ratio = solv.get('current_ratio', 0)
            cr_eval = "优秀" if current_ratio >= 2 else "良好" if current_ratio >= 1.5 else "及格" if current_ratio >= 1 else "风险"
            report += f"| 流动比率 | {current_ratio:.2f} | {cr_eval} |\n"

            quick_ratio = solv.get('quick_ratio', 0)
            qr_eval = "优秀" if quick_ratio >= 1.5 else "良好" if quick_ratio >= 1 else "一般" if quick_ratio >= 0.8 else "风险"
            report += f"| 速动比率 | {quick_ratio:.2f} | {qr_eval} |\n"

            debt_ratio = solv.get('debt_to_asset', 0)
            dr_eval = "优秀" if debt_ratio <= 40 else "良好" if debt_ratio <= 60 else "一般" if debt_ratio <= 70 else "风险"
            report += f"| 资产负债率 | {debt_ratio:.2f}% | {dr_eval} |\n"

            report += "\n"

        # 添加运营能力指标
        if 'operational' in indicators:
            report += "### 2.3 运营能力指标\n\n"
            oper = indicators['operational']
            report += "| 指标 | 数值 |\n|------|------|\n"

            if 'asset_turnover' in oper:
                report += f"| 总资产周转率 | {oper['asset_turnover']:.2f} |\n"
            if 'receivables_turnover' in oper:
                report += f"| 应收账款周转率 | {oper['receivables_turnover']:.2f} |\n"
            if 'receivables_days' in oper:
                report += f"| 应收账款周转天数 | {oper['receivables_days']:.0f} 天 |\n"
            if 'inventory_turnover' in oper:
                report += f"| 存货周转率 | {oper['inventory_turnover']:.2f} |\n"
            if 'cash_conversion_cycle' in oper:
                report += f"| 现金循环周期 | {oper['cash_conversion_cycle']:.0f} 天 |\n"

            report += "\n"

        # 添加现金流质量指标
        if 'cashflow_quality' in indicators:
            report += "### 2.4 现金流质量指标\n\n"
            cf = indicators['cashflow_quality']
            report += "| 指标 | 数值 | 评价 |\n|------|------|------|\n"

            cf_to_profit = cf.get('operating_cf_to_net_profit', 0)
            cf_eval = "优秀" if cf_to_profit >= 100 else "良好" if cf_to_profit >= 80 else "一般" if cf_to_profit >= 50 else "较差"
            report += f"| 经营现金流/净利润 | {cf_to_profit:.2f}% | {cf_eval} |\n"

            fcf = cf.get('free_cashflow', 0)
            fcf_eval = "正" if fcf > 0 else "负"
            report += f"| 自由现金流 | {fcf:,.2f} 万元 | {fcf_eval} |\n"

            report += "\n"

        # 添加杜邦分析章节
        if dupont_analysis:
            report += self._generate_dupont_section(dupont_analysis)

        # 添加趋势分析章节
        if trend_analysis:
            report += self._generate_trend_section(trend_analysis)

        report += """
---

## 三、专业财务分析

"""
        # 添加详细分析
        report += analysis.get('detailed_analysis', '暂无详细分析')

        report += """

---

## 四、优势与劣势分析

### 4.1 核心优势
"""
        strengths = analysis.get('strengths', [])
        if strengths:
            for i, strength in enumerate(strengths, 1):
                report += f"{i}. {strength}\n"
        else:
            report += "暂未发现明显优势\n"

        report += """
### 4.2 主要劣势
"""
        weaknesses = analysis.get('weaknesses', [])
        if weaknesses:
            for i, weakness in enumerate(weaknesses, 1):
                report += f"{i}. {weakness}\n"
        else:
            report += "暂未发现明显劣势\n"

        report += """
---

## 五、风险提示

"""
        risks = analysis.get('risks', [])
        if risks:
            for i, risk in enumerate(risks, 1):
                report += f"{i}. ⚠️ {risk}\n"
        else:
            report += "暂无重大风险提示\n"

        report += """
---

## 六、投资建议

"""
        # 添加投资建议
        report += f"**投资评级**: {recommendation.get('rating', 'N/A')}\n\n"
        report += f"**操作建议**: {recommendation.get('action', 'N/A')}\n\n"
        report += f"**目标投资者**: {recommendation.get('target_investor', 'N/A')}\n\n"

        if recommendation.get('target_price'):
            report += f"**目标价**: {recommendation['target_price']} 元\n\n"
        if recommendation.get('entry_price'):
            report += f"**建议买入价**: {recommendation['entry_price']} 元\n\n"
        if recommendation.get('stop_loss'):
            report += f"**止损价**: {recommendation['stop_loss']} 元\n\n"

        report += "**主要理由**:\n\n"
        reasons = recommendation.get('reasons', [])
        if reasons:
            for i, reason in enumerate(reasons, 1):
                report += f"{i}. {reason}\n"

        report += """

---

## 七、免责声明

本报告仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。
报告中的数据和分析基于公开披露的财务报表，可能存在滞后性。
投资者应结合自身风险承受能力和投资目标，审慎决策。

---

*报告生成工具: Financial Report Analyzer v1.0*
"""

        # 如果提供了输出路径，保存文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {output_path}")

        return report

    def generate_excel_report(
        self,
        company_name: str,
        report_period: str,
        statement_data: Dict,
        indicators: Dict,
        output_path: str
    ) -> None:
        """
        生成Excel格式的分析报告

        Args:
            company_name: 公司名称
            report_period: 报告期
            statement_data: 报表数据
            indicators: 财务指标
            output_path: 输出文件路径
        """
        # 创建Excel writer
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 资产负债表
            if 'balance_sheet' in statement_data:
                bs_df = pd.DataFrame([statement_data['balance_sheet']]).T
                bs_df.columns = ['金额（万元）']
                bs_df.index.name = '项目'
                bs_df.to_excel(writer, sheet_name='资产负债表')

            # 利润表
            if 'income_statement' in statement_data:
                is_df = pd.DataFrame([statement_data['income_statement']]).T
                is_df.columns = ['金额（万元）']
                is_df.index.name = '项目'
                is_df.to_excel(writer, sheet_name='利润表')

            # 现金流量表
            if 'cashflow_statement' in statement_data:
                cf_df = pd.DataFrame([statement_data['cashflow_statement']]).T
                cf_df.columns = ['金额（万元）']
                cf_df.index.name = '项目'
                cf_df.to_excel(writer, sheet_name='现金流量表')

            # 财务指标汇总
            all_indicators = {}
            for category, metrics in indicators.items():
                if isinstance(metrics, dict):
                    for key, value in metrics.items():
                        all_indicators[f"{category}_{key}"] = value

            if all_indicators:
                ind_df = pd.DataFrame([all_indicators]).T
                ind_df.columns = ['数值']
                ind_df.index.name = '指标'
                ind_df.to_excel(writer, sheet_name='财务指标')

        print(f"Excel报告已保存到: {output_path}")

    def generate_summary_dataframe(
        self,
        company_name: str,
        report_period: str,
        indicators: Dict,
        analysis: Dict
    ) -> pd.DataFrame:
        """
        生成摘要DataFrame，便于多期对比

        Returns:
            摘要DataFrame
        """
        summary = {
            '公司名称': company_name,
            '报告期': report_period,
            '综合评级': analysis.get('overall_rating', 'N/A'),
        }

        # 添加关键指标
        if 'profitability' in indicators:
            prof = indicators['profitability']
            summary['ROE(%)'] = prof.get('roe', 0)
            summary['毛利率(%)'] = prof.get('gross_margin', 0)
            summary['净利率(%)'] = prof.get('net_margin', 0)

        if 'solvency' in indicators:
            solv = indicators['solvency']
            summary['流动比率'] = solv.get('current_ratio', 0)
            summary['资产负债率(%)'] = solv.get('debt_to_asset', 0)

        if 'operational' in indicators:
            oper = indicators['operational']
            summary['总资产周转率'] = oper.get('asset_turnover', 0)

        if 'cashflow_quality' in indicators:
            cf = indicators['cashflow_quality']
            summary['现金净利比(%)'] = cf.get('operating_cf_to_net_profit', 0)

        return pd.DataFrame([summary])

    def _generate_dupont_section(self, dupont_analysis: Dict) -> str:
        """生成杜邦分析报告章节"""
        section = """
---

## 杜邦分析

"""
        # 分解结果
        decomposition = dupont_analysis.get('decomposition', {})
        if decomposition:
            roe = decomposition.get('roe', 0)
            npm = decomposition.get('net_profit_margin', 0)
            at = decomposition.get('asset_turnover', 0)
            em = decomposition.get('equity_multiplier', 0)

            section += "### ROE分解\n\n"
            section += f"**ROE = 净利率 × 资产周转率 × 权益乘数**\n\n"
            section += f"**{roe:.2f}% = {npm:.2f}% × {at:.4f} × {em:.4f}**\n\n"

            section += "| 因素 | 数值 | 说明 |\n|------|------|------|\n"
            section += f"| 净利率 | {npm:.2f}% | 反映盈利能力 |\n"
            section += f"| 资产周转率 | {at:.4f} | 反映运营效率 |\n"
            section += f"| 权益乘数 | {em:.4f} | 反映财务杠杆 |\n"
            section += f"| **ROE** | **{roe:.2f}%** | 综合收益率 |\n\n"

        # 质量评估
        quality = dupont_analysis.get('quality_evaluation', {})
        if quality:
            section += "### ROE质量评估\n\n"
            section += f"- **驱动类型**: {quality.get('driver_type', 'N/A')}\n"
            section += f"- **质量评级**: {quality.get('quality', 'N/A')}\n"
            section += f"- **风险等级**: {quality.get('risk_level', 'N/A')}\n"
            section += f"- **可持续性**: {quality.get('sustainability', 'N/A')}\n\n"

            details = quality.get('details', [])
            if details:
                section += "**分析要点:**\n\n"
                for detail in details:
                    section += f"- {detail}\n"
                section += "\n"

        # 驱动因素分析（如果有对比数据）
        driver_analysis = dupont_analysis.get('driver_analysis', {})
        if driver_analysis:
            section += "### ROE变动分析\n\n"

            changes = driver_analysis.get('changes', {})
            roe_change = changes.get('roe_change', 0)
            section += f"**ROE变动: {'+' if roe_change >= 0 else ''}{roe_change:.2f}个百分点**\n\n"

            contributions = driver_analysis.get('contributions', {})
            if contributions:
                section += "| 驱动因素 | 贡献度 |\n|----------|--------|\n"
                section += f"| 净利率变动 | {contributions.get('net_profit_margin_contribution', 0):+.2f}% |\n"
                section += f"| 资产周转率变动 | {contributions.get('asset_turnover_contribution', 0):+.2f}% |\n"
                section += f"| 权益乘数变动 | {contributions.get('equity_multiplier_contribution', 0):+.2f}% |\n\n"

            main_driver = driver_analysis.get('main_driver', '')
            if main_driver:
                section += f"**主要驱动因素**: {main_driver}\n\n"

            interpretations = driver_analysis.get('interpretation', [])
            if interpretations:
                section += "**解读:**\n\n"
                for interp in interpretations:
                    section += f"- {interp}\n"
                section += "\n"

        return section

    def _generate_trend_section(self, trend_analysis: Dict) -> str:
        """生成趋势分析报告章节"""
        section = """
---

## 趋势分析

"""
        summary = trend_analysis.get('summary', {})

        # 分析期间
        date_range = summary.get('date_range', {})
        if date_range:
            section += f"**分析期间**: {date_range.get('start', '')} 至 {date_range.get('end', '')}\n\n"

        # CAGR
        cagr = trend_analysis.get('cagr', {})
        if cagr:
            section += "### 复合增长率 (CAGR)\n\n"
            section += "| 指标 | CAGR |\n|------|------|\n"
            for metric_name, value in cagr.items():
                section += f"| {metric_name} | {value:+.2f}% |\n"
            section += "\n"

        # 关键指标趋势
        key_trends = trend_analysis.get('key_metric_trends', {})
        if key_trends:
            section += "### 关键指标趋势\n\n"
            section += "| 指标 | 趋势方向 | 最新值 |\n|------|----------|--------|\n"
            for metric_name, trend_data in key_trends.items():
                direction = trend_data.get('direction', 'N/A')
                values = trend_data.get('values', [])
                latest = values[-1] if values else 'N/A'
                if isinstance(latest, (int, float)):
                    section += f"| {metric_name} | {direction} | {latest:.2f} |\n"
                else:
                    section += f"| {metric_name} | {direction} | {latest} |\n"
            section += "\n"

        # 预警信息
        alerts = trend_analysis.get('alerts', {})
        if alerts:
            total_alerts = alerts.get('total_alerts', 0)
            if total_alerts > 0:
                section += "### 趋势预警\n\n"

                by_level = alerts.get('by_level', {})

                # 严重预警
                critical = by_level.get('严重', [])
                if critical:
                    section += "**🔴 严重预警:**\n\n"
                    for alert in critical:
                        section += f"- {alert.get('message', '')}\n"
                    section += "\n"

                # 警告
                warnings = by_level.get('警告', [])
                if warnings:
                    section += "**🟠 警告:**\n\n"
                    for alert in warnings:
                        section += f"- {alert.get('message', '')}\n"
                    section += "\n"

                # 注意
                cautions = by_level.get('注意', [])
                if cautions:
                    section += "**🟡 注意:**\n\n"
                    for alert in cautions:
                        section += f"- {alert.get('message', '')}\n"
                    section += "\n"

        return section
