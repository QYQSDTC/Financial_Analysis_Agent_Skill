#!/Users/qyq/miniconda3/envs/quant/bin/python
# -*- coding: utf-8 -*-
"""
个股技术分析脚本
使用akshare获取数据，ta-lib计算技术指标，生成交易计划
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

import pandas as pd
import numpy as np

import os
# 禁用代理以确保直连
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

try:
    import akshare as ak
except ImportError:
    print("错误: 请安装 akshare: pip install akshare")
    sys.exit(1)

try:
    import talib
except ImportError:
    print("错误: 请安装 ta-lib")
    print("macOS: brew install ta-lib && pip install ta-lib")
    print("Ubuntu: apt-get install libta-lib-dev && pip install ta-lib")
    sys.exit(1)


class StockAnalyzer:
    """个股技术分析器"""
    
    def __init__(self, days: int = 90):
        """
        初始化分析器
        
        Args:
            days: 获取数据的天数，默认90天（约3个月）
        """
        self.days = days
        self.df: Optional[pd.DataFrame] = None
        self.stock_code: str = ""
        self.stock_name: str = ""
        self.indicators: Dict[str, Any] = {}
        
    def get_stock_code(self, name: str) -> Optional[str]:
        """根据股票名称获取股票代码"""
        try:
            # 获取A股股票列表
            stock_list = ak.stock_info_a_code_name()
            match = stock_list[stock_list['name'].str.contains(name, na=False)]
            if not match.empty:
                return match.iloc[0]['code']
            return None
        except Exception as e:
            print(f"查找股票代码失败: {e}")
            return None
    
    def get_stock_name(self, code: str) -> str:
        """根据股票代码获取股票名称"""
        try:
            stock_list = ak.stock_info_a_code_name()
            match = stock_list[stock_list['code'] == code]
            if not match.empty:
                return match.iloc[0]['name']
            return code
        except Exception:
            return code
    
    def fetch_data(self, code: str) -> bool:
        """
        获取股票历史数据
        
        Args:
            code: 股票代码（6位数字）
            
        Returns:
            是否成功获取数据
        """
        self.stock_code = code
        self.stock_name = self.get_stock_name(code)
        
        # 计算日期范围
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=self.days + 60)).strftime('%Y%m%d')  # 多取60天用于计算MA60
        
        # 判断市场（上海/深圳）
        if code.startswith('6'):
            symbol = f"sh{code}"
        else:
            symbol = f"sz{code}"
        
        # 尝试多种数据源
        df = None
        
        # 方法1: 尝试东方财富数据源
        try:
            df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                    start_date=start_date, end_date=end_date, 
                                    adjust="qfq")  # 前复权
            if df is not None and not df.empty:
                # 标准化列名（akshare返回中文列名，需要映射）
                column_mapping = {
                    '日期': 'date',
                    '股票代码': 'stock_code',
                    '开盘': 'open',
                    '收盘': 'close',
                    '最高': 'high',
                    '最低': 'low',
                    '成交量': 'volume',
                    '成交额': 'turnover',
                    '振幅': 'amplitude',
                    '涨跌幅': 'change_pct',
                    '涨跌额': 'change_amount',
                    '换手率': 'turnover_rate'
                }
                df = df.rename(columns=column_mapping)
        except Exception as e:
            print(f"东方财富数据源失败: {e}")
            df = None
        
        # 方法2: 如果东方财富失败，尝试新浪数据源
        if df is None or df.empty:
            try:
                print("尝试新浪数据源...")
                df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, 
                                         end_date=end_date, adjust="qfq")
                if df is not None and not df.empty:
                    # 新浪数据源列名已经是英文，但需要调整
                    # 列名: ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'outstanding_share', 'turnover']
                    df = df.rename(columns={'amount': 'turnover', 'turnover': 'turnover_rate'})
            except Exception as e:
                print(f"新浪数据源失败: {e}")
                df = None
        
        if df is None or df.empty:
            print(f"无法获取股票 {code} 的数据")
            return False
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        self.df = df
        return True
    
    def calculate_indicators(self) -> Dict[str, Any]:
        """计算所有技术指标"""
        if self.df is None or self.df.empty:
            return {}
        
        df = self.df
        close = df['close'].values
        high = df['high'].values
        low = df['low'].values
        volume = df['volume'].values
        
        # ===== 均线系统 =====
        ma5 = talib.SMA(close, timeperiod=5)
        ma10 = talib.SMA(close, timeperiod=10)
        ma20 = talib.SMA(close, timeperiod=20)
        ma60 = talib.SMA(close, timeperiod=60)
        
        # ===== MACD =====
        dif, dea, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        
        # ===== RSI =====
        rsi6 = talib.RSI(close, timeperiod=6)
        rsi12 = talib.RSI(close, timeperiod=12)
        rsi24 = talib.RSI(close, timeperiod=24)
        
        # ===== KDJ =====
        slowk, slowd = talib.STOCH(high, low, close, 
                                    fastk_period=9, slowk_period=3, slowk_matype=0,
                                    slowd_period=3, slowd_matype=0)
        j = 3 * slowk - 2 * slowd
        
        # ===== 布林带 =====
        upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        
        # ===== ATR (平均真实波幅) =====
        atr = talib.ATR(high, low, close, timeperiod=14)
        
        # ===== ADX (趋势强度) =====
        adx = talib.ADX(high, low, close, timeperiod=14)
        
        # ===== 成交量指标 =====
        # 5日平均成交量
        vol_ma5 = talib.SMA(volume.astype(float), timeperiod=5)
        # 量比
        current_vol = volume[-1]
        avg_vol = vol_ma5[-1] if not np.isnan(vol_ma5[-1]) else volume[-5:].mean()
        volume_ratio = current_vol / avg_vol if avg_vol > 0 else 1.0
        
        # OBV (能量潮)
        obv = talib.OBV(close, volume.astype(float))
        
        # 获取最新值
        latest_idx = -1
        
        self.indicators = {
            'ma': {
                'ma5': self._safe_value(ma5[latest_idx]),
                'ma10': self._safe_value(ma10[latest_idx]),
                'ma20': self._safe_value(ma20[latest_idx]),
                'ma60': self._safe_value(ma60[latest_idx]),
            },
            'macd': {
                'dif': self._safe_value(dif[latest_idx]),
                'dea': self._safe_value(dea[latest_idx]),
                'histogram': self._safe_value(macd_hist[latest_idx]),
                'prev_histogram': self._safe_value(macd_hist[-2]),
            },
            'rsi': {
                'rsi6': self._safe_value(rsi6[latest_idx]),
                'rsi12': self._safe_value(rsi12[latest_idx]),
                'rsi24': self._safe_value(rsi24[latest_idx]),
            },
            'kdj': {
                'k': self._safe_value(slowk[latest_idx]),
                'd': self._safe_value(slowd[latest_idx]),
                'j': self._safe_value(j[latest_idx]),
            },
            'bollinger': {
                'upper': self._safe_value(upper[latest_idx]),
                'middle': self._safe_value(middle[latest_idx]),
                'lower': self._safe_value(lower[latest_idx]),
                'bandwidth': self._safe_value((upper[latest_idx] - lower[latest_idx]) / middle[latest_idx] * 100),
                'prev_bandwidth': self._safe_value((upper[-2] - lower[-2]) / middle[-2] * 100) if len(upper) > 1 else None,
            },
            'atr': {
                'value': self._safe_value(atr[latest_idx]),
                'percent': self._safe_value(atr[latest_idx] / close[latest_idx] * 100),
            },
            'adx': {
                'value': self._safe_value(adx[latest_idx]),
            },
            'volume': {
                'current': int(current_vol),
                'avg_5': int(avg_vol) if not np.isnan(avg_vol) else 0,
                'volume_ratio': round(volume_ratio, 2),
                'obv': self._safe_value(obv[latest_idx]),
                'obv_prev': self._safe_value(obv[-2]) if len(obv) > 1 else None,
            },
            # 保存数组用于趋势分析
            '_arrays': {
                'ma5': ma5,
                'ma10': ma10,
                'ma20': ma20,
                'ma60': ma60,
                'macd_hist': macd_hist,
                'rsi6': rsi6,
                'upper': upper,
                'lower': lower,
            }
        }
        
        return self.indicators
    
    def _safe_value(self, val, decimals: int = 2) -> Optional[float]:
        """安全转换数值，处理NaN"""
        if val is None or (isinstance(val, float) and np.isnan(val)):
            return None
        return round(float(val), decimals)
    
    def analyze_trend(self) -> Dict[str, Any]:
        """分析当前趋势"""
        if not self.indicators or self.df is None:
            return {}
        
        df = self.df
        close = df['close'].values[-1]
        ma = self.indicators['ma']
        macd = self.indicators['macd']
        boll = self.indicators['bollinger']
        adx = self.indicators['adx']['value']
        volume = self.indicators['volume']
        
        # ===== 判断均线排列 =====
        ma_values = [ma['ma5'], ma['ma10'], ma['ma20'], ma['ma60']]
        if all(v is not None for v in ma_values):
            if ma['ma5'] > ma['ma10'] > ma['ma20'] > ma['ma60']:
                ma_arrangement = "多头排列"
                ma_score = 2
            elif ma['ma5'] < ma['ma10'] < ma['ma20'] < ma['ma60']:
                ma_arrangement = "空头排列"
                ma_score = -2
            elif ma['ma5'] > ma['ma10'] > ma['ma20']:
                ma_arrangement = "短期多头"
                ma_score = 1
            elif ma['ma5'] < ma['ma10'] < ma['ma20']:
                ma_arrangement = "短期空头"
                ma_score = -1
            else:
                ma_arrangement = "均线交织"
                ma_score = 0
        else:
            ma_arrangement = "数据不足"
            ma_score = 0
        
        # ===== 判断MACD信号 =====
        if macd['dif'] is not None and macd['dea'] is not None:
            if macd['dif'] > macd['dea']:
                if macd['histogram'] > 0 and (macd['prev_histogram'] is None or macd['histogram'] > macd['prev_histogram']):
                    macd_signal = "金叉放量"
                    macd_score = 2
                else:
                    macd_signal = "金叉"
                    macd_score = 1
            else:
                if macd['histogram'] < 0 and (macd['prev_histogram'] is None or macd['histogram'] < macd['prev_histogram']):
                    macd_signal = "死叉放量"
                    macd_score = -2
                else:
                    macd_signal = "死叉"
                    macd_score = -1
            
            # MACD柱状图缩量（趋势减弱）
            if macd['prev_histogram'] is not None:
                if abs(macd['histogram']) < abs(macd['prev_histogram']) * 0.8:
                    macd_signal += "(动能减弱)"
        else:
            macd_signal = "数据不足"
            macd_score = 0
        
        # ===== 判断布林带位置 =====
        if boll['upper'] is not None and boll['lower'] is not None:
            boll_position = (close - boll['lower']) / (boll['upper'] - boll['lower'])
            if boll_position > 0.8:
                boll_status = "接近上轨"
            elif boll_position < 0.2:
                boll_status = "接近下轨"
            elif 0.4 < boll_position < 0.6:
                boll_status = "中轨附近"
            else:
                boll_status = "中间区域"
                
            # 布林带收窄判断（突破前兆）
            if boll['bandwidth'] is not None and boll['prev_bandwidth'] is not None:
                if boll['bandwidth'] < 10:  # 带宽小于10%
                    boll_squeeze = True
                elif boll['bandwidth'] < boll['prev_bandwidth'] * 0.9:
                    boll_squeeze = True
                else:
                    boll_squeeze = False
            else:
                boll_squeeze = False
        else:
            boll_status = "数据不足"
            boll_position = 0.5
            boll_squeeze = False
        
        # ===== 计算支撑阻力位 =====
        support_level = self._calculate_support()
        resistance_level = self._calculate_resistance()
        
        # ===== 综合判断趋势 =====
        total_score = ma_score + macd_score
        
        # 判断是否即将突破
        is_breakout_pending = (
            boll_squeeze and 
            volume['volume_ratio'] > 1.2 and 
            abs(total_score) <= 1
        )
        
        if is_breakout_pending:
            trend = "即将突破"
            strength = "待确认"
        elif total_score >= 3:
            trend = "上涨趋势"
            strength = "强"
        elif total_score >= 1:
            trend = "上涨趋势"
            strength = "中等"
        elif total_score <= -3:
            trend = "下跌趋势"
            strength = "强"
        elif total_score <= -1:
            trend = "下跌趋势"
            strength = "中等"
        else:
            trend = "平台震荡"
            strength = "弱"
        
        # ADX趋势强度修正
        if adx is not None:
            if adx > 25:
                if strength == "弱":
                    strength = "中等"
            elif adx < 20 and trend != "平台震荡":
                trend = "平台震荡"
                strength = "弱"
        
        return {
            'trend': trend,
            'strength': strength,
            'score': total_score,
            'ma_arrangement': ma_arrangement,
            'macd_signal': macd_signal,
            'boll_status': boll_status,
            'boll_squeeze': boll_squeeze,
            'support_level': support_level,
            'resistance_level': resistance_level,
            'adx': adx,
        }
    
    def _calculate_support(self) -> Optional[float]:
        """计算支撑位"""
        if self.df is None:
            return None
        
        close = self.df['close'].values[-1]
        ma = self.indicators['ma']
        boll = self.indicators['bollinger']
        
        # 支撑位候选：MA20、MA60、布林下轨、近期低点
        candidates = []
        
        if ma['ma20'] is not None and ma['ma20'] < close:
            candidates.append(ma['ma20'])
        if ma['ma60'] is not None and ma['ma60'] < close:
            candidates.append(ma['ma60'])
        if boll['lower'] is not None:
            candidates.append(boll['lower'])
        
        # 近期低点
        recent_low = self.df['low'].tail(20).min()
        if recent_low < close:
            candidates.append(recent_low)
        
        if candidates:
            # 选择最接近当前价格的支撑
            return round(max(candidates), 2)
        return None
    
    def _calculate_resistance(self) -> Optional[float]:
        """计算阻力位"""
        if self.df is None:
            return None
        
        close = self.df['close'].values[-1]
        ma = self.indicators['ma']
        boll = self.indicators['bollinger']
        
        # 阻力位候选：MA20、MA60、布林上轨、近期高点
        candidates = []
        
        if ma['ma20'] is not None and ma['ma20'] > close:
            candidates.append(ma['ma20'])
        if ma['ma60'] is not None and ma['ma60'] > close:
            candidates.append(ma['ma60'])
        if boll['upper'] is not None:
            candidates.append(boll['upper'])
        
        # 近期高点
        recent_high = self.df['high'].tail(20).max()
        if recent_high > close:
            candidates.append(recent_high)
        
        if candidates:
            # 选择最接近当前价格的阻力
            return round(min(candidates), 2)
        return None
    
    def generate_trading_plan(self, trend_analysis: Dict) -> Dict[str, Any]:
        """生成交易计划"""
        if self.df is None or not self.indicators:
            return {}
        
        close = self.df['close'].values[-1]
        atr = self.indicators['atr']['value']
        rsi = self.indicators['rsi']
        kdj = self.indicators['kdj']
        volume = self.indicators['volume']
        
        trend = trend_analysis['trend']
        strength = trend_analysis['strength']
        support = trend_analysis['support_level']
        resistance = trend_analysis['resistance_level']
        
        # ===== 确定操作建议 =====
        reasons = []
        warnings = []
        
        if trend == "上涨趋势":
            if strength == "强":
                action = "买入/加仓"
                position_size = "30%-50%"
                reasons.append(f"趋势强劲，{trend_analysis['ma_arrangement']}")
            else:
                action = "持有/轻仓买入"
                position_size = "20%-30%"
                reasons.append(f"趋势向上，{trend_analysis['ma_arrangement']}")
            
            reasons.append(f"MACD{trend_analysis['macd_signal']}")
            
        elif trend == "下跌趋势":
            if strength == "强":
                action = "卖出/空仓"
                position_size = "0%"
                reasons.append(f"趋势向下，{trend_analysis['ma_arrangement']}")
            else:
                action = "减仓/观望"
                position_size = "0%-10%"
                reasons.append(f"趋势偏弱，{trend_analysis['ma_arrangement']}")
            
            reasons.append(f"MACD{trend_analysis['macd_signal']}")
            
        elif trend == "即将突破":
            action = "观望待突破"
            position_size = "10%-20%"
            reasons.append("布林带收窄，蓄势待发")
            reasons.append(f"量比{volume['volume_ratio']}，成交活跃")
            warnings.append("等待方向明确后再操作")
            
        else:  # 平台震荡
            action = "观望/高抛低吸"
            position_size = "10%-20%"
            reasons.append("价格在区间内震荡")
            warnings.append("避免追高杀低")
        
        # ===== RSI 超买超卖警告 =====
        if rsi['rsi6'] is not None:
            if rsi['rsi6'] > 80:
                warnings.append(f"RSI6={rsi['rsi6']:.0f}，严重超买")
            elif rsi['rsi6'] > 70:
                warnings.append(f"RSI6={rsi['rsi6']:.0f}，接近超买")
            elif rsi['rsi6'] < 20:
                warnings.append(f"RSI6={rsi['rsi6']:.0f}，严重超卖")
                if trend == "下跌趋势":
                    warnings.append("可能有反弹机会")
            elif rsi['rsi6'] < 30:
                warnings.append(f"RSI6={rsi['rsi6']:.0f}，接近超卖")
        
        # ===== KDJ 信号 =====
        if kdj['j'] is not None:
            if kdj['j'] > 100:
                warnings.append(f"KDJ J值={kdj['j']:.0f}，超买区")
            elif kdj['j'] < 0:
                warnings.append(f"KDJ J值={kdj['j']:.0f}，超卖区")
        
        # ===== 成交量警告 =====
        if volume['volume_ratio'] > 2:
            warnings.append(f"量比{volume['volume_ratio']}，成交量异常放大")
        elif volume['volume_ratio'] < 0.5:
            warnings.append(f"量比{volume['volume_ratio']}，成交清淡")
        
        # ===== 计算入场价、目标价、止损价 =====
        if action in ["买入/加仓", "持有/轻仓买入"]:
            entry_price = close  # 当前价入场
            # 目标价：阻力位或ATR的2-3倍
            if resistance:
                target_price = resistance
            else:
                target_price = close + (atr * 3 if atr else close * 0.1)
            # 止损：支撑位或ATR的1.5倍
            if support:
                stop_loss = support - (atr * 0.5 if atr else support * 0.02)
            else:
                stop_loss = close - (atr * 1.5 if atr else close * 0.05)
        elif action == "观望待突破":
            # 突破后再入场
            entry_price = resistance if resistance else close * 1.02  # 突破阻力后买入
            target_price = entry_price * 1.1  # 目标10%
            stop_loss = support if support else close * 0.95
        else:
            entry_price = None
            target_price = None
            stop_loss = support if support else close * 0.95
        
        # ===== 计算风险收益比 =====
        if entry_price and target_price and stop_loss and entry_price > stop_loss:
            potential_profit = target_price - entry_price
            potential_loss = entry_price - stop_loss
            risk_reward = round(potential_profit / potential_loss, 2) if potential_loss > 0 else 0
        else:
            risk_reward = None
        
        return {
            'action': action,
            'entry_price': round(entry_price, 2) if entry_price else None,
            'target_price': round(target_price, 2) if target_price else None,
            'stop_loss': round(stop_loss, 2) if stop_loss else None,
            'position_size': position_size,
            'risk_reward_ratio': risk_reward,
            'reasons': reasons,
            'warnings': warnings,
        }
    
    def analyze(self, code: str = None, name: str = None) -> Dict[str, Any]:
        """
        执行完整分析
        
        Args:
            code: 股票代码
            name: 股票名称（二选一）
            
        Returns:
            完整分析结果
        """
        # 获取股票代码
        if name and not code:
            code = self.get_stock_code(name)
            if not code:
                return {'error': f'未找到股票: {name}'}
        
        if not code:
            return {'error': '请提供股票代码或名称'}
        
        # 获取数据
        if not self.fetch_data(code):
            return {'error': f'获取股票数据失败: {code}'}
        
        # 计算指标
        self.calculate_indicators()
        
        # 分析趋势
        trend_analysis = self.analyze_trend()
        
        # 生成交易计划
        trading_plan = self.generate_trading_plan(trend_analysis)
        
        # 当前价格信息
        df = self.df
        current_price = df['close'].values[-1]
        prev_close = df['close'].values[-2] if len(df) > 1 else current_price
        change_pct = (current_price - prev_close) / prev_close * 100
        
        # 移除内部数组数据
        indicators_clean = {k: v for k, v in self.indicators.items() if not k.startswith('_')}
        
        return {
            'stock_info': {
                'code': self.stock_code,
                'name': self.stock_name,
                'current_price': round(current_price, 2),
                'change_pct': round(change_pct, 2),
                'date': df['date'].values[-1].astype('datetime64[D]').astype(str),
            },
            'indicators': indicators_clean,
            'trend_analysis': trend_analysis,
            'trading_plan': trading_plan,
            'data_range': {
                'start_date': df['date'].values[0].astype('datetime64[D]').astype(str),
                'end_date': df['date'].values[-1].astype('datetime64[D]').astype(str),
                'days': len(df),
            }
        }


def format_output(result: Dict[str, Any]) -> str:
    """格式化输出结果"""
    if 'error' in result:
        return f"错误: {result['error']}"
    
    stock = result['stock_info']
    trend = result['trend_analysis']
    plan = result['trading_plan']
    indicators = result['indicators']
    data_range = result['data_range']
    
    output = []
    output.append("=" * 60)
    output.append(f"📊 {stock['name']} ({stock['code']}) 技术分析报告")
    output.append("=" * 60)
    output.append(f"📅 数据范围: {data_range['start_date']} ~ {data_range['end_date']} ({data_range['days']}个交易日)")
    output.append(f"💰 当前价格: {stock['current_price']} ({'+' if stock['change_pct'] >= 0 else ''}{stock['change_pct']}%)")
    output.append("")
    
    # 趋势分析
    output.append("📈 趋势分析")
    output.append("-" * 40)
    trend_emoji = {"上涨趋势": "🟢", "下跌趋势": "🔴", "平台震荡": "🟡", "即将突破": "⚡"}
    output.append(f"趋势状态: {trend_emoji.get(trend['trend'], '⚪')} {trend['trend']} ({trend['strength']})")
    output.append(f"均线排列: {trend['ma_arrangement']}")
    output.append(f"MACD信号: {trend['macd_signal']}")
    output.append(f"布林位置: {trend['boll_status']}" + (" [布林收窄]" if trend['boll_squeeze'] else ""))
    if trend['support_level']:
        output.append(f"支撑位: {trend['support_level']}")
    if trend['resistance_level']:
        output.append(f"阻力位: {trend['resistance_level']}")
    if trend['adx']:
        output.append(f"趋势强度(ADX): {trend['adx']:.1f}")
    output.append("")
    
    # 技术指标
    output.append("📉 关键指标")
    output.append("-" * 40)
    ma = indicators['ma']
    output.append(f"MA: 5日={ma['ma5']} | 10日={ma['ma10']} | 20日={ma['ma20']} | 60日={ma['ma60']}")
    
    macd = indicators['macd']
    output.append(f"MACD: DIF={macd['dif']} | DEA={macd['dea']} | 柱状={macd['histogram']}")
    
    rsi = indicators['rsi']
    output.append(f"RSI: 6日={rsi['rsi6']:.0f} | 12日={rsi['rsi12']:.0f} | 24日={rsi['rsi24']:.0f}" if rsi['rsi6'] else "RSI: 数据不足")
    
    kdj = indicators['kdj']
    output.append(f"KDJ: K={kdj['k']:.0f} | D={kdj['d']:.0f} | J={kdj['j']:.0f}" if kdj['k'] else "KDJ: 数据不足")
    
    vol = indicators['volume']
    output.append(f"成交量: 量比={vol['volume_ratio']}")
    output.append("")
    
    # 交易计划
    output.append("📋 交易计划")
    output.append("-" * 40)
    action_emoji = {"买入/加仓": "🟢", "持有/轻仓买入": "🟢", "持有/加仓": "🟢",
                   "卖出/空仓": "🔴", "减仓/观望": "🔴",
                   "观望待突破": "🟡", "观望/高抛低吸": "🟡"}
    output.append(f"操作建议: {action_emoji.get(plan['action'], '⚪')} {plan['action']}")
    output.append(f"建议仓位: {plan['position_size']}")
    
    if plan['entry_price']:
        output.append(f"入场价格: {plan['entry_price']}")
    if plan['target_price']:
        output.append(f"目标价格: {plan['target_price']}")
    if plan['stop_loss']:
        output.append(f"止损价格: {plan['stop_loss']}")
    if plan['risk_reward_ratio']:
        output.append(f"风险收益比: 1:{plan['risk_reward_ratio']}")
    
    output.append("")
    output.append("📌 依据:")
    for reason in plan['reasons']:
        output.append(f"  ✓ {reason}")
    
    if plan['warnings']:
        output.append("")
        output.append("⚠️ 警告:")
        for warning in plan['warnings']:
            output.append(f"  ⚠ {warning}")
    
    output.append("")
    output.append("=" * 60)
    output.append("⚠️ 风险提示: 本分析仅供参考，不构成投资建议。")
    output.append("   股市有风险，投资需谨慎。")
    output.append("=" * 60)
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='个股技术分析工具')
    parser.add_argument('--code', '-c', type=str, help='股票代码（6位数字）')
    parser.add_argument('--name', '-n', type=str, help='股票名称')
    parser.add_argument('--days', '-d', type=int, default=90, help='获取数据天数（默认90天）')
    parser.add_argument('--format', '-f', type=str, choices=['text', 'json'], default='text',
                       help='输出格式：text（默认）或 json')
    
    args = parser.parse_args()
    
    if not args.code and not args.name:
        parser.error("请提供股票代码(--code)或股票名称(--name)")
    
    analyzer = StockAnalyzer(days=args.days)
    result = analyzer.analyze(code=args.code, name=args.name)
    
    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == '__main__':
    main()
