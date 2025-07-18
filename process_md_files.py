#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
python process_md_files.py "./my-website/docs/庆余年/第一卷"
Markdown文档处理脚本
功能：为指定文件夹内的所有md文档添加sidebar_position配置
"""

import os
import re
import sys
from pathlib import Path


def chinese_to_arabic(chinese_num):
    """
    将中文数字转换为阿拉伯数字

    Args:
        chinese_num: 中文数字字符串

    Returns:
        int: 对应的阿拉伯数字
    """
    chinese_digits = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5,
        '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10
    }

    # 处理简单的一位数
    if len(chinese_num) == 1 and chinese_num in chinese_digits:
        return chinese_digits[chinese_num]

    # 处理十位数：十、一十、二十等
    if '十' in chinese_num or '拾' in chinese_num:
        if chinese_num == '十' or chinese_num == '拾':
            return 10
        elif chinese_num.startswith('十') or chinese_num.startswith('拾'):
            # 十一、十二等
            return 10 + chinese_digits.get(chinese_num[1], 0)
        elif chinese_num.endswith('十') or chinese_num.endswith('拾'):
            # 二十、三十等
            return chinese_digits.get(chinese_num[0], 0) * 10
        else:
            # 二十一、三十五等
            parts = chinese_num.replace('拾', '十').split('十')
            if len(parts) == 2:
                tens = chinese_digits.get(parts[0], 0) * 10
                ones = chinese_digits.get(parts[1], 0)
                return tens + ones

    return None


def extract_chapter_number(filename, content):
    """
    从文件名或内容中提取章节号

    Args:
        filename: 文件名
        content: 文件内容

    Returns:
        int: 章节号，如果无法提取则返回None
    """
    # 尝试从文件名中提取章节号
    # 匹配模式：第X章、第X节、ChapterX等（支持中文数字和阿拉伯数字）

    # 阿拉伯数字模式
    arabic_patterns = [
        r'第(\d+)章',
        r'第(\d+)节',
        r'chapter(\d+)',
        r'Chapter(\d+)',
        r'(\d+)章',
        r'(\d+)节'
    ]

    # 中文数字模式
    chinese_patterns = [
        r'第([零一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾〇]+)章',
        r'第([零一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾〇]+)节'
    ]

    # 先尝试阿拉伯数字模式
    for pattern in arabic_patterns:
        # 从文件名中查找
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            return int(match.group(1))

        # 从内容的前几行中查找
        lines = content.split('\n')[:10]  # 只检查前10行
        for line in lines:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return int(match.group(1))

    # 再尝试中文数字模式
    for pattern in chinese_patterns:
        # 从文件名中查找
        match = re.search(pattern, filename)
        if match:
            chinese_num = match.group(1)
            arabic_num = chinese_to_arabic(chinese_num)
            if arabic_num is not None:
                return arabic_num

        # 从内容的前几行中查找
        lines = content.split('\n')[:10]  # 只检查前10行
        for line in lines:
            match = re.search(pattern, line)
            if match:
                chinese_num = match.group(1)
                arabic_num = chinese_to_arabic(chinese_num)
                if arabic_num is not None:
                    return arabic_num

    return None


def has_sidebar_position(content):
    """
    检查文档是否已经包含sidebar_position配置
    
    Args:
        content: 文件内容
    
    Returns:
        bool: 如果已包含则返回True
    """
    lines = content.split('\n')
    
    # 检查前5行是否包含sidebar_position
    for i, line in enumerate(lines[:5]):
        if 'sidebar_position' in line:
            return True
        # 如果遇到非空行且不是---，说明不是frontmatter格式
        if line.strip() and not line.strip().startswith('---'):
            break
    
    return False


def add_sidebar_position(content, position):
    """
    在文档开头添加sidebar_position配置
    
    Args:
        content: 原文件内容
        position: 章节位置号
    
    Returns:
        str: 处理后的内容
    """
    frontmatter = f"""---
sidebar_position: {position}
---

"""
    
    # 如果文档已经有frontmatter，需要合并
    lines = content.split('\n')
    if lines and lines[0].strip() == '---':
        # 查找frontmatter结束位置
        end_index = -1
        for i in range(1, min(len(lines), 20)):  # 最多检查前20行
            if lines[i].strip() == '---':
                end_index = i
                break
        
        if end_index > 0:
            # 已有frontmatter，在其中添加sidebar_position
            existing_frontmatter = lines[1:end_index]
            has_sidebar = any('sidebar_position' in line for line in existing_frontmatter)
            
            if not has_sidebar:
                existing_frontmatter.insert(0, f'sidebar_position: {position}')
                new_content = '---\n' + '\n'.join(existing_frontmatter) + '\n---\n' + '\n'.join(lines[end_index+1:])
                return new_content
            else:
                return content  # 已有sidebar_position，不修改
    
    # 没有frontmatter，直接添加
    return frontmatter + content


def process_md_files(folder_path):
    """
    处理指定文件夹中的所有md文件
    
    Args:
        folder_path: 目标文件夹路径
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"错误：文件夹 '{folder_path}' 不存在")
        return
    
    if not folder.is_dir():
        print(f"错误：'{folder_path}' 不是一个文件夹")
        return
    
    # 查找所有md文件
    md_files = list(folder.glob('*.md'))
    
    if not md_files:
        print(f"在文件夹 '{folder_path}' 中没有找到md文件")
        return
    
    print(f"找到 {len(md_files)} 个md文件")
    print("-" * 50)
    
    processed_count = 0
    skipped_count = 0
    
    for md_file in md_files:
        try:
            # 读取文件内容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已有sidebar_position
            if has_sidebar_position(content):
                print(f"跳过：{md_file.name} (已包含sidebar_position)")
                skipped_count += 1
                continue
            
            # 提取章节号
            chapter_num = extract_chapter_number(md_file.name, content)
            
            if chapter_num is None:
                print(f"警告：无法从 '{md_file.name}' 中提取章节号，跳过处理")
                skipped_count += 1
                continue
            
            # 添加sidebar_position
            new_content = add_sidebar_position(content, chapter_num)
            
            # 写回文件
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"处理完成：{md_file.name} -> sidebar_position: {chapter_num}")
            processed_count += 1
            
        except Exception as e:
            print(f"处理文件 '{md_file.name}' 时出错：{e}")
    
    print("-" * 50)
    print(f"处理完成！共处理 {processed_count} 个文件，跳过 {skipped_count} 个文件")


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法：python process_md_files.py <文件夹路径>")
        print("示例：python process_md_files.py ./my-website/docs/南明史")
        return
    
    folder_path = sys.argv[1]
    process_md_files(folder_path)


if __name__ == "__main__":
    main()
