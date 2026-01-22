"""
多期趋势分析模块
分析财务指标趋势、检测转折点、生成预警
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


class TrendDirection(Enum):
    """趋势方向"""
    UP = "上升"
    DOWN = "下降"
    STABLE = "稳定"
    VOLATILE = "波动"


class AlertLevel(Enum):
    """预警级别"""
    CRITICAL = "严重"
    WARNING = "警告"
    CAUTION = "注意"
    INFO = "提示"


class MultiPeriodTrendAnalyzer:
    """
    多期趋势分析器

    支持分析多期财务数据的趋势变化，检测转折点和异常，生成预警
    """

    def __init__(self):
        """初始化趋势分析器"""
        self.period_data = []  # 存储多期数据
        self.alerts = []  # 预警列表

    def add_period_data(
        self,
        period: str,
        balance_sheet: Dict[str, float],
        income_statement: Dict[str, float],
        cashflow_statement: Dict[str, float],
        indicators: Dict[str, Dict[str, float]] = None
    ) -> None:
        """
        添加一期财务数据

        Args:
            period: 期间标识 (如 "2023Q4", "2023-12-31")
            balance_sheet: 资产负债表数据
            income_statement: 利润表数据
            cashflow_statement: 现金流量表数据
            indicators: 已计算的财务指标（可选）
        """
        self.period_data.append({
            'period': period,
            'balance_sheet': balance_sheet,
            'income_statement': income_statement,
            'cashflow_statement': cashflow_statement,
            'indicators': indicators or {}
        })

    def analyze_metric_trend(
        self,
        metric_path: str,
        min_periods: int = 3
    ) -> Dict:
        """
        分析单个指标的趋势

        Args:
            metric_path: 指标路径，如 "profitability.roe" 或 "income_statement.net_profit"
            min_periods: 最少需要的期数

        Returns:
            趋势分析结果
        """
        if len(self.period_data) < min_periods:
            return {
                'status': 'insufficient_data',
                'message': f'数据期数不足，需要至少{min_periods}期数据'
            }

        # 提取指标序列
        values = self._extract_metric_values(metric_path)
        if not values:
            return {
                'status': 'metric_not_found',
                'message': f'未找到指标: {metric_path}'
            }

        periods = [p['period'] for p in self.period_data]

        # 计算趋势统计
        trend_stats = self._calculate_trend_stats(values)

        # 检测转折点
        turning_points = self.detect_turning_points(values, periods)

        # 判断趋势方向
        direction = self._determine_trend_direction(values, trend_stats)

        return {
            'metric': metric_path,
            'periods': periods,
            'values': values,
            'direction': direction.value,
            'statistics': trend_stats,
            'turning_points': turning_points,
            'latest_value': values[-1] if values else None,
            'change_from_first': self._calculate_change(values[0], values[-1]) if len(values) >= 2 else None
        }

    def _extract_metric_values(self, metric_path: str) -> List[float]:
        """提取指标值序列"""
        values = []
        parts = metric_path.split('.')

        for period_data in self.period_data:
            value = None

            if len(parts) == 1:
                # 单级路径，从所有数据源查找
                for source in ['balance_sheet', 'income_statement', 'cashflow_statement']:
                    if parts[0] in period_data.get(source, {}):
                        value = period_data[source][parts[0]]
                        break
            elif len(parts) == 2:
                # 双级路径
                source_key, metric_key = parts
                source_data = period_data.get(source_key, {})
                if isinstance(source_data, dict):
                    value = source_data.get(metric_key)

            if value is not None:
                values.append(value)

        return values

    def _calculate_trend_stats(self, values: List[float]) -> Dict:
        """计算趋势统计量"""
        if not values:
            return {}

        n = len(values)
        mean_val = sum(values) / n
        variance = sum((x - mean_val) ** 2 for x in values) / n if n > 0 else 0
        std_dev = math.sqrt(variance)

        # 计算变异系数
        cv = (std_dev / mean_val * 100) if mean_val != 0 else 0

        # 计算最大回撤
        max_drawdown = self._calculate_max_drawdown(values)

        # 计算线性回归斜率（简化版）
        slope = self._calculate_slope(values)

        return {
            'mean': round(mean_val, 4),
            'std_dev': round(std_dev, 4),
            'coefficient_of_variation': round(cv, 2),
            'max_value': max(values),
            'min_value': min(values),
            'max_drawdown': round(max_drawdown, 2),
            'slope': round(slope, 4),
            'periods_count': n
        }

    def _calculate_max_drawdown(self, values: List[float]) -> float:
        """计算最大回撤百分比"""
        if len(values) < 2:
            return 0

        max_drawdown = 0
        peak = values[0]

        for value in values[1:]:
            if value > peak:
                peak = value
            else:
                drawdown = (peak - value) / peak * 100 if peak != 0 else 0
                max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown

    def _calculate_slope(self, values: List[float]) -> float:
        """计算线性回归斜率（简化版最小二乘法）"""
        n = len(values)
        if n < 2:
            return 0

        x_mean = (n - 1) / 2
        y_mean = sum(values) / n

        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        return numerator / denominator if denominator != 0 else 0

    def _determine_trend_direction(
        self,
        values: List[float],
        stats: Dict
    ) -> TrendDirection:
        """判断趋势方向"""
        if len(values) < 2:
            return TrendDirection.STABLE

        slope = stats.get('slope', 0)
        cv = stats.get('coefficient_of_variation', 0)

        # 高波动性
        if cv > 30:
            return TrendDirection.VOLATILE

        # 根据斜率判断方向
        # 使用相对斜率（相对于均值的变化）
        mean_val = stats.get('mean', 1)
        relative_slope = slope / abs(mean_val) * 100 if mean_val != 0 else 0

        if relative_slope > 5:
            return TrendDirection.UP
        elif relative_slope < -5:
            return TrendDirection.DOWN
        else:
            return TrendDirection.STABLE

    def detect_turning_points(
        self,
        values: List[float],
        periods: List[str]
    ) -> List[Dict]:
        """
        检测转折点

        Args:
            values: 指标值序列
            periods: 期间标识序列

        Returns:
            转折点列表
        """
        turning_points = []

        if len(values) < 3:
            return turning_points

        for i in range(1, len(values) - 1):
            prev_val = values[i - 1]
            curr_val = values[i]
            next_val = values[i + 1]

            # 检测峰值
            if curr_val > prev_val and curr_val > next_val:
                change_before = self._calculate_change(prev_val, curr_val)
                change_after = self._calculate_change(curr_val, next_val)
                if abs(change_before) > 5 or abs(change_after) > 5:
                    turning_points.append({
                        'period': periods[i],
                        'type': '峰值',
                        'value': curr_val,
                        'change_before': change_before,
                        'change_after': change_after
                    })

            # 检测谷值
            elif curr_val < prev_val and curr_val < next_val:
                change_before = self._calculate_change(prev_val, curr_val)
                change_after = self._calculate_change(curr_val, next_val)
                if abs(change_before) > 5 or abs(change_after) > 5:
                    turning_points.append({
                        'period': periods[i],
                        'type': '谷值',
                        'value': curr_val,
                        'change_before': change_before,
                        'change_after': change_after
                    })

        return turning_points

    def _calculate_change(self, old_value: float, new_value: float) -> float:
        """计算变化百分比"""
        if old_value == 0:
            return 0 if new_value == 0 else 100
        return ((new_value - old_value) / abs(old_value)) * 100

    def calculate_cagr(
        self,
        metric_path: str,
        years: int = None
    ) -> Optional[float]:
        """
        计算复合年增长率 (CAGR)

        Args:
            metric_path: 指标路径
            years: 年数，如不指定则根据数据期数推算

        Returns:
            CAGR百分比
        """
        values = self._extract_metric_values(metric_path)

        if len(values) < 2:
            return None

        beginning_value = values[0]
        ending_value = values[-1]

        if beginning_value <= 0 or ending_value <= 0:
            return None

        # 如果未指定年数，假设每期数据代表一年
        if years is None:
            years = len(values) - 1

        if years <= 0:
            return None

        # CAGR = (终值/初值)^(1/年数) - 1
        cagr = ((ending_value / beginning_value) ** (1 / years) - 1) * 100

        return round(cagr, 2)

    def generate_alerts(self) -> List[Dict]:
        """
        生成预警

        Returns:
            预警列表
        """
        self.alerts = []

        if len(self.period_data) < 2:
            return self.alerts

        latest = self.period_data[-1]
        previous = self.period_data[-2]

        # 盈利能力预警
        self._check_profitability_alerts(latest, previous)

        # 偿债能力预警
        self._check_solvency_alerts(latest, previous)

        # 现金流预警
        self._check_cashflow_alerts(latest, previous)

        # 多期连续下滑预警
        self._check_consecutive_decline_alerts()

        return self.alerts

    def _check_profitability_alerts(
        self,
        latest: Dict,
        previous: Dict
    ) -> None:
        """检查盈利能力预警"""
        latest_ind = latest.get('indicators', {}).get('profitability', {})
        prev_ind = previous.get('indicators', {}).get('profitability', {})

        # ROE预警
        roe = latest_ind.get('roe', 0)
        prev_roe = prev_ind.get('roe', 0)

        if roe < 5:
            self.alerts.append({
                'level': AlertLevel.WARNING.value,
                'category': '盈利能力',
                'metric': 'ROE',
                'message': f'ROE({roe:.2f}%)低于5%警戒线，盈利能力较弱',
                'value': roe,
                'threshold': 5
            })

        if prev_roe > 0 and roe < prev_roe * 0.7:
            change = ((roe - prev_roe) / prev_roe) * 100
            self.alerts.append({
                'level': AlertLevel.WARNING.value,
                'category': '盈利能力',
                'metric': 'ROE',
                'message': f'ROE较上期下降{abs(change):.1f}%，降幅超过30%',
                'value': roe,
                'previous_value': prev_roe,
                'change': change
            })

        # 净利率预警
        net_margin = latest_ind.get('net_margin', 0)
        if net_margin < 3:
            self.alerts.append({
                'level': AlertLevel.CAUTION.value,
                'category': '盈利能力',
                'metric': '净利率',
                'message': f'净利率({net_margin:.2f}%)过低，盈利空间狭窄',
                'value': net_margin,
                'threshold': 3
            })

    def _check_solvency_alerts(
        self,
        latest: Dict,
        previous: Dict
    ) -> None:
        """检查偿债能力预警"""
        latest_ind = latest.get('indicators', {}).get('solvency', {})

        # 流动比率预警
        current_ratio = latest_ind.get('current_ratio', 0)
        if current_ratio < 1:
            level = AlertLevel.CRITICAL if current_ratio < 0.8 else AlertLevel.WARNING
            self.alerts.append({
                'level': level.value,
                'category': '偿债能力',
                'metric': '流动比率',
                'message': f'流动比率({current_ratio:.2f})低于1，存在流动性风险',
                'value': current_ratio,
                'threshold': 1
            })

        # 资产负债率预警
        debt_ratio = latest_ind.get('debt_to_asset', 0)
        if debt_ratio > 70:
            level = AlertLevel.CRITICAL if debt_ratio > 80 else AlertLevel.WARNING
            self.alerts.append({
                'level': level.value,
                'category': '偿债能力',
                'metric': '资产负债率',
                'message': f'资产负债率({debt_ratio:.2f}%)过高，财务风险较大',
                'value': debt_ratio,
                'threshold': 70
            })

        # 利息保障倍数预警
        interest_coverage = latest_ind.get('interest_coverage', 0)
        if interest_coverage > 0 and interest_coverage < 2:
            self.alerts.append({
                'level': AlertLevel.WARNING.value,
                'category': '偿债能力',
                'metric': '利息保障倍数',
                'message': f'利息保障倍数({interest_coverage:.2f})偏低，债务偿付能力不足',
                'value': interest_coverage,
                'threshold': 2
            })

    def _check_cashflow_alerts(
        self,
        latest: Dict,
        previous: Dict
    ) -> None:
        """检查现金流预警"""
        latest_cf = latest.get('cashflow_statement', {})
        latest_ind = latest.get('indicators', {}).get('cashflow_quality', {})

        # 经营现金流为负
        operating_cf = latest_cf.get('operating_cashflow', 0)
        if operating_cf < 0:
            self.alerts.append({
                'level': AlertLevel.WARNING.value,
                'category': '现金流',
                'metric': '经营现金流',
                'message': '经营活动现金流为负，可能存在经营困难',
                'value': operating_cf
            })

        # 现金净利比过低
        cf_to_profit = latest_ind.get('operating_cf_to_net_profit', 0)
        if 0 < cf_to_profit < 50:
            self.alerts.append({
                'level': AlertLevel.CAUTION.value,
                'category': '现金流',
                'metric': '现金净利比',
                'message': f'现金净利比({cf_to_profit:.1f}%)偏低，利润质量存疑',
                'value': cf_to_profit,
                'threshold': 50
            })

    def _check_consecutive_decline_alerts(self) -> None:
        """检查连续下滑预警"""
        if len(self.period_data) < 3:
            return

        # 检查关键指标是否连续下滑
        key_metrics = [
            ('profitability.roe', 'ROE', 3),
            ('profitability.net_margin', '净利率', 3),
            ('income_statement.net_profit', '净利润', 3),
            ('income_statement.operating_revenue', '营业收入', 3)
        ]

        for metric_path, metric_name, consecutive_periods in key_metrics:
            values = self._extract_metric_values(metric_path)

            if len(values) >= consecutive_periods:
                # 检查最近N期是否连续下滑
                recent_values = values[-consecutive_periods:]
                is_declining = all(
                    recent_values[i] > recent_values[i + 1]
                    for i in range(len(recent_values) - 1)
                )

                if is_declining:
                    total_decline = self._calculate_change(
                        recent_values[0], recent_values[-1]
                    )
                    self.alerts.append({
                        'level': AlertLevel.WARNING.value,
                        'category': '趋势预警',
                        'metric': metric_name,
                        'message': f'{metric_name}连续{consecutive_periods}期下滑，'
                                   f'累计下降{abs(total_decline):.1f}%',
                        'values': recent_values,
                        'total_change': total_decline
                    })

    def get_trend_summary(self) -> Dict:
        """
        获取趋势分析摘要

        Returns:
            趋势分析摘要
        """
        if len(self.period_data) < 2:
            return {'status': 'insufficient_data'}

        summary = {
            'periods_analyzed': len(self.period_data),
            'date_range': {
                'start': self.period_data[0]['period'],
                'end': self.period_data[-1]['period']
            },
            'key_trends': {},
            'alerts': self.generate_alerts()
        }

        # 分析关键指标趋势
        key_metrics = [
            'profitability.roe',
            'profitability.net_margin',
            'solvency.current_ratio',
            'solvency.debt_to_asset',
            'operational.asset_turnover',
            'cashflow_quality.operating_cf_to_net_profit'
        ]

        for metric in key_metrics:
            trend = self.analyze_metric_trend(metric)
            if trend.get('status') != 'metric_not_found':
                metric_name = metric.split('.')[-1]
                summary['key_trends'][metric_name] = {
                    'direction': trend.get('direction'),
                    'latest_value': trend.get('latest_value'),
                    'change': trend.get('change_from_first')
                }

        # 计算关键指标的CAGR
        summary['cagr'] = {}
        for metric in ['income_statement.operating_revenue', 'income_statement.net_profit']:
            cagr = self.calculate_cagr(metric)
            if cagr is not None:
                metric_name = metric.split('.')[-1]
                summary['cagr'][metric_name] = cagr

        return summary

    def get_alert_summary(self) -> Dict:
        """
        获取预警摘要

        Returns:
            按级别分类的预警统计
        """
        alerts = self.generate_alerts()

        summary = {
            'total_alerts': len(alerts),
            'by_level': {
                AlertLevel.CRITICAL.value: [],
                AlertLevel.WARNING.value: [],
                AlertLevel.CAUTION.value: [],
                AlertLevel.INFO.value: []
            },
            'by_category': {}
        }

        for alert in alerts:
            level = alert['level']
            category = alert['category']

            summary['by_level'][level].append(alert)

            if category not in summary['by_category']:
                summary['by_category'][category] = []
            summary['by_category'][category].append(alert)

        return summary
