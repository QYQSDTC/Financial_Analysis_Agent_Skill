"""
财务报表分析系统
专业的上市公司财务分析工具，支持PDF格式的季报、半年报、年报智能解析与分析
"""

from .parsers.pdf_parser import FinancialReportParser
from .analyzers.financial_analyzer import FinancialAnalyzer
from .indicators.calculator import FinancialIndicatorCalculator
from .reports.report_generator import AnalysisReportGenerator

__version__ = "1.0.0"
__all__ = [
    "FinancialReportParser",
    "FinancialAnalyzer",
    "FinancialIndicatorCalculator",
    "AnalysisReportGenerator"
]
