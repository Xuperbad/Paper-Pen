#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
python process_md_files.py add "./my-website/docs/庆余年/第一卷"
python process_md_files.py remove "./my-website/docs/庆余年/第一卷"
Markdown文档处理脚本
功能：为指定文件夹内的所有md文档添加或删除sidebar_position配置
"""

import re
import sys
from pathlib import Path


def chinese_to_arabic(chinese_num):
    """
    将中文数字转换为阿拉伯数字，支持到万位

    Args:
        chinese_num: 中文数字字符串

    Returns:
        int: 对应的阿拉伯数字
    """
    chinese_digits = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9,
        '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5,
        '陆': 6, '柒': 7, '捌': 8, '玖': 9
    }

    chinese_units = {
        '十': 10, '拾': 10,
        '百': 100, '佰': 100,
        '千': 1000, '仟': 1000,
        '万': 10000, '萬': 10000
    }

    # 处理简单的一位数
    if len(chinese_num) == 1 and chinese_num in chinese_digits:
        return chinese_digits[chinese_num]

    # 标准化处理：统一使用简体字
    chinese_num = chinese_num.replace('拾', '十').replace('佰', '百').replace('仟', '千').replace('萬', '万')

    # 特殊情况：单独的"十"
    if chinese_num == '十':
        return 10

    # 处理复杂的中文数字
    result = 0
    temp_num = 0

    i = 0
    while i < len(chinese_num):
        char = chinese_num[i]

        if char in chinese_digits:
            temp_num = chinese_digits[char]
        elif char in chinese_units:
            unit_value = chinese_units[char]

            if unit_value == 10000:  # 万
                result += temp_num * unit_value
                temp_num = 0
            elif unit_value >= 10:  # 十、百、千
                if temp_num == 0:  # 处理"十"开头的情况，如"十一"
                    temp_num = 1
                result += temp_num * unit_value
                temp_num = 0
        elif char == '零':
            # 零不影响计算，跳过
            pass

        i += 1

    # 加上最后的个位数
    result += temp_num

    return result if result > 0 else None


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

    # 中文数字模式（支持百、千、万）
    chinese_patterns = [
        r'第([零一二三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬〇]+)章',
        r'第([零一二三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬〇]+)节'
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
    for line in lines[:5]:
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


def remove_sidebar_position(content):
    """
    从文档中删除sidebar_position配置

    Args:
        content: 原文件内容

    Returns:
        tuple: (处理后的内容, 是否找到并删除了sidebar_position)
    """
    lines = content.split('\n')

    # 检查是否有frontmatter
    if not lines or lines[0].strip() != '---':
        return content, False

    # 查找frontmatter结束位置
    end_index = -1
    for i in range(1, min(len(lines), 20)):  # 最多检查前20行
        if lines[i].strip() == '---':
            end_index = i
            break

    if end_index <= 0:
        return content, False

    # 提取frontmatter内容
    frontmatter_lines = lines[1:end_index]
    remaining_content = lines[end_index+1:]

    # 查找并删除sidebar_position行
    new_frontmatter_lines = []
    found_sidebar_position = False

    for line in frontmatter_lines:
        if 'sidebar_position' in line and ':' in line:
            found_sidebar_position = True
            continue  # 跳过这一行，即删除它
        new_frontmatter_lines.append(line)

    if not found_sidebar_position:
        return content, False

    # 重新组装内容
    if new_frontmatter_lines:
        # 还有其他frontmatter配置，保留frontmatter结构
        new_content = '---\n' + '\n'.join(new_frontmatter_lines) + '\n---\n' + '\n'.join(remaining_content)
    else:
        # frontmatter为空，完全删除frontmatter结构
        new_content = '\n'.join(remaining_content)
        # 删除开头的空行
        new_content = new_content.lstrip('\n')

    return new_content, True


def process_md_files(folder_path, action='add'):
    """
    处理指定文件夹中的所有md文件

    Args:
        folder_path: 目标文件夹路径
        action: 操作类型，'add' 为添加sidebar_position，'remove' 为删除sidebar_position
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

    action_desc = "添加" if action == 'add' else "删除"
    print(f"找到 {len(md_files)} 个md文件，准备{action_desc}sidebar_position配置")
    print("-" * 50)

    processed_count = 0
    skipped_count = 0

    for md_file in md_files:
        try:
            # 读取文件内容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if action == 'add':
                # 添加sidebar_position
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

                print(f"处理完成：{md_file.name} -> 添加 sidebar_position: {chapter_num}")
                processed_count += 1

            elif action == 'remove':
                # 删除sidebar_position
                new_content, found = remove_sidebar_position(content)

                if not found:
                    print(f"跳过：{md_file.name} (未找到sidebar_position)")
                    skipped_count += 1
                    continue

                # 写回文件
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"处理完成：{md_file.name} -> 删除 sidebar_position")
                processed_count += 1

        except Exception as e:
            print(f"处理文件 '{md_file.name}' 时出错：{e}")

    print("-" * 50)
    print(f"处理完成！共{action_desc} {processed_count} 个文件，跳过 {skipped_count} 个文件")


def main():
    """主函数"""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("使用方法：")
        print("  添加sidebar_position：python process_md_files.py add <文件夹路径>")
        print("  删除sidebar_position：python process_md_files.py remove <文件夹路径>")
        print("  兼容旧版本（默认添加）：python process_md_files.py <文件夹路径>")
        print()
        print("示例：")
        print("  python process_md_files.py add ./my-website/docs/南明史")
        print("  python process_md_files.py remove ./my-website/docs/南明史")
        print("  python process_md_files.py ./my-website/docs/南明史")
        return

    # 解析命令行参数
    if len(sys.argv) == 2:
        # 兼容旧版本，默认为添加操作
        action = 'add'
        folder_path = sys.argv[1]
    else:
        # 新版本，指定操作类型
        action = sys.argv[1].lower()
        folder_path = sys.argv[2]

        if action not in ['add', 'remove']:
            print(f"错误：不支持的操作 '{action}'，请使用 'add' 或 'remove'")
            return

    process_md_files(folder_path, action)


if __name__ == "__main__":
    main()
