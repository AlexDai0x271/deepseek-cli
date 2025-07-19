#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek CLI Chat Tool
一个与DeepSeek大语言模型交互的命令行工具

安装为全局命令:
1. chmod +x deepseek_cli.py
2. sudo ln -sf $(pwd)/deepseek_cli.py /usr/local/bin/deepseek
3. deepseek --api-key YOUR_KEY

或者使用 pip 安装:
1. 创建 setup.py 文件
2. pip install -e .
3. deepseek
"""

import os
import json
import argparse
import requests
import sys
from datetime import datetime
from typing import List, Dict, Optional
import readline  # 启用命令行历史和编辑功能

# 版本信息
__version__ = "0.0.1"
__author__ = "AlexDai"
__email__ = "alexdai0625@outlook.com"
__description__ = "DeepSeek大语言模型命令行聊天工具"

class DeepSeekCLI:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1", model: str = "deepseek-chat"):
        """初始化DeepSeek CLI客户端
        
        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL
            model: 使用的模型名称
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.conversation_history: List[Dict] = []
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        
        # 配置参数
        self.max_tokens = 2000
        self.temperature = 0.7
        self.stream = True
        
        # 历史记录文件
        self.history_file = os.path.expanduser("~/.deepseek_history.json")
        self.load_history()

    def load_history(self):
        """加载对话历史"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('history', [])
                    print(f"✓ 已加载 {len(self.conversation_history)} 条历史消息")
        except Exception as e:
            print(f"⚠ 加载历史记录失败: {e}")
            self.conversation_history = []

    def save_history(self):
        """保存对话历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'history': self.conversation_history,
                    'last_updated': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠ 保存历史记录失败: {e}")

    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            print("✓ 对话历史已清空")
        except Exception as e:
            print(f"⚠ 清空历史记录失败: {e}")

    def chat_completion(self, message: str, stream: bool = True) -> str:
        """发送聊天完成请求
        
        Args:
            message: 用户消息
            stream: 是否使用流式响应
            
        Returns:
            模型回复内容
        """
        # 添加用户消息到历史
        self.conversation_history.append({"role": "user", "content": message})
        
        # 准备请求数据
        data = {
            "model": self.model,
            "messages": self.conversation_history,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": stream
        }
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            if stream:
                return self._stream_response(url, data)
            else:
                return self._non_stream_response(url, data)
                
        except Exception as e:
            error_msg = f"请求失败: {e}"
            print(f"\n❌ {error_msg}")
            return error_msg

    def _stream_response(self, url: str, data: dict) -> str:
        """处理流式响应"""
        response = self.session.post(url, json=data, stream=True)
        response.raise_for_status()
        
        full_response = ""
        print("\n🤖 DeepSeek: ", end="", flush=True)
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str.strip() == '[DONE]':
                        break
                    
                    try:
                        data_obj = json.loads(data_str)
                        if 'choices' in data_obj and len(data_obj['choices']) > 0:
                            delta = data_obj['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                print(content, end="", flush=True)
                                full_response += content
                    except json.JSONDecodeError:
                        continue
        
        print()  # 换行
        
        # 添加助手回复到历史
        if full_response:
            self.conversation_history.append({"role": "assistant", "content": full_response})
        
        return full_response

    def _non_stream_response(self, url: str, data: dict) -> str:
        """处理非流式响应"""
        response = self.session.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print(f"\n🤖 DeepSeek: {content}")
        
        # 添加助手回复到历史
        self.conversation_history.append({"role": "assistant", "content": content})
        
        return content

    def show_help(self):
        """显示帮助信息"""
        help_text = """
📖 DeepSeek CLI 使用帮助

命令:
  /help     - 显示此帮助信息
  /clear    - 清空对话历史
  /history  - 显示对话历史
  /config   - 显示当前配置
  /set      - 设置配置参数
  /version  - 显示版本信息
  /exit     - 退出程序

设置参数:
  /set temperature 0.8    - 设置温度参数 (0.0-2.0)
  /set max_tokens 1000    - 设置最大token数
  /set stream true        - 设置是否流式输出
  /set model model_name   - 设置模型名称

快捷键:
  Ctrl+C    - 中断当前输入
  Ctrl+D    - 退出程序
  ↑/↓       - 浏览输入历史

示例:
  你好，请介绍一下你自己
  /set temperature 0.9
  /clear
        """
        print(help_text)

    def show_history(self):
        """显示对话历史"""
        if not self.conversation_history:
            print("📝 暂无对话历史")
            return
        
        print(f"\n📝 对话历史 (共 {len(self.conversation_history)} 条):")
        print("=" * 60)
        
        for i, msg in enumerate(self.conversation_history, 1):
            role = "👤 用户" if msg['role'] == 'user' else "🤖 DeepSeek"
            content = msg['content']
            # 限制显示长度
            if len(content) > 100:
                content = content[:100] + "..."
            print(f"{i:2d}. {role}: {content}")
        
        print("=" * 60)

    def show_config(self):
        """显示当前配置"""
        config_text = f"""
⚙️  当前配置:
  模型: {self.model}
  温度: {self.temperature}
  最大tokens: {self.max_tokens}
  流式输出: {self.stream}
  API端点: {self.base_url}
  历史记录: {len(self.conversation_history)} 条
        """
        print(config_text)

    def show_version(self):
        """显示版本信息"""
        version_text = f"""
🚀 DeepSeek CLI v{__version__}

📋 详细信息:
  版本: {__version__}
  作者: {__author__}
  邮箱: {__email__}
  描述: {__description__}
  
🔗 项目链接:
  GitHub: https://github.com/AlexDai0x271/deepseek-cli
  Issues: https://github.com/AlexDai0x271/deepseek-cli/issues
        """
        print(version_text)

    def set_config(self, param: str, value: str):
        """设置配置参数"""
        try:
            if param == 'temperature':
                val = float(value)
                if 0.0 <= val <= 2.0:
                    self.temperature = val
                    print(f"✓ 温度已设置为: {val}")
                else:
                    print("❌ 温度值应在 0.0-2.0 之间")
            
            elif param == 'max_tokens':
                val = int(value)
                if val > 0:
                    self.max_tokens = val
                    print(f"✓ 最大tokens已设置为: {val}")
                else:
                    print("❌ 最大tokens应大于0")
            
            elif param == 'stream':
                val = value.lower() in ['true', '1', 'yes', 'on']
                self.stream = val
                print(f"✓ 流式输出已设置为: {val}")
            
            elif param == 'model':
                self.model = value
                print(f"✓ 模型已设置为: {value}")
            
            else:
                print(f"❌ 未知参数: {param}")
                
        except ValueError as e:
            print(f"❌ 参数值无效: {e}")

    def run(self):
        """运行主循环"""
        print("🚀 DeepSeek CLI 聊天工具")
        print("输入 /help 查看帮助，输入 /exit 退出程序")
        print("-" * 50)
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n👤 你: ").strip()
                
                if not user_input:
                    continue
                
                # 处理命令
                if user_input.startswith('/'):
                    cmd_parts = user_input[1:].split()
                    cmd = cmd_parts[0].lower()
                    
                    if cmd == 'help':
                        self.show_help()
                    elif cmd == 'exit':
                        print("👋 再见!")
                        break
                    elif cmd == 'clear':
                        self.clear_history()
                    elif cmd == 'history':
                        self.show_history()
                    elif cmd == 'config':
                        self.show_config()
                    elif cmd == 'version':
                        self.show_version()
                    elif cmd == 'set' and len(cmd_parts) >= 3:
                        self.set_config(cmd_parts[1], cmd_parts[2])
                    elif cmd == 'set':
                        print("❌ 用法: /set <参数> <值>")
                    else:
                        print(f"❌ 未知命令: {cmd}")
                    continue
                
                # 发送消息给模型
                self.chat_completion(user_input, self.stream)
                
                # 自动保存历史
                self.save_history()
                
            except KeyboardInterrupt:
                print("\n\n👋 程序被用户中断")
                break
            except EOFError:
                print("\n\n👋 再见!")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")


def show_version():
    """显示版本信息 (用于命令行参数)"""
    print(f"DeepSeek CLI v{__version__}")
    print(f"作者: {__author__}")
    print(f"邮箱: {__email__}")
    print(f"描述: {__description__}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="DeepSeek CLI 聊天工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  %(prog)s --api-key YOUR_API_KEY
  %(prog)s --api-key YOUR_API_KEY --model deepseek-coder
  %(prog)s --version
  
环境变量:
  DEEPSEEK_API_KEY    DeepSeek API 密钥
  
更多信息请访问: https://github.com/AlexDai0x271/deepseek-cli
        """
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--api-key", help="DeepSeek API密钥")
    parser.add_argument("--model", default="deepseek-chat", help="模型名称")
    parser.add_argument("--base-url", default="https://api.deepseek.com/v1", help="API基础URL")
    parser.add_argument("--temperature", type=float, default=0.7, help="温度参数")
    parser.add_argument("--max-tokens", type=int, default=2000, help="最大token数")
    parser.add_argument("--no-stream", action="store_true", help="禁用流式输出")
    
    args = parser.parse_args()
    
    # 获取API密钥
    api_key = args.api_key or os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        print("❌ 请提供DeepSeek API密钥:")
        print("   方法1: --api-key YOUR_API_KEY")
        print("   方法2: 设置环境变量 DEEPSEEK_API_KEY")
        print("   方法3: deepseek --help 查看更多帮助")
        sys.exit(1)
    
    try:
        # 创建客户端
        client = DeepSeekCLI(
            api_key=api_key,
            base_url=args.base_url,
            model=args.model
        )
        
        # 设置初始参数
        client.temperature = args.temperature
        client.max_tokens = args.max_tokens
        client.stream = not args.no_stream
        
        # 运行
        client.run()
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()