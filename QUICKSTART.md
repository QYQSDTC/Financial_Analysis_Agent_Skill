# 快速开始指南 ⚡

## 一键安装

```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Development/agent_skills
./install.sh
```

## 三种使用方式

### 🤖 方式 1：在 Claude Code 中使用（最简单）

**在 Claude Code 对话中直接说：**

```
"帮我分析这个财报：~/Downloads/某公司2023年报.pdf，股价28.5元"
```

我会自动：
1. 解析PDF提取财务数据
2. 计算30+项财务指标
3. 进行AI深度分析
4. 生成投资建议
5. 输出详细报告

### 💻 方式 2：命令行使用

```bash
# 基本分析
./analyze-report 财报.pdf

# 包含股价
./analyze-report 财报.pdf --price 28.5

# 指定投资者类型
./analyze-report 财报.pdf --price 28.5 --investor-type 稳健型

# 完整示例
./analyze-report ~/Downloads/贵州茅台_2023年报.pdf \
  --price 1680 \
  --investor-type 稳健型 \
  --output-dir ./reports
```

**输出：**
- ✅ Markdown 分析报告
- ✅ Excel 财务数据表
- ✅ 投资评级和建议

### 🐍 方式 3：Python 代码中使用

```python
from financial_analyzer import (
    FinancialReportParser,
    FinancialAnalyzer
)

# 一行代码分析
parser = FinancialReportParser()
statement = parser.parse_pdf("财报.pdf")

# 查看结果
print(f"公司: {statement.company_name}")
print(f"ROE: {statement.balance_sheet.get('roe')}%")
```

## 关键功能

✅ **自动提取**：资产负债表、利润表、现金流量表
✅ **智能计算**：ROE、毛利率、资产负债率等30+指标
✅ **AI分析**：识别优势、风险、投资机会
✅ **投资建议**：评级 + 目标价 + 买入价 + 止损价
✅ **专业报告**：Markdown + Excel 双格式输出

## 示例输出

```
✅ 分析完成！
====================================
📊 贵州茅台 - 年报
📅 报告期: 2023-12-31

💯 综合评分: 92.3/100
⭐ 综合评级: 优秀
📈 投资评级: 强烈推荐
💡 操作建议: 买入

💰 当前价格: 1680.00 元
🎯 目标价格: 2100.00 元
📊 上涨空间: +25.00%

📄 报告文件:
   - 贵州茅台_2023-12-31_分析报告.md
   - 贵州茅台_2023-12-31_数据.xlsx
====================================
```

## 可选配置

### 启用 AI 深度分析
```bash
export ANTHROPIC_API_KEY="your_api_key"
```

不设置也能用，只是分析会更基础一些。

## 常见问题

**Q: PDF 解析失败怎么办？**
A: 确保PDF是文字版（非扫描版），格式为标准财报格式

**Q: 如何批量分析多个季度？**
A: 在 Claude Code 中说 "帮我批量分析这些财报：Q1.pdf, Q2.pdf, Q3.pdf, Q4.pdf"

**Q: 能否自定义指标？**
A: 可以，修改 `financial_analyzer/indicators/calculator.py` 中的评分函数

---

**需要帮助？** 查看 [README.md](README.md) 或在 Claude Code 中问我！
