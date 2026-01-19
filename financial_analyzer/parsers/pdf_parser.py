"""
PDF财务报表解析器
支持从PDF格式的财报中智能提取结构化数据
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import pdfplumber
import pandas as pd


@dataclass
class FinancialStatement:
    """财务报表数据结构"""
    company_name: str
    report_period: str
    report_type: str  # 季报/半年报/年报

    # 资产负债表
    balance_sheet: Dict[str, float]

    # 利润表
    income_statement: Dict[str, float]

    # 现金流量表
    cashflow_statement: Dict[str, float]

    # 其他关键信息
    metadata: Dict[str, any]


class FinancialReportParser:
    """财务报表PDF解析器"""

    def __init__(self):
        """初始化解析器"""
        self.current_statement = None

        # 关键财务指标的中英文映射
        self.key_items = {
            # 资产负债表
            '总资产': 'total_assets',
            '流动资产': 'current_assets',
            '货币资金': 'cash_and_equivalents',
            '应收账款': 'accounts_receivable',
            '存货': 'inventory',
            '固定资产': 'fixed_assets',
            '无形资产': 'intangible_assets',
            '总负债': 'total_liabilities',
            '流动负债': 'current_liabilities',
            '短期借款': 'short_term_debt',
            '应付账款': 'accounts_payable',
            '长期借款': 'long_term_debt',
            '股东权益': 'shareholders_equity',
            '实收资本': 'paid_in_capital',
            '未分配利润': 'retained_earnings',

            # 利润表
            '营业收入': 'operating_revenue',
            '营业成本': 'operating_cost',
            '营业利润': 'operating_profit',
            '利润总额': 'total_profit',
            '净利润': 'net_profit',
            '归属于母公司股东的净利润': 'net_profit_attributable',
            '扣非净利润': 'adjusted_net_profit',
            '毛利润': 'gross_profit',
            '销售费用': 'selling_expenses',
            '管理费用': 'administrative_expenses',
            '财务费用': 'financial_expenses',
            '研发费用': 'rd_expenses',
            '基本每股收益': 'basic_eps',

            # 现金流量表
            '经营活动产生的现金流量净额': 'operating_cashflow',
            '投资活动产生的现金流量净额': 'investing_cashflow',
            '筹资活动产生的现金流量净额': 'financing_cashflow',
            '现金及现金等价物净增加额': 'net_cashflow',
            '销售商品提供劳务收到的现金': 'cash_from_sales',
            '购买商品接受劳务支付的现金': 'cash_for_purchases',
        }

    def parse_pdf(self, pdf_path: str) -> FinancialStatement:
        """
        解析PDF财务报表

        Args:
            pdf_path: PDF文件路径

        Returns:
            FinancialStatement: 解析后的财务报表数据
        """
        print(f"正在解析财务报表: {pdf_path}")

        with pdfplumber.open(pdf_path) as pdf:
            # 提取所有文本
            full_text = ""
            tables = []

            for page in pdf.pages:
                # 提取文本
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

                # 提取表格
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)

        # 解析基本信息
        company_name = self._extract_company_name(full_text)
        report_period = self._extract_report_period(full_text)
        report_type = self._determine_report_type(full_text, report_period)

        # 解析三大报表
        balance_sheet = self._parse_balance_sheet(full_text, tables)
        income_statement = self._parse_income_statement(full_text, tables)
        cashflow_statement = self._parse_cashflow_statement(full_text, tables)

        # 提取元数据
        metadata = self._extract_metadata(full_text)

        statement = FinancialStatement(
            company_name=company_name,
            report_period=report_period,
            report_type=report_type,
            balance_sheet=balance_sheet,
            income_statement=income_statement,
            cashflow_statement=cashflow_statement,
            metadata=metadata
        )

        self.current_statement = statement
        print(f"解析完成: {company_name} - {report_period} {report_type}")

        return statement

    def _extract_company_name(self, text: str) -> str:
        """提取公司名称"""
        # 匹配常见的公司名称模式
        patterns = [
            r'([\u4e00-\u9fa5]+(?:股份)?有限公司)',
            r'公司名称[：:]\s*([\u4e00-\u9fa5]+)',
            r'证券简称[：:]\s*([\u4e00-\u9fa5]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text[:2000])  # 只搜索前2000字符
            if match:
                return match.group(1).strip()

        return "未识别公司名称"

    def _extract_report_period(self, text: str) -> str:
        """提取报告期"""
        patterns = [
            r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
            r'报告期[：:]\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})',
            r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text[:2000])
            if match:
                year = match.group(1)
                month = match.group(2).zfill(2)
                day = match.group(3).zfill(2) if len(match.groups()) >= 3 else "31"
                return f"{year}-{month}-{day}"

        return datetime.now().strftime("%Y-%m-%d")

    def _determine_report_type(self, text: str, period: str) -> str:
        """判断报告类型"""
        if '年度报告' in text or '年报' in text:
            return '年报'
        elif '半年度报告' in text or '中报' in text or '半年报' in text:
            return '半年报'
        elif '季度报告' in text or '季报' in text:
            # 根据日期判断是第几季度
            month = period.split('-')[1]
            if month in ['03']:
                return '一季报'
            elif month in ['06']:
                return '二季报'  # 也可能是半年报
            elif month in ['09']:
                return '三季报'
            else:
                return '季报'

        # 根据日期推断
        month = period.split('-')[1]
        if month == '12':
            return '年报'
        elif month == '06':
            return '半年报'
        else:
            return '季报'

    def _parse_balance_sheet(self, text: str, tables: List) -> Dict[str, float]:
        """解析资产负债表"""
        balance_sheet = {}

        # 从表格中提取数据
        for table in tables:
            if not table:
                continue

            # 检查是否是资产负债表
            table_str = str(table).lower()
            if '资产负债' not in table_str and 'balance' not in table_str:
                continue

            # 解析表格数据
            for row in table:
                if not row or len(row) < 2:
                    continue

                item_name = str(row[0]).strip() if row[0] else ""

                # 匹配关键项目
                for cn_name, en_name in self.key_items.items():
                    if cn_name in item_name:
                        # 提取数值（通常在第二列或最后一列）
                        value = self._extract_number(row)
                        if value is not None:
                            balance_sheet[en_name] = value
                            break

        # 计算衍生指标
        if 'current_assets' in balance_sheet and 'current_liabilities' in balance_sheet:
            balance_sheet['working_capital'] = (
                balance_sheet['current_assets'] - balance_sheet['current_liabilities']
            )

        return balance_sheet

    def _parse_income_statement(self, text: str, tables: List) -> Dict[str, float]:
        """解析利润表"""
        income_statement = {}

        for table in tables:
            if not table:
                continue

            table_str = str(table).lower()
            if '利润' not in table_str and 'income' not in table_str:
                continue

            for row in table:
                if not row or len(row) < 2:
                    continue

                item_name = str(row[0]).strip() if row[0] else ""

                for cn_name, en_name in self.key_items.items():
                    if cn_name in item_name:
                        value = self._extract_number(row)
                        if value is not None:
                            income_statement[en_name] = value
                            break

        # 计算衍生指标
        if 'operating_revenue' in income_statement and 'operating_cost' in income_statement:
            income_statement['gross_profit'] = (
                income_statement['operating_revenue'] - income_statement['operating_cost']
            )

        return income_statement

    def _parse_cashflow_statement(self, text: str, tables: List) -> Dict[str, float]:
        """解析现金流量表"""
        cashflow_statement = {}

        for table in tables:
            if not table:
                continue

            table_str = str(table).lower()
            if '现金流' not in table_str and 'cash flow' not in table_str:
                continue

            for row in table:
                if not row or len(row) < 2:
                    continue

                item_name = str(row[0]).strip() if row[0] else ""

                for cn_name, en_name in self.key_items.items():
                    if cn_name in item_name:
                        value = self._extract_number(row)
                        if value is not None:
                            cashflow_statement[en_name] = value
                            break

        return cashflow_statement

    def _extract_number(self, row: List) -> Optional[float]:
        """从表格行中提取数值"""
        # 尝试从最后几列提取数字
        for cell in reversed(row[1:]):  # 跳过第一列（通常是项目名称）
            if cell is None:
                continue

            cell_str = str(cell).strip()

            # 移除常见的非数字字符
            cell_str = cell_str.replace(',', '').replace('，', '')
            cell_str = cell_str.replace(' ', '').replace('\n', '')

            # 匹配数字（包括负数和小数）
            match = re.search(r'-?\d+\.?\d*', cell_str)
            if match:
                try:
                    value = float(match.group())
                    # 如果数值太小，可能需要转换单位（很多财报以万元或元为单位）
                    return value
                except ValueError:
                    continue

        return None

    def _extract_metadata(self, text: str) -> Dict:
        """提取其他元数据"""
        metadata = {}

        # 提取股票代码
        code_match = re.search(r'股票代码[：:]\s*(\d{6})', text[:2000])
        if code_match:
            metadata['stock_code'] = code_match.group(1)

        # 提取审计意见
        if '标准无保留意见' in text:
            metadata['audit_opinion'] = '标准无保留意见'
        elif '保留意见' in text:
            metadata['audit_opinion'] = '保留意见'

        # 提取总股本
        shares_match = re.search(r'总股本[：:]\s*([\d,，.]+)', text)
        if shares_match:
            shares_str = shares_match.group(1).replace(',', '').replace('，', '')
            try:
                metadata['total_shares'] = float(shares_str)
            except ValueError:
                pass

        return metadata

    def export_to_dataframe(self) -> pd.DataFrame:
        """将解析结果导出为DataFrame"""
        if not self.current_statement:
            return pd.DataFrame()

        data = {
            '公司名称': [self.current_statement.company_name],
            '报告期': [self.current_statement.report_period],
            '报告类型': [self.current_statement.report_type],
        }

        # 添加所有财务数据
        for key, value in self.current_statement.balance_sheet.items():
            data[f'资产负债表_{key}'] = [value]

        for key, value in self.current_statement.income_statement.items():
            data[f'利润表_{key}'] = [value]

        for key, value in self.current_statement.cashflow_statement.items():
            data[f'现金流量表_{key}'] = [value]

        return pd.DataFrame(data)
