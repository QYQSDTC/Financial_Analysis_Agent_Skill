#!/bin/bash
# 财务分析工具安装脚本

echo "======================================"
echo "财务报表分析助手 - 安装脚本"
echo "======================================"

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "📦 安装目录: $SCRIPT_DIR"

# 1. 检查 Python
echo ""
echo "[1/3] 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ 找到 $PYTHON_VERSION"
else
    echo "✗ 未找到 Python 3"
    echo "请先安装 Python 3.9 或更高版本"
    exit 1
fi

# 2. 安装依赖
echo ""
echo "[2/3] 安装 Python 依赖包..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

if [ $? -eq 0 ]; then
    echo "✓ 依赖安装完成"
else
    echo "✗ 依赖安装失败"
    exit 1
fi

# 3. 设置权限
echo ""
echo "[3/3] 设置执行权限..."
chmod +x "$SCRIPT_DIR/analyze-report"
chmod +x "$SCRIPT_DIR/example.py"
echo "✓ 权限设置完成"

# 4. 提示添加到 PATH
echo ""
echo "======================================"
echo "✅ 安装完成！"
echo "======================================"
echo ""
echo "📋 使用方式："
echo ""
echo "1. 在当前目录使用："
echo "   cd $SCRIPT_DIR"
echo "   ./analyze-report 财报.pdf"
echo ""
echo "2. 添加到 PATH 后全局使用："
echo "   echo 'export PATH=\"$SCRIPT_DIR:\$PATH\"' >> ~/.zshrc"
echo "   source ~/.zshrc"
echo "   analyze-report 财报.pdf"
echo ""
echo "3. 在 Claude Code 对话中直接使用："
echo "   \"帮我分析这个财报PDF\""
echo ""
echo "4. 在 Python 代码中使用："
echo "   from financial_analyzer import FinancialReportParser"
echo ""
echo "📚 详细文档: $SCRIPT_DIR/README.md"
echo "📖 使用指南: $SCRIPT_DIR/USAGE.md"
echo ""
echo "🔑 可选：设置 API 密钥启用 AI 深度分析"
echo "   export ANTHROPIC_API_KEY='your_key_here'"
echo ""
