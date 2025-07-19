#!/bin/bash
# DeepSeek CLI 一键安装脚本

set -e

echo "🚀 DeepSeek CLI 安装脚本"
echo "=========================="

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✓ 检测到 Python 版本: $python_version"

# 检查是否有 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip3，请先安装 pip"
    exit 1
fi

echo "✓ 检测到 pip3"

# 安装依赖
echo "📦 安装依赖包..."
pip3 install requests

# 获取当前目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DEEPSEEK_SCRIPT="$SCRIPT_DIR/deepseek_cli.py"

# 检查脚本文件是否存在
if [ ! -f "$DEEPSEEK_SCRIPT" ]; then
    echo "❌ 未找到 deepseek_cli.py 文件"
    exit 1
fi

# 方法1: 使用 pip 安装 (推荐)
echo "🔧 安装 DeepSeek CLI..."
if [ -f "$SCRIPT_DIR/setup.py" ]; then
    echo "使用 pip 安装..."
    pip3 install -e "$SCRIPT_DIR"
    echo "✅ 安装完成！可以使用 'deepseek' 命令启动"
else
    # 方法2: 创建符号链接
    echo "创建命令链接..."
    
    # 让脚本可执行
    chmod +x "$DEEPSEEK_SCRIPT"
    
    # 检查 /usr/local/bin 是否存在
    if [ -d "/usr/local/bin" ]; then
        INSTALL_DIR="/usr/local/bin"
    else
        INSTALL_DIR="$HOME/.local/bin"
        mkdir -p "$INSTALL_DIR"
        echo "⚠️  将安装到 $INSTALL_DIR，请确保此目录在你的 PATH 中"
    fi
    
    # 创建符号链接
    if [ -w "$INSTALL_DIR" ]; then
        ln -sf "$DEEPSEEK_SCRIPT" "$INSTALL_DIR/deepseek"
        echo "✅ 安装完成！可以使用 'deepseek' 命令启动"
    else
        echo "需要管理员权限安装到 $INSTALL_DIR"
        sudo ln -sf "$DEEPSEEK_SCRIPT" "$INSTALL_DIR/deepseek"
        echo "✅ 安装完成！可以使用 'deepseek' 命令启动"
    fi
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "使用方法:"
echo "  deepseek --api-key YOUR_API_KEY"
echo "  或者设置环境变量: export DEEPSEEK_API_KEY='your_key'"
echo "  然后直接运行: deepseek"
echo ""
echo "查看帮助: deepseek --help"
echo "祝你使用愉快！"