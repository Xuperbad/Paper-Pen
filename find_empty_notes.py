#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找包含空的 :::info 笔记 结构的 Markdown 文件
"""

import os
import re
import sys

def find_empty_note_blocks(file_path):
    """
    检查文件是否包含空的 :::info 笔记 块
    返回 True 如果找到空的笔记块
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式匹配 :::info 笔记 到 ::: 之间的内容
        # 允许笔记后面有空格，中间只有空白字符（空格、制表符、换行符）
        pattern = r':::info\s+笔记\s*\n([\s]*)\n\s*:::'
        
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        # 如果找到匹配项，检查是否为空（只包含空白字符）
        for match in matches:
            if not match.strip():  # 如果匹配的内容去除空白后为空
                return True
                
        return False
        
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return False

def scan_directory(directory):
    """
    扫描目录下所有 .md 文件，查找包含空笔记块的文件
    """
    empty_note_files = []
    
    # 递归查找所有 .md 文件
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if find_empty_note_blocks(file_path):
                    empty_note_files.append(file_path)
    
    return empty_note_files

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python find_empty_notes.py <目标目录路径>")
        print("示例: python find_empty_notes.py ./docs")
        sys.exit(1)

    scan_dir = sys.argv[1]

    # 检查目录是否存在
    if not os.path.exists(scan_dir):
        print(f"错误: 目录 '{scan_dir}' 不存在")
        sys.exit(1)

    if not os.path.isdir(scan_dir):
        print(f"错误: '{scan_dir}' 不是一个目录")
        sys.exit(1)

    print("正在扫描目录:", os.path.abspath(scan_dir))
    print("查找包含空的 :::info 笔记 结构的文件...")
    print("-" * 50)

    empty_files = scan_directory(scan_dir)

    if empty_files:
        print(f"找到 {len(empty_files)} 个包含空笔记块的文件:")
        print()
        for file_path in empty_files:
            print(file_path)
    else:
        print("没有找到包含空笔记块的文件。")

if __name__ == "__main__":
    main()
