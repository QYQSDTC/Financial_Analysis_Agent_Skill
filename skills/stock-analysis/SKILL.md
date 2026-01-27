---
name: stock-analysis
description: 个股技术分析技能。使用akshare获取A股数据，ta-lib计算技术指标（MA、MACD、RSI、KDJ、布林带等），分析股票趋势（上涨、震荡、即将突破），生成明确的交易计划。当用户请求分析某只股票、判断买卖点、技术面分析时使用此技能。
---

# 个股技术分析技能

基于技术指标的A股个股分析工具，支持：
- 使用 akshare 获取股票历史行情数据（默认3个月）
- 使用 ta-lib 计算多种技术指标
- 判断股票当前趋势状态
- 生成明确的交易计划和建议

## 快速使用

当用户说"使用 stock analysis skill 分析 XXX 股票"时：

1. **获取股票代码** - 从用户输入中提取股票代码或名称
2. **运行分析脚本** - 执行技术分析
3. **解读结果** - 向用户展示分析结论和交易计划

## 分析流程

```bash
# 基础用法（默认3个月数据）
python scripts/stock_analyzer.py --code 000001

# 指定时间范围
python scripts/stock_analyzer.py --code 000001 --days 90

# 指定股票名称（自动查找代码）
python scripts/stock_analyzer.py --name 平安银行

# 输出JSON格式
python scripts/stock_analyzer.py --code 000001 --format json
```

## 技术指标

### 趋势指标
- **MA均线系统**: MA5/MA10/MA20/MA60，判断多空排列
- **MACD**: DIF/DEA/柱状图，判断趋势强度和转折
- **ADX**: 趋势强度指标

### 超买超卖指标
- **RSI**: 相对强弱指标，判断超买超卖
- **KDJ**: 随机指标，捕捉短期转折点

### 波动指标
- **布林带**: 判断价格位置和突破信号
- **ATR**: 平均真实波幅，用于止损设置

### 成交量指标
- **量比**: 当日成交量vs近期平均
- **OBV**: 能量潮指标

## 趋势判断

脚本自动判断以下趋势状态：

| 状态 | 判断依据 |
|------|----------|
| **上涨趋势** | MA多头排列 + MACD金叉 + 价格在布林中轨上方 |
| **下跌趋势** | MA空头排列 + MACD死叉 + 价格在布林中轨下方 |
| **平台震荡** | MA交织 + MACD柱状图缩量 + 布林带收窄 |
| **即将突破** | 布林带极度收窄 + 成交量异动 + 价格接近关键位 |

## 输出结构

分析结果包含以下部分：

```python
{
    "stock_info": {
        "code": "000001",
        "name": "平安银行",
        "current_price": 12.50,
        "change_pct": 1.25
    },
    "indicators": {
        "ma": {"ma5": 12.3, "ma10": 12.1, "ma20": 11.8, "ma60": 11.5},
        "macd": {"dif": 0.15, "dea": 0.12, "histogram": 0.03},
        "rsi": {"rsi6": 55, "rsi12": 52, "rsi24": 50},
        "kdj": {"k": 60, "d": 55, "j": 70},
        "bollinger": {"upper": 13.0, "middle": 12.2, "lower": 11.4},
        "volume": {"volume_ratio": 1.2, "avg_volume_5": 50000000}
    },
    "trend_analysis": {
        "trend": "上涨趋势",  # 上涨趋势/下跌趋势/平台震荡/即将突破
        "strength": "中等",  # 强/中等/弱
        "ma_arrangement": "多头排列",
        "macd_signal": "金叉",
        "support_level": 11.8,
        "resistance_level": 13.0
    },
    "trading_plan": {
        "action": "持有/加仓",  # 买入/持有/加仓/减仓/卖出/观望
        "entry_price": 12.3,
        "target_price": 13.5,
        "stop_loss": 11.5,
        "position_size": "30%",  # 建议仓位
        "risk_reward_ratio": 1.5,
        "reasons": ["MA多头排列", "MACD金叉确认", "成交量配合"],
        "warnings": ["RSI接近超买区", "注意大盘风险"]
    }
}
```

## 交易计划说明

### 操作建议
- **买入**: 趋势向上 + 技术面支持 + 风险可控
- **加仓**: 上涨趋势中回踩支撑
- **持有**: 趋势延续，无明显卖出信号
- **减仓**: 趋势转弱或接近阻力位
- **卖出**: 趋势反转信号明确
- **观望**: 趋势不明朗，等待信号

### 仓位建议
- 强势上涨趋势：30%-50%
- 普通上涨趋势：20%-30%
- 震荡/突破前：10%-20%
- 下跌趋势：空仓或极低仓位

### 止损设置
- 基于ATR的动态止损
- 关键支撑位下方
- 通常为入场价的3%-5%

## 使用示例

### 示例1：基础分析

用户：使用 stock analysis skill 分析 贵州茅台

执行：
```bash
python scripts/stock_analyzer.py --name 贵州茅台
```

### 示例2：指定代码分析

用户：分析一下 600519 这只股票

执行：
```bash
python scripts/stock_analyzer.py --code 600519
```

### 示例3：更长时间范围

用户：分析 000858 近半年走势

执行：
```bash
python scripts/stock_analyzer.py --code 000858 --days 180
```

## 注意事项

1. **数据来源**: 使用akshare获取数据，可能存在延迟
2. **技术分析局限**: 技术指标是滞后指标，不能预测未来
3. **风险提示**: 本工具仅供参考，不构成投资建议
4. **市场风险**: 需结合大盘走势和基本面综合判断

## 依赖安装

```bash
pip install akshare ta-lib pandas numpy
```

注意：ta-lib 需要先安装C语言库：
- macOS: `brew install ta-lib`
- Ubuntu: `apt-get install libta-lib-dev`
- Windows: 下载预编译wheel安装

## 脚本详情

详细实现见 [scripts/stock_analyzer.py](scripts/stock_analyzer.py)
