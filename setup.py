#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="deepseek-cli",
    version="1.0.0",
    description="DeepSeek大语言模型命令行聊天工具",
    long_description="""
一个功能丰富的DeepSeek CLI聊天工具，支持：
- 流式对话响应
- 对话历史记录
- 参数动态配置
- 多种交互命令
- 友好的用户界面
    """.strip(),
    long_description_content_type="text/plain",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/Alexdai0x271/deepseek-cli",
    py_modules=["deepseek_cli"],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "deepseek=deepseek_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="deepseek ai chatbot cli command-line llm",
    project_urls={
        "Bug Reports": "https://github.com/AlexDai0x271/deepseek-cli/issues",
        "Source": "https://github.com/AlexDai0x271/deepseek-cli",
    },
)