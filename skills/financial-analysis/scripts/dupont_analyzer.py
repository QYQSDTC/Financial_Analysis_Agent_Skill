"""
杜邦分析模块
实现ROE的三因素分解和驱动因素分析
"""

from typing import Dict, Optional, List


class DuPontAnalyzer:
    """
    杜邦分析器

    ROE = 净利率 × 资产周转率 × 权益乘数
    ROE = (净利润/营业收入) × (营业收入/总资产) × (总资产/股东权益)
    """

    def __init__(self):
        """初始化杜邦分析器"""
        self.current_decomposition = None
        self.previous_decomposition = None

    def calculate_dupont_decomposition(
        self,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float]
    ) -> Dict[str, float]:
        """
        计算杜邦分解的三个因素

        Args:
            balance_sheet: 资产负债表数据
            income_statement: 利润表数据

        Returns:
            杜邦分解结果字典，包含：
            - net_profit_margin: 净利率 (%)
            - asset_turnover: 资产周转率 (次)
            - equity_multiplier: 权益乘数 (倍)
            - roe: ROE (%)
            - roe_calculated: 杜邦分解计算的ROE (%)
        """
        decomposition = {}

        # 获取关键数据
        net_profit = income_statement.get('net_profit', 0)
        revenue = income_statement.get('operating_revenue', 0)
        total_assets = balance_sheet.get('total_assets', 0)
        equity = balance_sheet.get('shareholders_equity', 0)

        # 计算净利率 = 净利润 / 营业收入
        if revenue > 0:
            decomposition['net_profit_margin'] = (net_profit / revenue) * 100
        else:
            decomposition['net_profit_margin'] = 0

        # 计算资产周转率 = 营业收入 / 总资产
        if total_assets > 0:
            decomposition['asset_turnover'] = revenue / total_assets
        else:
            decomposition['asset_turnover'] = 0

        # 计算权益乘数 = 总资产 / 股东权益
        if equity > 0:
            decomposition['equity_multiplier'] = total_assets / equity
        else:
            decomposition['equity_multiplier'] = 0

        # 直接计算ROE = 净利润 / 股东权益
        if equity > 0:
            decomposition['roe'] = (net_profit / equity) * 100
        else:
            decomposition['roe'] = 0

        # 杜邦公式验证: ROE = 净利率 × 资产周转率 × 权益乘数
        decomposition['roe_calculated'] = (
            decomposition['net_profit_margin'] / 100 *
            decomposition['asset_turnover'] *
            decomposition['equity_multiplier']
        ) * 100

        self.current_decomposition = decomposition
        return decomposition

    def analyze_roe_drivers(
        self,
        current_balance_sheet: Dict[str, float],
        current_income_statement: Dict[str, float],
        previous_balance_sheet: Dict[str, float],
        previous_income_statement: Dict[str, float]
    ) -> Dict[str, any]:
        """
        分析ROE变动的驱动因素

        Args:
            current_balance_sheet: 当期资产负债表
            current_income_statement: 当期利润表
            previous_balance_sheet: 上期资产负债表
            previous_income_statement: 上期利润表

        Returns:
            ROE驱动因素分析结果
        """
        # 计算当期和上期的杜邦分解
        current = self.calculate_dupont_decomposition(
            current_balance_sheet, current_income_statement
        )
        self.current_decomposition = current

        previous = self.calculate_dupont_decomposition(
            previous_balance_sheet, previous_income_statement
        )
        self.previous_decomposition = previous

        # 计算各因素变动
        roe_change = current['roe'] - previous['roe']
        npm_change = current['net_profit_margin'] - previous['net_profit_margin']
        at_change = current['asset_turnover'] - previous['asset_turnover']
        em_change = current['equity_multiplier'] - previous['equity_multiplier']

        # 计算各因素对ROE变动的贡献（连环替代法简化版）
        # 净利率变动贡献
        npm_contribution = (npm_change / 100) * previous['asset_turnover'] * previous['equity_multiplier'] * 100

        # 资产周转率变动贡献
        at_contribution = (current['net_profit_margin'] / 100) * at_change * previous['equity_multiplier'] * 100

        # 权益乘数变动贡献
        em_contribution = (current['net_profit_margin'] / 100) * current['asset_turnover'] * em_change * 100

        # 确定主要驱动因素
        contributions = {
            '净利率': npm_contribution,
            '资产周转率': at_contribution,
            '权益乘数': em_contribution
        }

        main_driver = max(contributions, key=lambda k: abs(contributions[k]))

        analysis = {
            'current_period': current,
            'previous_period': previous,
            'changes': {
                'roe_change': round(roe_change, 2),
                'net_profit_margin_change': round(npm_change, 2),
                'asset_turnover_change': round(at_change, 4),
                'equity_multiplier_change': round(em_change, 4)
            },
            'contributions': {
                'net_profit_margin_contribution': round(npm_contribution, 2),
                'asset_turnover_contribution': round(at_contribution, 2),
                'equity_multiplier_contribution': round(em_contribution, 2)
            },
            'main_driver': main_driver,
            'interpretation': self._interpret_changes(
                roe_change, npm_change, at_change, em_change, contributions
            )
        }

        return analysis

    def _interpret_changes(
        self,
        roe_change: float,
        npm_change: float,
        at_change: float,
        em_change: float,
        contributions: Dict[str, float]
    ) -> List[str]:
        """
        解读ROE变动原因

        Returns:
            解读文本列表
        """
        interpretations = []

        # 总体判断
        if abs(roe_change) < 0.5:
            interpretations.append("ROE基本稳定，变动幅度较小")
        elif roe_change > 0:
            interpretations.append(f"ROE提升{roe_change:.2f}个百分点")
        else:
            interpretations.append(f"ROE下降{abs(roe_change):.2f}个百分点")

        # 净利率分析
        if abs(npm_change) > 1:
            if npm_change > 0:
                interpretations.append(
                    f"净利率提升{npm_change:.2f}%，表明盈利能力增强，"
                    "可能源于毛利率提升或费用控制改善"
                )
            else:
                interpretations.append(
                    f"净利率下降{abs(npm_change):.2f}%，盈利能力减弱，"
                    "需关注成本上涨或价格下降风险"
                )

        # 资产周转率分析
        if abs(at_change) > 0.05:
            if at_change > 0:
                interpretations.append(
                    f"资产周转率提升{at_change:.2f}，资产使用效率改善，"
                    "营运效率提高"
                )
            else:
                interpretations.append(
                    f"资产周转率下降{abs(at_change):.2f}，资产使用效率下降，"
                    "可能存在资产闲置或收入增长放缓"
                )

        # 权益乘数分析
        if abs(em_change) > 0.1:
            if em_change > 0:
                interpretations.append(
                    f"权益乘数提升{em_change:.2f}，财务杠杆增加，"
                    "放大了盈利但也提高了财务风险"
                )
            else:
                interpretations.append(
                    f"权益乘数下降{abs(em_change):.2f}，财务杠杆降低，"
                    "财务风险下降但可能制约ROE提升空间"
                )

        # 主要驱动因素
        sorted_contributions = sorted(
            contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        main_factor, main_contribution = sorted_contributions[0]

        if abs(main_contribution) > 0.5:
            direction = "正向" if main_contribution > 0 else "负向"
            interpretations.append(
                f"ROE变动的主要驱动因素是{main_factor}，"
                f"{direction}贡献{abs(main_contribution):.2f}个百分点"
            )

        return interpretations

    def get_dupont_chart_data(self) -> Dict[str, any]:
        """
        获取杜邦分析图表数据

        Returns:
            用于生成杜邦分析图的数据结构
        """
        if not self.current_decomposition:
            return {}

        current = self.current_decomposition

        chart_data = {
            'roe': round(current['roe'], 2),
            'level_1': {
                'net_profit_margin': round(current['net_profit_margin'], 2),
                'asset_turnover': round(current['asset_turnover'], 4),
                'equity_multiplier': round(current['equity_multiplier'], 4)
            },
            'formula': (
                f"ROE({current['roe']:.2f}%) = "
                f"净利率({current['net_profit_margin']:.2f}%) × "
                f"资产周转率({current['asset_turnover']:.2f}) × "
                f"权益乘数({current['equity_multiplier']:.2f})"
            )
        }

        # 如果有上期数据，添加对比
        if self.previous_decomposition:
            previous = self.previous_decomposition
            chart_data['comparison'] = {
                'roe': {
                    'current': round(current['roe'], 2),
                    'previous': round(previous['roe'], 2),
                    'change': round(current['roe'] - previous['roe'], 2)
                },
                'net_profit_margin': {
                    'current': round(current['net_profit_margin'], 2),
                    'previous': round(previous['net_profit_margin'], 2),
                    'change': round(
                        current['net_profit_margin'] - previous['net_profit_margin'], 2
                    )
                },
                'asset_turnover': {
                    'current': round(current['asset_turnover'], 4),
                    'previous': round(previous['asset_turnover'], 4),
                    'change': round(
                        current['asset_turnover'] - previous['asset_turnover'], 4
                    )
                },
                'equity_multiplier': {
                    'current': round(current['equity_multiplier'], 4),
                    'previous': round(previous['equity_multiplier'], 4),
                    'change': round(
                        current['equity_multiplier'] - previous['equity_multiplier'], 4
                    )
                }
            }

        return chart_data

    def evaluate_roe_quality(self) -> Dict[str, any]:
        """
        评估ROE的质量（判断ROE是由何种因素驱动）

        Returns:
            ROE质量评估结果
        """
        if not self.current_decomposition:
            return {'quality': '无法评估', 'reason': '缺少分解数据'}

        current = self.current_decomposition
        npm = current['net_profit_margin']
        at = current['asset_turnover']
        em = current['equity_multiplier']
        roe = current['roe']

        evaluation = {
            'roe': round(roe, 2),
            'quality': '',
            'driver_type': '',
            'risk_level': '',
            'sustainability': '',
            'details': []
        }

        # 判断驱动类型
        # 高净利率驱动（差异化/高端定位）
        if npm >= 15 and at < 0.8 and em < 2:
            evaluation['driver_type'] = '高净利率驱动'
            evaluation['quality'] = '优质'
            evaluation['risk_level'] = '低'
            evaluation['sustainability'] = '高'
            evaluation['details'].append(
                "ROE主要由高净利率驱动，体现较强的定价权和成本控制能力"
            )

        # 高周转驱动（薄利多销）
        elif npm < 10 and at >= 1.5 and em < 2:
            evaluation['driver_type'] = '高周转驱动'
            evaluation['quality'] = '良好'
            evaluation['risk_level'] = '中低'
            evaluation['sustainability'] = '中高'
            evaluation['details'].append(
                "ROE主要由高资产周转率驱动，体现高效的运营管理能力"
            )

        # 高杠杆驱动（风险较高）
        elif em >= 3:
            evaluation['driver_type'] = '高杠杆驱动'
            evaluation['quality'] = '一般'
            evaluation['risk_level'] = '高'
            evaluation['sustainability'] = '低'
            evaluation['details'].append(
                "ROE主要由高财务杠杆驱动，存在较高的财务风险"
            )

        # 均衡型
        elif npm >= 8 and at >= 0.6 and em >= 1.5 and em < 3:
            evaluation['driver_type'] = '均衡型'
            evaluation['quality'] = '良好'
            evaluation['risk_level'] = '中'
            evaluation['sustainability'] = '中高'
            evaluation['details'].append(
                "ROE由多因素均衡驱动，财务结构较为合理"
            )

        # 低效型
        else:
            evaluation['driver_type'] = '需改善'
            evaluation['quality'] = '较差'
            evaluation['risk_level'] = '中'
            evaluation['sustainability'] = '低'
            evaluation['details'].append(
                "各因素均表现一般，存在较大提升空间"
            )

        # 添加具体指标评价
        if npm >= 20:
            evaluation['details'].append(f"净利率{npm:.1f}%表现优秀")
        elif npm < 5:
            evaluation['details'].append(f"净利率仅{npm:.1f}%，盈利空间狭窄")

        if at >= 2:
            evaluation['details'].append(f"资产周转率{at:.2f}表现优秀")
        elif at < 0.5:
            evaluation['details'].append(f"资产周转率{at:.2f}偏低，资产效率待提升")

        if em >= 4:
            evaluation['details'].append(f"权益乘数{em:.2f}过高，财务杠杆风险大")
        elif em < 1.2:
            evaluation['details'].append(f"权益乘数{em:.2f}较低，可适度提升杠杆")

        return evaluation
