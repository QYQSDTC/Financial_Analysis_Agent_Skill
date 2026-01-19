"""
财务指标计算器
计算各类财务指标和比率，用于深度财务分析
"""

from typing import Dict, Optional
import math


class FinancialIndicatorCalculator:
    """财务指标计算器"""

    def __init__(self):
        """初始化计算器"""
        self.indicators = {}

    def calculate_all_indicators(
        self,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float],
        cashflow_statement: Dict[str, float],
        metadata: Dict = None
    ) -> Dict[str, Dict]:
        """
        计算所有财务指标

        Returns:
            包含各类指标的字典：
            - profitability: 盈利能力指标
            - solvency: 偿债能力指标
            - operational: 运营能力指标
            - growth: 成长性指标
            - valuation: 估值指标
            - cashflow: 现金流指标
        """
        results = {
            'profitability': self.calculate_profitability(balance_sheet, income_statement),
            'solvency': self.calculate_solvency(balance_sheet, income_statement),
            'operational': self.calculate_operational_efficiency(balance_sheet, income_statement),
            'cashflow_quality': self.calculate_cashflow_quality(income_statement, cashflow_statement),
            'valuation': self.calculate_valuation_metrics(balance_sheet, income_statement, metadata),
        }

        self.indicators = results
        return results

    def calculate_profitability(
        self,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算盈利能力指标

        Returns:
            - gross_margin: 毛利率
            - operating_margin: 营业利润率
            - net_margin: 净利率
            - roe: 净资产收益率 (ROE)
            - roa: 总资产收益率 (ROA)
            - roic: 投入资本回报率 (ROIC)
        """
        indicators = {}

        # 毛利率 = (营业收入 - 营业成本) / 营业收入
        revenue = income_statement.get('operating_revenue', 0)
        cost = income_statement.get('operating_cost', 0)
        if revenue > 0:
            indicators['gross_margin'] = ((revenue - cost) / revenue) * 100

        # 营业利润率 = 营业利润 / 营业收入
        operating_profit = income_statement.get('operating_profit', 0)
        if revenue > 0:
            indicators['operating_margin'] = (operating_profit / revenue) * 100

        # 净利率 = 净利润 / 营业收入
        net_profit = income_statement.get('net_profit', 0)
        if revenue > 0:
            indicators['net_margin'] = (net_profit / revenue) * 100

        # ROE = 净利润 / 股东权益
        equity = balance_sheet.get('shareholders_equity', 0)
        if equity > 0:
            indicators['roe'] = (net_profit / equity) * 100

        # ROA = 净利润 / 总资产
        total_assets = balance_sheet.get('total_assets', 0)
        if total_assets > 0:
            indicators['roa'] = (net_profit / total_assets) * 100

        # ROIC = 息税后利润 / 投入资本
        # 简化计算：ROIC ≈ 营业利润 * (1 - 25%) / (总资产 - 流动负债)
        current_liabilities = balance_sheet.get('current_liabilities', 0)
        invested_capital = total_assets - current_liabilities
        if invested_capital > 0:
            nopat = operating_profit * 0.75  # 假设税率25%
            indicators['roic'] = (nopat / invested_capital) * 100

        return indicators

    def calculate_solvency(
        self,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算偿债能力指标

        Returns:
            - current_ratio: 流动比率
            - quick_ratio: 速动比率
            - cash_ratio: 现金比率
            - debt_to_asset: 资产负债率
            - debt_to_equity: 产权比率
            - interest_coverage: 利息保障倍数
            - equity_multiplier: 权益乘数
        """
        indicators = {}

        current_assets = balance_sheet.get('current_assets', 0)
        current_liabilities = balance_sheet.get('current_liabilities', 0)
        inventory = balance_sheet.get('inventory', 0)
        cash = balance_sheet.get('cash_and_equivalents', 0)
        total_assets = balance_sheet.get('total_assets', 0)
        total_liabilities = balance_sheet.get('total_liabilities', 0)
        equity = balance_sheet.get('shareholders_equity', 0)

        # 流动比率 = 流动资产 / 流动负债
        if current_liabilities > 0:
            indicators['current_ratio'] = current_assets / current_liabilities

        # 速动比率 = (流动资产 - 存货) / 流动负债
        if current_liabilities > 0:
            indicators['quick_ratio'] = (current_assets - inventory) / current_liabilities

        # 现金比率 = 货币资金 / 流动负债
        if current_liabilities > 0:
            indicators['cash_ratio'] = cash / current_liabilities

        # 资产负债率 = 总负债 / 总资产
        if total_assets > 0:
            indicators['debt_to_asset'] = (total_liabilities / total_assets) * 100

        # 产权比率 = 总负债 / 股东权益
        if equity > 0:
            indicators['debt_to_equity'] = (total_liabilities / equity) * 100

        # 利息保障倍数 = (利润总额 + 财务费用) / 财务费用
        total_profit = income_statement.get('total_profit', 0)
        financial_expenses = income_statement.get('financial_expenses', 0)
        if financial_expenses > 0:
            indicators['interest_coverage'] = (total_profit + financial_expenses) / financial_expenses

        # 权益乘数 = 总资产 / 股东权益
        if equity > 0:
            indicators['equity_multiplier'] = total_assets / equity

        return indicators

    def calculate_operational_efficiency(
        self,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算运营能力指标

        Returns:
            - asset_turnover: 总资产周转率
            - receivables_turnover: 应收账款周转率
            - inventory_turnover: 存货周转率
            - payables_turnover: 应付账款周转率
            - operating_cycle: 营业周期（天）
            - cash_conversion_cycle: 现金循环周期（天）
        """
        indicators = {}

        revenue = income_statement.get('operating_revenue', 0)
        cost = income_statement.get('operating_cost', 0)
        total_assets = balance_sheet.get('total_assets', 0)
        receivables = balance_sheet.get('accounts_receivable', 0)
        inventory = balance_sheet.get('inventory', 0)
        payables = balance_sheet.get('accounts_payable', 0)

        # 总资产周转率 = 营业收入 / 总资产
        if total_assets > 0:
            indicators['asset_turnover'] = revenue / total_assets

        # 应收账款周转率 = 营业收入 / 应收账款
        if receivables > 0:
            indicators['receivables_turnover'] = revenue / receivables
            indicators['receivables_days'] = 365 / indicators['receivables_turnover']

        # 存货周转率 = 营业成本 / 存货
        if inventory > 0:
            indicators['inventory_turnover'] = cost / inventory
            indicators['inventory_days'] = 365 / indicators['inventory_turnover']

        # 应付账款周转率 = 营业成本 / 应付账款
        if payables > 0:
            indicators['payables_turnover'] = cost / payables
            indicators['payables_days'] = 365 / indicators['payables_turnover']

        # 营业周期 = 应收账款周转天数 + 存货周转天数
        if 'receivables_days' in indicators and 'inventory_days' in indicators:
            indicators['operating_cycle'] = (
                indicators['receivables_days'] + indicators['inventory_days']
            )

        # 现金循环周期 = 营业周期 - 应付账款周转天数
        if 'operating_cycle' in indicators and 'payables_days' in indicators:
            indicators['cash_conversion_cycle'] = (
                indicators['operating_cycle'] - indicators['payables_days']
            )

        return indicators

    def calculate_cashflow_quality(
        self,
        income_statement: Dict[str, float],
        cashflow_statement: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算现金流质量指标

        Returns:
            - operating_cf_to_revenue: 销售现金比率
            - operating_cf_to_net_profit: 现金净利比
            - fcf: 自由现金流
            - fcf_to_revenue: 自由现金流比率
        """
        indicators = {}

        revenue = income_statement.get('operating_revenue', 0)
        net_profit = income_statement.get('net_profit', 0)
        operating_cf = cashflow_statement.get('operating_cashflow', 0)
        investing_cf = cashflow_statement.get('investing_cashflow', 0)

        # 销售现金比率 = 经营活动现金流 / 营业收入
        if revenue > 0:
            indicators['operating_cf_to_revenue'] = (operating_cf / revenue) * 100

        # 现金净利比 = 经营活动现金流 / 净利润
        if net_profit > 0:
            indicators['operating_cf_to_net_profit'] = (operating_cf / net_profit) * 100

        # 自由现金流 = 经营活动现金流 + 投资活动现金流
        # 注意：投资活动现金流通常为负
        indicators['free_cashflow'] = operating_cf + investing_cf

        # 自由现金流比率
        if revenue > 0:
            indicators['fcf_to_revenue'] = (indicators['free_cashflow'] / revenue) * 100

        return indicators

    def calculate_valuation_metrics(
        self,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float],
        metadata: Dict = None
    ) -> Dict[str, float]:
        """
        计算估值相关指标

        Returns:
            - eps: 每股收益
            - bvps: 每股净资产
            - pb_denominator: 市净率分母（每股净资产）
            - pe_denominator: 市盈率分母（每股收益）
        """
        indicators = {}

        if not metadata:
            return indicators

        total_shares = metadata.get('total_shares', 0)
        if total_shares <= 0:
            return indicators

        net_profit = income_statement.get('net_profit', 0)
        equity = balance_sheet.get('shareholders_equity', 0)

        # 每股收益 (EPS)
        eps = income_statement.get('basic_eps')
        if not eps and total_shares > 0:
            eps = net_profit / total_shares
        if eps:
            indicators['eps'] = eps

        # 每股净资产 (BVPS)
        if equity > 0 and total_shares > 0:
            indicators['bvps'] = equity / total_shares

        # 为估值计算提供分母
        if 'eps' in indicators:
            indicators['pe_denominator'] = indicators['eps']
        if 'bvps' in indicators:
            indicators['pb_denominator'] = indicators['bvps']

        return indicators

    def calculate_growth_rates(
        self,
        current_statement: Dict,
        previous_statement: Dict
    ) -> Dict[str, float]:
        """
        计算同比/环比增长率

        Args:
            current_statement: 当期报表数据
            previous_statement: 上期报表数据

        Returns:
            各项指标的增长率
        """
        growth_rates = {}

        key_metrics = [
            'operating_revenue',
            'net_profit',
            'total_assets',
            'shareholders_equity',
            'operating_cashflow'
        ]

        for metric in key_metrics:
            current = current_statement.get(metric, 0)
            previous = previous_statement.get(metric, 0)

            if previous > 0:
                growth = ((current - previous) / previous) * 100
                growth_rates[f'{metric}_growth'] = growth

        return growth_rates

    def get_summary(self) -> Dict:
        """获取指标汇总"""
        if not self.indicators:
            return {}

        summary = {
            '盈利能力评分': self._score_profitability(),
            '偿债能力评分': self._score_solvency(),
            '运营能力评分': self._score_operational(),
            '现金流质量评分': self._score_cashflow(),
            '综合评分': 0
        }

        # 计算综合评分（加权平均）
        weights = {
            '盈利能力评分': 0.35,
            '偿债能力评分': 0.25,
            '运营能力评分': 0.20,
            '现金流质量评分': 0.20
        }

        total_score = sum(
            summary[key] * weights[key]
            for key in weights
            if summary[key] is not None
        )
        summary['综合评分'] = round(total_score, 1)

        return summary

    def _score_profitability(self) -> Optional[float]:
        """盈利能力评分 (0-100)"""
        if 'profitability' not in self.indicators:
            return None

        prof = self.indicators['profitability']
        score = 0

        # ROE评分 (30分)
        roe = prof.get('roe', 0)
        if roe >= 20:
            score += 30
        elif roe >= 15:
            score += 25
        elif roe >= 10:
            score += 20
        elif roe >= 5:
            score += 10

        # 净利率评分 (30分)
        net_margin = prof.get('net_margin', 0)
        if net_margin >= 20:
            score += 30
        elif net_margin >= 15:
            score += 25
        elif net_margin >= 10:
            score += 20
        elif net_margin >= 5:
            score += 10

        # 毛利率评分 (20分)
        gross_margin = prof.get('gross_margin', 0)
        if gross_margin >= 50:
            score += 20
        elif gross_margin >= 40:
            score += 16
        elif gross_margin >= 30:
            score += 12
        elif gross_margin >= 20:
            score += 8

        # ROA评分 (20分)
        roa = prof.get('roa', 0)
        if roa >= 10:
            score += 20
        elif roa >= 7:
            score += 15
        elif roa >= 5:
            score += 10
        elif roa >= 3:
            score += 5

        return round(score, 1)

    def _score_solvency(self) -> Optional[float]:
        """偿债能力评分 (0-100)"""
        if 'solvency' not in self.indicators:
            return None

        solv = self.indicators['solvency']
        score = 0

        # 流动比率评分 (30分)
        current_ratio = solv.get('current_ratio', 0)
        if current_ratio >= 2:
            score += 30
        elif current_ratio >= 1.5:
            score += 25
        elif current_ratio >= 1:
            score += 15
        elif current_ratio >= 0.8:
            score += 5

        # 速动比率评分 (25分)
        quick_ratio = solv.get('quick_ratio', 0)
        if quick_ratio >= 1.5:
            score += 25
        elif quick_ratio >= 1:
            score += 20
        elif quick_ratio >= 0.8:
            score += 12
        elif quick_ratio >= 0.5:
            score += 5

        # 资产负债率评分 (25分)
        debt_ratio = solv.get('debt_to_asset', 0)
        if debt_ratio <= 40:
            score += 25
        elif debt_ratio <= 60:
            score += 20
        elif debt_ratio <= 70:
            score += 10
        elif debt_ratio <= 80:
            score += 5

        # 利息保障倍数评分 (20分)
        interest_cov = solv.get('interest_coverage', 0)
        if interest_cov >= 10:
            score += 20
        elif interest_cov >= 5:
            score += 15
        elif interest_cov >= 3:
            score += 10
        elif interest_cov >= 1.5:
            score += 5

        return round(score, 1)

    def _score_operational(self) -> Optional[float]:
        """运营能力评分 (0-100)"""
        if 'operational' not in self.indicators:
            return None

        oper = self.indicators['operational']
        score = 0

        # 总资产周转率评分 (35分)
        asset_turnover = oper.get('asset_turnover', 0)
        if asset_turnover >= 1.5:
            score += 35
        elif asset_turnover >= 1:
            score += 28
        elif asset_turnover >= 0.7:
            score += 20
        elif asset_turnover >= 0.5:
            score += 10

        # 应收账款周转率评分 (25分)
        receivables_turnover = oper.get('receivables_turnover', 0)
        if receivables_turnover >= 12:
            score += 25
        elif receivables_turnover >= 8:
            score += 20
        elif receivables_turnover >= 5:
            score += 12
        elif receivables_turnover >= 3:
            score += 6

        # 存货周转率评分 (20分)
        inventory_turnover = oper.get('inventory_turnover', 0)
        if inventory_turnover >= 10:
            score += 20
        elif inventory_turnover >= 6:
            score += 15
        elif inventory_turnover >= 4:
            score += 10
        elif inventory_turnover >= 2:
            score += 5

        # 现金循环周期评分 (20分)
        ccc = oper.get('cash_conversion_cycle')
        if ccc is not None:
            if ccc <= 30:
                score += 20
            elif ccc <= 60:
                score += 15
            elif ccc <= 90:
                score += 10
            elif ccc <= 120:
                score += 5

        return round(score, 1)

    def _score_cashflow(self) -> Optional[float]:
        """现金流质量评分 (0-100)"""
        if 'cashflow_quality' not in self.indicators:
            return None

        cf = self.indicators['cashflow_quality']
        score = 0

        # 现金净利比评分 (50分)
        cf_to_profit = cf.get('operating_cf_to_net_profit', 0)
        if cf_to_profit >= 120:
            score += 50
        elif cf_to_profit >= 100:
            score += 45
        elif cf_to_profit >= 80:
            score += 35
        elif cf_to_profit >= 50:
            score += 20
        elif cf_to_profit >= 0:
            score += 10

        # 销售现金比率评分 (30分)
        cf_to_revenue = cf.get('operating_cf_to_revenue', 0)
        if cf_to_revenue >= 15:
            score += 30
        elif cf_to_revenue >= 10:
            score += 24
        elif cf_to_revenue >= 5:
            score += 15
        elif cf_to_revenue >= 0:
            score += 8

        # 自由现金流评分 (20分)
        fcf = cf.get('free_cashflow', 0)
        if fcf > 0:
            fcf_ratio = cf.get('fcf_to_revenue', 0)
            if fcf_ratio >= 10:
                score += 20
            elif fcf_ratio >= 5:
                score += 15
            elif fcf_ratio >= 0:
                score += 10

        return round(score, 1)
