"""
专业财务分析器
基于AI大模型进行深度财务分析和投资建议
"""

from typing import Dict, List, Optional
from openai import OpenAI
import os

# 导入新增模块
from scripts.dupont_analyzer import DuPontAnalyzer
from scripts.trend_analyzer import MultiPeriodTrendAnalyzer


class FinancialAnalyzer:
    """专业财务分析器"""

    # 第三方 API endpoint
    BASE_URL = "https://api.drqyq.com"
    MODEL = "claude-opus-4-5-20250514"

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化分析器

        Args:
            api_key: API密钥，如果不提供则从环境变量读取
        """
        self.api_key = (
            api_key or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        )
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.BASE_URL)
        else:
            self.client = None
            print("警告: 未提供API密钥，AI分析功能将不可用")

    def analyze_financial_health(
        self,
        company_name: str,
        indicators: Dict[str, Dict],
        report_type: str,
        report_period: str,
    ) -> Dict[str, any]:
        """
        综合分析公司财务健康状况

        Args:
            company_name: 公司名称
            indicators: 财务指标字典
            report_type: 报告类型
            report_period: 报告期

        Returns:
            分析结果字典，包含：
            - overall_rating: 综合评级 (优秀/良好/一般/较差/差)
            - strengths: 优势列表
            - weaknesses: 劣势列表
            - risks: 风险列表
            - opportunities: 机会列表
            - detailed_analysis: 详细分析文本
        """
        analysis = {
            "overall_rating": self._get_overall_rating(indicators),
            "strengths": self._identify_strengths(indicators),
            "weaknesses": self._identify_weaknesses(indicators),
            "risks": self._identify_risks(indicators),
            "opportunities": self._identify_opportunities(indicators),
        }

        # 使用AI进行深度分析
        if self.client:
            analysis["detailed_analysis"] = self._ai_deep_analysis(
                company_name, indicators, report_type, report_period, analysis
            )
        else:
            analysis["detailed_analysis"] = self._basic_analysis(
                company_name, indicators, analysis
            )

        return analysis

    def _get_overall_rating(self, indicators: Dict) -> str:
        """获取综合评级"""
        # 计算各维度平均分
        scores = []

        for dimension in [
            "profitability",
            "solvency",
            "operational",
            "cashflow_quality",
        ]:
            if dimension in indicators:
                dim_data = indicators[dimension]
                # 简单评分逻辑
                if dimension == "profitability":
                    roe = dim_data.get("roe", 0)
                    if roe >= 15:
                        scores.append(90)
                    elif roe >= 10:
                        scores.append(75)
                    elif roe >= 5:
                        scores.append(60)
                    else:
                        scores.append(40)

                elif dimension == "solvency":
                    current_ratio = dim_data.get("current_ratio", 0)
                    debt_ratio = dim_data.get("debt_to_asset", 100)
                    if current_ratio >= 1.5 and debt_ratio <= 50:
                        scores.append(85)
                    elif current_ratio >= 1 and debt_ratio <= 70:
                        scores.append(70)
                    else:
                        scores.append(50)

        avg_score = sum(scores) / len(scores) if scores else 50

        if avg_score >= 85:
            return "优秀"
        elif avg_score >= 70:
            return "良好"
        elif avg_score >= 60:
            return "一般"
        elif avg_score >= 50:
            return "较差"
        else:
            return "差"

    def _identify_strengths(self, indicators: Dict) -> List[str]:
        """识别优势"""
        strengths = []

        # 盈利能力优势
        if "profitability" in indicators:
            prof = indicators["profitability"]
            if prof.get("roe", 0) >= 15:
                strengths.append(f"净资产收益率优秀 ({prof['roe']:.2f}%)，盈利能力强")
            if prof.get("gross_margin", 0) >= 40:
                strengths.append(
                    f"毛利率高 ({prof['gross_margin']:.2f}%)，产品竞争力强"
                )
            if prof.get("net_margin", 0) >= 15:
                strengths.append(
                    f"净利率高 ({prof['net_margin']:.2f}%)，成本控制能力强"
                )

        # 偿债能力优势
        if "solvency" in indicators:
            solv = indicators["solvency"]
            if solv.get("current_ratio", 0) >= 2:
                strengths.append(
                    f"流动比率优秀 ({solv['current_ratio']:.2f})，短期偿债能力强"
                )
            if solv.get("debt_to_asset", 100) <= 40:
                strengths.append(
                    f"资产负债率低 ({solv['debt_to_asset']:.2f}%)，财务风险小"
                )

        # 运营能力优势
        if "operational" in indicators:
            oper = indicators["operational"]
            if oper.get("asset_turnover", 0) >= 1.2:
                strengths.append(
                    f"资产周转率高 ({oper['asset_turnover']:.2f})，资产使用效率优秀"
                )
            if oper.get("cash_conversion_cycle", 999) <= 60:
                strengths.append(
                    f"现金循环周期短 ({oper['cash_conversion_cycle']:.0f}天)，资金周转快"
                )

        # 现金流优势
        if "cashflow_quality" in indicators:
            cf = indicators["cashflow_quality"]
            if cf.get("operating_cf_to_net_profit", 0) >= 100:
                strengths.append(
                    f"经营现金流充沛 ({cf['operating_cf_to_net_profit']:.2f}%)，利润质量高"
                )
            if cf.get("free_cashflow", -999999) > 0:
                strengths.append("自由现金流为正，现金创造能力强")

        return strengths

    def _identify_weaknesses(self, indicators: Dict) -> List[str]:
        """识别劣势"""
        weaknesses = []

        # 盈利能力劣势
        if "profitability" in indicators:
            prof = indicators["profitability"]
            if prof.get("roe", 0) < 5:
                weaknesses.append(
                    f"净资产收益率较低 ({prof.get('roe', 0):.2f}%)，盈利能力不足"
                )
            if prof.get("gross_margin", 0) < 20:
                weaknesses.append(
                    f"毛利率偏低 ({prof.get('gross_margin', 0):.2f}%)，产品竞争力弱"
                )
            if prof.get("net_margin", 0) < 5:
                weaknesses.append(
                    f"净利率低 ({prof.get('net_margin', 0):.2f}%)，盈利空间小"
                )

        # 偿债能力劣势
        if "solvency" in indicators:
            solv = indicators["solvency"]
            if solv.get("current_ratio", 0) < 1:
                weaknesses.append(
                    f"流动比率不足1 ({solv.get('current_ratio', 0):.2f})，短期偿债压力大"
                )
            if solv.get("debt_to_asset", 0) > 70:
                weaknesses.append(
                    f"资产负债率高 ({solv.get('debt_to_asset', 0):.2f}%)，财务杠杆风险大"
                )
            if solv.get("interest_coverage", 0) < 2:
                weaknesses.append("利息保障倍数低，债务偿付能力堪忧")

        # 运营能力劣势
        if "operational" in indicators:
            oper = indicators["operational"]
            if oper.get("asset_turnover", 0) < 0.5:
                weaknesses.append(
                    f"资产周转率低 ({oper.get('asset_turnover', 0):.2f})，资产使用效率差"
                )
            if oper.get("receivables_days", 0) > 90:
                weaknesses.append(
                    f"应收账款周转天数长 ({oper.get('receivables_days', 0):.0f}天)，回款慢"
                )

        # 现金流劣势
        if "cashflow_quality" in indicators:
            cf = indicators["cashflow_quality"]
            if cf.get("operating_cf_to_net_profit", 0) < 50:
                weaknesses.append("经营现金流与净利润不匹配，利润质量存疑")
            if cf.get("free_cashflow", 1) < 0:
                weaknesses.append("自由现金流为负，现金创造能力不足")

        return weaknesses

    def _identify_risks(self, indicators: Dict) -> List[str]:
        """识别风险"""
        risks = []

        # 流动性风险
        if "solvency" in indicators:
            solv = indicators["solvency"]
            if solv.get("current_ratio", 0) < 0.8:
                risks.append("流动比率过低，存在流动性风险")
            if solv.get("quick_ratio", 0) < 0.5:
                risks.append("速动比率过低，即期偿债能力不足")

        # 财务风险
        if "solvency" in indicators:
            solv = indicators["solvency"]
            if solv.get("debt_to_asset", 0) > 80:
                risks.append("资产负债率过高，财务风险极高")
            if solv.get("debt_to_equity", 0) > 200:
                risks.append("产权比率过高，资本结构不合理")

        # 盈利风险
        if "profitability" in indicators:
            prof = indicators["profitability"]
            if prof.get("net_margin", 0) < 3:
                risks.append("净利率过低，盈利空间极小，抗风险能力弱")

        # 现金流风险
        if "cashflow_quality" in indicators:
            cf = indicators["cashflow_quality"]
            operating_cf = cf.get("operating_cf_to_net_profit", 0)
            if operating_cf < 0:
                risks.append("经营现金流为负，存在资金链断裂风险")

        return risks

    def _identify_opportunities(self, indicators: Dict) -> List[str]:
        """识别机会"""
        opportunities = []

        # 增长机会
        if "profitability" in indicators:
            prof = indicators["profitability"]
            if prof.get("roe", 0) >= 12 and prof.get("gross_margin", 0) >= 30:
                opportunities.append("高盈利能力为业务扩张提供资金支持")

        # 效率提升机会
        if "operational" in indicators:
            oper = indicators["operational"]
            if oper.get("inventory_days", 0) > 90:
                opportunities.append("存货周转率有提升空间，可优化库存管理")
            if oper.get("receivables_days", 0) > 60:
                opportunities.append("应收账款管理有改善空间，可加速资金回笼")

        # 资本结构优化
        if "solvency" in indicators:
            solv = indicators["solvency"]
            if solv.get("debt_to_asset", 100) < 30 and solv.get("current_ratio", 0) > 2:
                opportunities.append("财务稳健，可适度提高财务杠杆以提升ROE")

        return opportunities

    def _ai_deep_analysis(
        self,
        company_name: str,
        indicators: Dict,
        report_type: str,
        report_period: str,
        basic_analysis: Dict,
    ) -> str:
        """使用AI进行深度分析"""
        prompt = f"""
你是一位资深的证券分析师，请对以下公司的财务数据进行深入分析：

公司名称: {company_name}
报告类型: {report_type}
报告期: {report_period}

财务指标:
{self._format_indicators(indicators)}

初步分析结果:
综合评级: {basic_analysis['overall_rating']}
主要优势: {', '.join(basic_analysis['strengths'][:3]) if basic_analysis['strengths'] else '无明显优势'}
主要劣势: {', '.join(basic_analysis['weaknesses'][:3]) if basic_analysis['weaknesses'] else '无明显劣势'}

请从以下角度进行专业分析:
1. 盈利能力分析（ROE、毛利率、净利率等核心指标解读）
2. 偿债能力分析（流动性、杠杆率等安全性评估）
3. 运营效率分析（周转率、现金循环等效率评价）
4. 现金流质量分析（经营现金流、自由现金流等质量判断）
5. 与行业平均水平对比（如可能）
6. 潜在风险提示
7. 投资价值评估

请提供专业、客观、结构化的分析报告。
"""

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI分析失败: {e}")
            return self._basic_analysis(company_name, indicators, basic_analysis)

    def _basic_analysis(
        self, company_name: str, indicators: Dict, basic_analysis: Dict
    ) -> str:
        """基础分析（当AI不可用时）"""
        analysis_text = f"## {company_name} 财务分析报告\n\n"
        analysis_text += f"### 综合评级: {basic_analysis['overall_rating']}\n\n"

        if basic_analysis["strengths"]:
            analysis_text += "### 主要优势:\n"
            for i, strength in enumerate(basic_analysis["strengths"], 1):
                analysis_text += f"{i}. {strength}\n"
            analysis_text += "\n"

        if basic_analysis["weaknesses"]:
            analysis_text += "### 主要劣势:\n"
            for i, weakness in enumerate(basic_analysis["weaknesses"], 1):
                analysis_text += f"{i}. {weakness}\n"
            analysis_text += "\n"

        if basic_analysis["risks"]:
            analysis_text += "### 主要风险:\n"
            for i, risk in enumerate(basic_analysis["risks"], 1):
                analysis_text += f"{i}. {risk}\n"
            analysis_text += "\n"

        if basic_analysis["opportunities"]:
            analysis_text += "### 发展机会:\n"
            for i, opp in enumerate(basic_analysis["opportunities"], 1):
                analysis_text += f"{i}. {opp}\n"

        return analysis_text

    def _format_indicators(self, indicators: Dict) -> str:
        """格式化指标用于AI分析"""
        formatted = ""

        if "profitability" in indicators:
            formatted += "盈利能力指标:\n"
            prof = indicators["profitability"]
            for key, value in prof.items():
                formatted += f"  {key}: {value:.2f}\n"

        if "solvency" in indicators:
            formatted += "\n偿债能力指标:\n"
            solv = indicators["solvency"]
            for key, value in solv.items():
                formatted += f"  {key}: {value:.2f}\n"

        if "operational" in indicators:
            formatted += "\n运营能力指标:\n"
            oper = indicators["operational"]
            for key, value in oper.items():
                formatted += f"  {key}: {value:.2f}\n"

        if "cashflow_quality" in indicators:
            formatted += "\n现金流质量指标:\n"
            cf = indicators["cashflow_quality"]
            for key, value in cf.items():
                formatted += f"  {key}: {value:.2f}\n"

        return formatted

    def generate_investment_recommendation(
        self,
        analysis: Dict,
        indicators: Dict,
        stock_price: Optional[float] = None,
        target_investor_type: str = "稳健型",
    ) -> Dict[str, any]:
        """
        生成投资建议

        Args:
            analysis: 财务分析结果
            indicators: 财务指标
            stock_price: 当前股价（可选）
            target_investor_type: 目标投资者类型（激进型/稳健型/保守型）

        Returns:
            投资建议字典
        """
        recommendation = {
            "rating": self._get_investment_rating(analysis, indicators),
            "target_investor": target_investor_type,
            "action": "",
            "reasons": [],
            "entry_price": None,
            "stop_loss": None,
            "target_price": None,
        }

        rating = recommendation["rating"]

        # 根据评级给出操作建议
        if rating == "强烈推荐":
            recommendation["action"] = "买入"
            recommendation["reasons"].append("公司财务状况优秀，各项指标表现突出")
        elif rating == "推荐":
            recommendation["action"] = (
                "买入" if target_investor_type != "保守型" else "关注"
            )
            recommendation["reasons"].append("公司财务状况良好，值得配置")
        elif rating == "中性":
            recommendation["action"] = "持有"
            recommendation["reasons"].append("公司财务状况一般，建议观望")
        elif rating == "不推荐":
            recommendation["action"] = (
                "卖出" if target_investor_type == "激进型" else "减持"
            )
            recommendation["reasons"].append("公司财务状况存在隐忧")
        else:  # 强烈不推荐
            recommendation["action"] = "卖出"
            recommendation["reasons"].append("公司财务风险较大，建议规避")

        # 添加具体理由
        if analysis.get("strengths"):
            recommendation["reasons"].extend(analysis["strengths"][:2])
        if analysis.get("risks"):
            recommendation["reasons"].extend(
                [f"风险: {r}" for r in analysis["risks"][:2]]
            )

        # 如果提供了股价，计算目标价
        if stock_price and "valuation" in indicators:
            val = indicators["valuation"]
            eps = val.get("eps", 0)
            if eps > 0:
                # 根据行业平均市盈率估算（这里简化为15-25倍）
                if rating in ["强烈推荐", "推荐"]:
                    target_pe = 25
                elif rating == "中性":
                    target_pe = 18
                else:
                    target_pe = 12

                recommendation["target_price"] = round(eps * target_pe, 2)
                recommendation["entry_price"] = round(stock_price * 0.95, 2)
                recommendation["stop_loss"] = round(stock_price * 0.85, 2)

        return recommendation

    def _get_investment_rating(self, analysis: Dict, indicators: Dict) -> str:
        """获取投资评级"""
        overall_rating = analysis.get("overall_rating", "一般")
        risk_count = len(analysis.get("risks", []))
        strength_count = len(analysis.get("strengths", []))

        if overall_rating == "优秀" and risk_count <= 1:
            return "强烈推荐"
        elif overall_rating in ["优秀", "良好"] and risk_count <= 2:
            return "推荐"
        elif overall_rating == "一般" or (overall_rating == "良好" and risk_count > 2):
            return "中性"
        elif overall_rating == "较差":
            return "不推荐"
        else:
            return "强烈不推荐"

    def perform_dupont_analysis(
        self,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float],
        previous_balance_sheet: Dict[str, float] = None,
        previous_income_statement: Dict[str, float] = None
    ) -> Dict:
        """
        执行杜邦分析

        Args:
            balance_sheet: 当期资产负债表
            income_statement: 当期利润表
            previous_balance_sheet: 上期资产负债表（可选，用于对比分析）
            previous_income_statement: 上期利润表（可选，用于对比分析）

        Returns:
            杜邦分析结果，包括分解结果、质量评估和对比分析（如果有上期数据）
        """
        dupont = DuPontAnalyzer()

        result = {
            'decomposition': dupont.calculate_dupont_decomposition(
                balance_sheet, income_statement
            ),
            'quality_evaluation': None,
            'driver_analysis': None,
            'chart_data': None
        }

        result['quality_evaluation'] = dupont.evaluate_roe_quality()
        result['chart_data'] = dupont.get_dupont_chart_data()

        # 如果有上期数据，进行驱动因素分析
        if previous_balance_sheet and previous_income_statement:
            result['driver_analysis'] = dupont.analyze_roe_drivers(
                balance_sheet, income_statement,
                previous_balance_sheet, previous_income_statement
            )

        return result

    def perform_trend_analysis(
        self,
        period_data_list: List[Dict]
    ) -> Dict:
        """
        执行多期趋势分析

        Args:
            period_data_list: 多期财务数据列表，每项包含:
                - period: 期间标识
                - balance_sheet: 资产负债表
                - income_statement: 利润表
                - cashflow_statement: 现金流量表
                - indicators: 计算好的财务指标（可选）

        Returns:
            趋势分析结果，包括趋势摘要、关键指标CAGR、预警列表
        """
        trend_analyzer = MultiPeriodTrendAnalyzer()

        # 添加多期数据
        for period_data in period_data_list:
            trend_analyzer.add_period_data(
                period=period_data['period'],
                balance_sheet=period_data.get('balance_sheet', {}),
                income_statement=period_data.get('income_statement', {}),
                cashflow_statement=period_data.get('cashflow_statement', {}),
                indicators=period_data.get('indicators')
            )

        # 获取趋势分析摘要
        trend_summary = trend_analyzer.get_trend_summary()

        # 获取预警摘要
        alert_summary = trend_analyzer.get_alert_summary()

        # 分析关键指标趋势
        key_metric_trends = {}
        key_metrics = [
            ('income_statement.operating_revenue', '营业收入'),
            ('income_statement.net_profit', '净利润'),
            ('profitability.roe', 'ROE'),
            ('profitability.net_margin', '净利率'),
            ('solvency.current_ratio', '流动比率'),
            ('solvency.debt_to_asset', '资产负债率'),
            ('operational.asset_turnover', '资产周转率'),
            ('cashflow_quality.operating_cf_to_net_profit', '现金净利比')
        ]

        for metric_path, metric_name in key_metrics:
            trend = trend_analyzer.analyze_metric_trend(metric_path)
            if trend.get('status') != 'metric_not_found' and trend.get('status') != 'insufficient_data':
                key_metric_trends[metric_name] = {
                    'direction': trend.get('direction'),
                    'values': trend.get('values'),
                    'turning_points': trend.get('turning_points'),
                    'statistics': trend.get('statistics')
                }

        # 计算CAGR
        cagr_results = {}
        cagr_metrics = [
            ('income_statement.operating_revenue', '营业收入CAGR'),
            ('income_statement.net_profit', '净利润CAGR'),
            ('balance_sheet.total_assets', '总资产CAGR'),
            ('balance_sheet.shareholders_equity', '股东权益CAGR')
        ]

        for metric_path, metric_name in cagr_metrics:
            cagr = trend_analyzer.calculate_cagr(metric_path)
            if cagr is not None:
                cagr_results[metric_name] = cagr

        return {
            'summary': trend_summary,
            'key_metric_trends': key_metric_trends,
            'cagr': cagr_results,
            'alerts': alert_summary,
            'periods_count': len(period_data_list)
        }

    def analyze_financial_health_enhanced(
        self,
        company_name: str,
        indicators: Dict[str, Dict],
        report_type: str,
        report_period: str,
        balance_sheet: Dict[str, float] = None,
        income_statement: Dict[str, float] = None,
        previous_balance_sheet: Dict[str, float] = None,
        previous_income_statement: Dict[str, float] = None,
        period_data_list: List[Dict] = None
    ) -> Dict:
        """
        增强版财务健康分析，集成杜邦分析和趋势分析

        Args:
            company_name: 公司名称
            indicators: 财务指标字典
            report_type: 报告类型
            report_period: 报告期
            balance_sheet: 当期资产负债表（用于杜邦分析）
            income_statement: 当期利润表（用于杜邦分析）
            previous_balance_sheet: 上期资产负债表
            previous_income_statement: 上期利润表
            period_data_list: 多期数据列表（用于趋势分析）

        Returns:
            综合分析结果
        """
        # 基础分析
        analysis = self.analyze_financial_health(
            company_name, indicators, report_type, report_period
        )

        # 杜邦分析
        if balance_sheet and income_statement:
            analysis['dupont_analysis'] = self.perform_dupont_analysis(
                balance_sheet, income_statement,
                previous_balance_sheet, previous_income_statement
            )

        # 趋势分析
        if period_data_list and len(period_data_list) >= 2:
            analysis['trend_analysis'] = self.perform_trend_analysis(period_data_list)

            # 将趋势预警添加到风险列表
            trend_alerts = analysis.get('trend_analysis', {}).get('alerts', {})
            critical_alerts = trend_alerts.get('by_level', {}).get('严重', [])
            warning_alerts = trend_alerts.get('by_level', {}).get('警告', [])

            for alert in critical_alerts + warning_alerts:
                analysis['risks'].append(f"[趋势预警] {alert.get('message', '')}")

        return analysis
