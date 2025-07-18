#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理Markdown文件脚本
删除指定文件夹中所有.md文件标题行之前的内容
标题格式：## 第X章 **章节名**
"""

import os
import re
import sys
from pathlib import Path


def clean_markdown_file(file_path):
    """
    清理单个markdown文件，删除标题行之前的所有内容
    
    Args:
        file_path (str): 文件路径
    
    Returns:
        bool: 是否成功处理
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 查找标题行（格式：## 第X章 **章节名**）
        title_pattern = r'^##\s+第.+章\s+\*\*.+\*\*\s*$'
        title_line_index = -1
        
        for i, line in enumerate(lines):
            if re.match(title_pattern, line.strip()):
                title_line_index = i
                break
        
        # 如果找到标题行，删除之前的所有内容
        if title_line_index >= 0:
            # 保留从标题行开始的所有内容
            cleaned_lines = lines[title_line_index:]
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)
            
            print(f"✓ 已处理: {file_path}")
            print(f"  删除了前 {title_line_index} 行内容")
            return True
        else:
            print(f"⚠ 未找到标题行: {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ 处理失败: {file_path}")
        print(f"  错误: {str(e)}")
        return False


def clean_folder(folder_path):
    """
    清理指定文件夹中的所有markdown文件
    
    Args:
        folder_path (str): 文件夹路径
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"错误: 文件夹不存在 - {folder_path}")
        return
    
    if not folder.is_dir():
        print(f"错误: 路径不是文件夹 - {folder_path}")
        return
    
    # 查找所有.md文件
    md_files = list(folder.glob("*.md"))
    
    if not md_files:
        print(f"未找到任何.md文件在文件夹: {folder_path}")
        return
    
    print(f"找到 {len(md_files)} 个.md文件")
    print("-" * 50)
    
    success_count = 0
    for md_file in md_files:
        if clean_markdown_file(str(md_file)):
            success_count += 1
    
    print("-" * 50)
    print(f"处理完成: {success_count}/{len(md_files)} 个文件成功处理")


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python clean_md_files.py <文件夹路径>")
        print("示例: python clean_md_files.py my-website\\docs\\庆余年\\第二卷")
        return
    
    folder_path = sys.argv[1]
    print(f"开始处理文件夹: {folder_path}")
    clean_folder(folder_path)


if __name__ == "__main__":
    main()
