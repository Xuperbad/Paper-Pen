#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py clean_nanming_history.py my-website\docs\南明史
南明史章节文献引用清理脚本
清理功能：
1. 删除开头的sidebar配置
2. 删除所有文献引用部分（包括分隔符）
3. 保留正文内容和标题结构
"""

import os
import re
import argparse
from pathlib import Path


def clean_markdown_file(file_path):
    """清理单个markdown文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        cleaned_lines = []
        skip_mode = False
        sidebar_section = True

        for i, line in enumerate(lines):
            # 跳过开头的sidebar配置部分
            if sidebar_section:
                if line.startswith('---') and i == 0:
                    continue
                elif line.startswith('sidebar_position:'):
                    continue
                elif line.startswith('---') and i > 0:
                    sidebar_section = False
                    continue
                elif line.strip() == '' and i < 5:
                    continue

            # 检测分隔符，开始跳过模式（文献引用部分）
            if line.strip() == '---' and not sidebar_section:
                skip_mode = True
                continue

            # 如果在跳过模式中，检查是否遇到下一个章节标题
            if skip_mode:
                # 如果遇到章节标题（## 开头），结束跳过模式
                if line.startswith('## '):
                    skip_mode = False
                    cleaned_lines.append(line)
                continue

            # 跳过各种格式的文献引用行
            line_stripped = line.strip()
            if (re.match(r'^\d+\.\s*\[.*\]\(#.*\)', line_stripped) or  # 标准引用格式
                re.match(r'^\d+\.\s*\[.*\].*​​​​​​​​​$', line_stripped) or  # 带特殊字符的引用
                re.match(r'^\d+\.\s*\[.*\]\(.*\)\s*​+', line_stripped)):  # 其他引用格式
                continue

            # 保留其他内容
            cleaned_lines.append(line)

        # 移除文件末尾的空行
        while cleaned_lines and cleaned_lines[-1].strip() == '':
            cleaned_lines.pop()

        # 确保文件以换行符结尾
        if cleaned_lines and not cleaned_lines[-1].endswith('\n'):
            cleaned_lines.append('')

        # 写回文件
        cleaned_content = '\n'.join(cleaned_lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"✓ 已清理文件: {file_path}")
        return True

    except Exception as e:
        print(f"✗ 清理文件失败 {file_path}: {e}")
        return False


def clean_directory(directory_path):
    """清理目录中的所有markdown文件"""
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"错误: 目录不存在 - {directory_path}")
        return
    
    if not directory.is_dir():
        print(f"错误: 路径不是目录 - {directory_path}")
        return
    
    # 查找所有markdown文件
    md_files = list(directory.glob('*.md'))
    
    if not md_files:
        print(f"在目录 {directory_path} 中未找到markdown文件")
        return
    
    print(f"找到 {len(md_files)} 个markdown文件")
    
    success_count = 0
    for md_file in md_files:
        if clean_markdown_file(md_file):
            success_count += 1
    
    print(f"\n清理完成: {success_count}/{len(md_files)} 个文件成功处理")


def main():
    parser = argparse.ArgumentParser(description='清理南明史章节的文献引用')
    parser.add_argument('path', help='要清理的文件或目录路径')
    parser.add_argument('--backup', '-b', action='store_true', help='清理前创建备份')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if not path.exists():
        print(f"错误: 路径不存在 - {args.path}")
        return
    
    # 创建备份
    if args.backup:
        import shutil
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if path.is_file():
            backup_path = path.with_suffix(f'.backup_{timestamp}{path.suffix}')
            shutil.copy2(path, backup_path)
            print(f"已创建备份: {backup_path}")
        else:
            backup_dir = path.parent / f"{path.name}_backup_{timestamp}"
            shutil.copytree(path, backup_dir)
            print(f"已创建备份目录: {backup_dir}")
    
    # 处理文件或目录
    if path.is_file():
        if path.suffix.lower() == '.md':
            clean_markdown_file(path)
        else:
            print(f"错误: 不是markdown文件 - {args.path}")
    else:
        clean_directory(path)


if __name__ == '__main__':
    main()
