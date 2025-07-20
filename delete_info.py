#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
python delete_info.py my-website/docs/南明史
删除markdown文件中的:::info 笔记结构
删除功能：
1. 删除 :::info 笔记 ... ::: 整个结构
2. 删除该结构，并保持格式美观
"""

import os
import argparse
from pathlib import Path


def delete_info_blocks(file_path):
    """删除单个markdown文件中的:::info 笔记结构"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        cleaned_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 检测:::info 笔记的开始
            if line.startswith(':::info') and '笔记' in line:
                # 删除该行前面的空行
                while cleaned_lines and cleaned_lines[-1].strip() == '':
                    cleaned_lines.pop()
                
                # 跳过:::info块内容，直到找到结束的:::
                i += 1
                while i < len(lines):
                    if lines[i].strip() == ':::':
                        i += 1  # 跳过结束的:::行
                        break
                    i += 1
                
                continue
            
            # 保留其他内容
            cleaned_lines.append(lines[i])
            i += 1
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        
        print(f"✓ 已处理文件: {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ 处理文件失败 {file_path}: {e}")
        return False


def process_directory(directory_path):
    """处理目录中的所有markdown文件"""
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
        if delete_info_blocks(md_file):
            success_count += 1
    
    print(f"\n处理完成: {success_count}/{len(md_files)} 个文件成功处理")


def main():
    parser = argparse.ArgumentParser(description='删除markdown文件中的:::info 笔记结构')
    parser.add_argument('path', help='要处理的文件或目录路径')
    parser.add_argument('--backup', '-b', action='store_true', help='处理前创建备份')
    
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
            delete_info_blocks(path)
        else:
            print(f"错误: 不是markdown文件 - {args.path}")
    else:
        process_directory(path)


if __name__ == '__main__':
    main()
