# DeepSeek CLI

🚀 一个功能丰富的DeepSeek大语言模型命令行聊天工具

## 功能特性

✨ **核心功能**
- 🔥 实时流式对话响应
- 💾 自动保存对话历史
- ⚙️ 动态配置参数调整
- 🎯 丰富的交互命令
- 🎨 友好的用户界面
- 📝 命令行历史记录支持

✨ **技术特性**
- 支持自定义模型和API端点
- 可配置的温度和token限制
- 流式/非流式输出模式切换
- 持久化对话历史存储
- 完整的错误处理机制

## 系统要求

- Python 3.7 或更高版本
- pip3 包管理器
- DeepSeek API 密钥

## 快速安装

### 方法一：一键安装脚本（推荐）

```bash
# 下载项目
git clone https://github.com/AlexDai0x271/deepseek-cli.git
cd deepseek-cli

# 运行一键安装脚本
chmod +x install.sh
./install.sh
```

### 方法二：使用 pip 安装

```bash
# 克隆项目
git clone https://github.com/AlexDai0x271/deepseek-cli.git
cd deepseek-cli

# 安装依赖
pip3 install requests

# 使用 pip 安装
pip3 install -e .
```

### 方法三：手动安装

```bash
# 下载脚本
wget https://raw.githubusercontent.com/AlexDai0x271/deepseek-cli/main/deepseek_cli.py

# 安装依赖
pip3 install requests

# 设置可执行权限
chmod +x deepseek_cli.py

# 创建软链接（可选）
sudo ln -sf $(pwd)/deepseek_cli.py /usr/local/bin/deepseek
```

## 快速检查版本

安装完成后，可以快速检查版本：

```bash
# 检查版本信息
deepseek --version

# 输出示例:
# DeepSeek CLI v1.0.0
# 作者: AlexDai
# 邮箱: your.email@example.com
# 描述: DeepSeek大语言模型命令行聊天工具
```

## 获取 API 密钥

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册账号并登录
3. 进入 API 管理页面
4. 创建新的 API 密钥
5. 复制生成的密钥

## 配置和使用

### 基础使用

**方法一：命令行参数**
```bash
deepseek --api-key YOUR_API_KEY
```

**方法二：环境变量**
```bash
# 设置环境变量
export DEEPSEEK_API_KEY="your_api_key_here"

# 直接运行
deepseek
```

**方法三：添加到 shell 配置文件**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export DEEPSEEK_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 高级配置

```bash
deepseek --api-key YOUR_KEY \
         --model deepseek-chat \
         --temperature 0.8 \
         --max-tokens 1500 \
         --base-url https://api.deepseek.com/v1
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--version` | 显示版本信息并退出 | - |
| `--api-key` | DeepSeek API 密钥 | 环境变量 |
| `--model` | 使用的模型名称 | `deepseek-chat` |
| `--base-url` | API 基础 URL | `https://api.deepseek.com/v1` |
| `--temperature` | 温度参数 (0.0-2.0) | `0.7` |
| `--max-tokens` | 最大 token 数 | `2000` |
| `--no-stream` | 禁用流式输出 | `false` |

## 交互命令

启动程序后，您可以使用以下命令：

### 基础命令

| 命令 | 功能 |
|------|------|
| `/help` | 显示帮助信息 |
| `/exit` | 退出程序 |
| `/clear` | 清空对话历史 |
| `/history` | 查看对话历史 |
| `/config` | 显示当前配置 |
| `/version` | 显示版本信息 |

### 配置命令

| 命令 | 示例 | 说明 |
|------|------|------|
| `/set temperature` | `/set temperature 0.9` | 设置温度参数 |
| `/set max_tokens` | `/set max_tokens 1000` | 设置最大 token 数 |
| `/set stream` | `/set stream false` | 设置流式输出 |
| `/set model` | `/set model deepseek-coder` | 设置模型名称 |

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `↑/↓` | 浏览输入历史 |
| `Ctrl+C` | 中断当前输入 |
| `Ctrl+D` | 退出程序 |

## 使用示例

### 基础对话
```
👤 你: 你好，请介绍一下你自己

🤖 DeepSeek: 你好！我是DeepSeek，一个由深度求索开发的人工智能助手...
```

### 配置调整
```
👤 你: /set temperature 0.9
✓ 温度已设置为: 0.9

👤 你: /config
⚙️  当前配置:
  模型: deepseek-chat
  温度: 0.9
  最大tokens: 2000
  流式输出: True
```

### 版本查看
```
👤 你: /version
🚀 DeepSeek CLI v1.0.0

📋 详细信息:
  版本: 1.0.0
  作者: AlexDai
  邮箱: your.email@example.com
  描述: DeepSeek大语言模型命令行聊天工具
  
🔗 项目链接:
  GitHub: https://github.com/AlexDai0x271/deepseek-cli
  Issues: https://github.com/AlexDai0x271/deepseek-cli/issues
```

### 查看历史
```
👤 你: /history
📝 对话历史 (共 4 条):
====================================
 1. 👤 用户: 你好，请介绍一下你自己
 2. 🤖 DeepSeek: 你好！我是DeepSeek...
```

## 文件说明

```
deepseek-cli/
├── deepseek_cli.py    # 主程序文件
├── install.sh         # 一键安装脚本
├── setup.py          # pip 安装配置
└── README.md         # 说明文档
```

### 数据存储

- 对话历史保存在：`~/.deepseek_history.json`
- 包含完整的对话记录和时间戳
- 支持跨会话历史记录保持

## 故障排除

### 常见问题

**1. 权限错误**
```bash
# 如果遇到权限问题，使用用户目录安装
pip3 install --user -e .
```

**2. 找不到命令**
```bash
# 检查 PATH 环境变量
echo $PATH

# 添加用户 bin 目录到 PATH
export PATH=$PATH:~/.local/bin
```

**3. API 连接失败**
```bash
# 检查网络连接
curl -I https://api.deepseek.com/v1

# 验证 API 密钥
deepseek --api-key YOUR_KEY /config
```

**4. Python 版本问题**
```bash
# 检查 Python 版本
python3 --version

# 如果版本过低，升级 Python
sudo apt update && sudo apt install python3.9
```

### 依赖问题

如果遇到依赖安装问题：

```bash
# 升级 pip
pip3 install --upgrade pip

# 安装必要依赖
pip3 install requests

# 清除缓存重新安装
pip3 cache purge
pip3 install requests --force-reinstall
```

## 卸载

### 使用 pip 安装的卸载方法
```bash
pip3 uninstall deepseek-cli
```

### 手动安装的卸载方法
```bash
# 删除命令链接
sudo rm /usr/local/bin/deepseek

# 删除历史文件
rm ~/.deepseek_history.json

# 删除项目目录
rm -rf deepseek-cli/
```

## 更新日志

### v0.0.1
- ✨ 初始发布版本
- 🔥 支持流式对话
- 💾 对话历史记录
- ⚙️ 动态参数配置
- 🎨 友好用户界面

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 开源协议

本项目基于 MIT 协议开源 - 详见 [LICENSE](./LICENSE) 文件

## 联系方式

- 项目主页: https://github.com/AlexDai0x271/deepseek-cli
- 问题反馈: https://github.com/AlexDai0x271/deepseek-cli/issues
- 邮箱联系: your.email@example.com

---

⭐ 如果这个项目对您有帮助，请给它一个 star！
