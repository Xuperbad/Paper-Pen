#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用书籍拆分脚本
功能：
1. 按章节拆分书籍
2. 清理所有图片引用语句
3. 生成符合 Docusaurus 格式的 Markdown 文件
4. 支持多种章节格式
"""

import re
import os
from pathlib import Path

def clean_image_references(content):
    """
    清理文档中的图片引用和断开的链接
    包括：
    - ![logo](../Images/logo.png)
    - ![](../Images/img02.jpg)
    - ![img00](../Images/img00.jpg)
    - ![s1](../Images/s1.jpg)
    - ![tt](../Images/tt.jpg)
    - [xxx](../Text/Section*.xhtml#xxx)
    - [xxx](./Text/Section*.xhtml#xxx)
    等各种格式的图片引用和断开的链接
    """
    # 匹配各种图片引用格式
    image_patterns = [
        r'!\[.*?\]\(\.\.\/Images\/.*?\)',  # ![xxx](../Images/xxx)
        r'!\[\]\(\.\.\/Images\/.*?\)',     # ![](../Images/xxx)
        r'!\[.*?\]\(Images\/.*?\)',        # ![xxx](Images/xxx)
        r'!\[\]\(Images\/.*?\)',           # ![](Images/xxx)
        r'!\[.*?\]\(\.\/Images\/.*?\)',    # ![xxx](./Images/xxx)
        r'!\[\]\(\.\/Images\/.*?\)',       # ![](./Images/xxx)
    ]

    # 匹配断开的内部链接格式
    link_patterns = [
        r'\[\[.*?\]\]\(\.\.\/Text\/.*?\.xhtml.*?\)',  # [[xxx]](../Text/xxx.xhtml)
        r'\[.*?\]\(\.\.\/Text\/.*?\.xhtml.*?\)',      # [xxx](../Text/xxx.xhtml)
        r'\[.*?\]\(\.\/Text\/.*?\.xhtml.*?\)',        # [xxx](./Text/xxx.xhtml)
    ]

    cleaned_content = content

    # 清理图片引用
    for pattern in image_patterns:
        cleaned_content = re.sub(pattern, '', cleaned_content)

    # 清理断开的内部链接，保留链接文本
    for pattern in link_patterns:
        # 提取链接文本并保留
        def replace_link(match):
            link_text = re.search(r'\[([^\]]*)\]', match.group(0))
            if link_text:
                return link_text.group(1)
            return ''
        cleaned_content = re.sub(pattern, replace_link, cleaned_content)

    # 清理多余的空行
    cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)

    return cleaned_content

def extract_chapters_chinese_history(content):
    """
    提取中国通史的章节内容
    """
    chapters = []
    
    # 匹配章节标题的正则表达式
    chapter_pattern = r'^## (第[一二三四五六七八九十\d]+章[^#\n]*)'
    
    # 分割内容
    lines = content.split('\n')
    current_chapter = None
    current_content = []
    
    for line in lines:
        # 检查是否是章节标题
        chapter_match = re.match(chapter_pattern, line)
        
        if chapter_match:
            # 保存上一章内容
            if current_chapter:
                chapters.append({
                    'title': current_chapter,
                    'content': '\n'.join(current_content)
                })
            
            # 开始新章节
            current_chapter = chapter_match.group(1)
            current_content = [line]  # 包含章节标题
        else:
            if current_chapter:
                current_content.append(line)
    
    # 保存最后一章
    if current_chapter:
        chapters.append({
            'title': current_chapter,
            'content': '\n'.join(current_content)
        })
    
    return chapters

def extract_chapters_game_book(content):
    """
    提取游戏改变世界的章节内容
    """
    chapters = []

    # 匹配章节标题的正则表达式
    chapter_pattern = r'^## (第\d+章[^#\n]*)'

    # 分割内容
    lines = content.split('\n')
    current_chapter = None
    current_content = []

    for line in lines:
        # 检查是否是章节标题
        chapter_match = re.match(chapter_pattern, line)

        if chapter_match:
            # 保存上一章内容
            if current_chapter:
                chapters.append({
                    'title': current_chapter,
                    'content': '\n'.join(current_content)
                })

            # 开始新章节
            current_chapter = chapter_match.group(1)
            current_content = [line]  # 包含章节标题
        else:
            if current_chapter:
                current_content.append(line)

    # 保存最后一章
    if current_chapter:
        chapters.append({
            'title': current_chapter,
            'content': '\n'.join(current_content)
        })

    return chapters

def generate_sidebar_position_chinese(chapter_num):
    """
    根据中文章节号生成侧边栏位置
    """
    # 提取章节数字
    match = re.search(r'第([一二三四五六七八九十\d]+)章', chapter_num)
    if match:
        chinese_num = match.group(1)
        # 转换中文数字为阿拉伯数字
        chinese_to_arabic = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
            '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
            '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
            '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30,
            '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35,
            '三十六': 36, '三十七': 37, '三十八': 38, '三十九': 39, '四十': 40,
            '四十一': 41, '四十二': 42, '四十三': 43, '四十四': 44, '四十五': 45,
            '四十六': 46, '四十七': 47, '四十八': 48, '四十九': 49, '五十': 50,
            '五十一': 51, '五十二': 52, '五十三': 53, '五十四': 54
        }
        
        if chinese_num in chinese_to_arabic:
            return chinese_to_arabic[chinese_num]
        elif chinese_num.isdigit():
            return int(chinese_num)
    
    return 1

def generate_sidebar_position_arabic(chapter_num):
    """
    根据阿拉伯数字章节号生成侧边栏位置
    """
    # 提取章节数字
    match = re.search(r'第(\d+)章', chapter_num)
    if match:
        return int(match.group(1))
    
    return 1

def create_chapter_file(chapter, output_dir, book_type):
    """
    创建章节文件
    """
    title = chapter['title']
    content = chapter['content']
    
    # 清理图片引用
    cleaned_content = clean_image_references(content)
    
    # 生成文件名（移除特殊字符）
    filename = re.sub(r'[^\w\s-]', '', title).strip()
    filename = re.sub(r'[-\s]+', '-', filename)
    filename = f"{filename}.md"
    
    # 生成侧边栏位置
    if book_type == 'chinese_history':
        sidebar_position = generate_sidebar_position_chinese(title)
    else:
        sidebar_position = generate_sidebar_position_arabic(title)
    
    # 添加 frontmatter
    frontmatter = f"""---
sidebar_position: {sidebar_position}
---

"""
    
    # 组合最终内容
    final_content = frontmatter + cleaned_content
    
    # 写入文件
    file_path = output_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"已创建: {filename}")
    return filename

def process_book(input_file, output_dir, book_type):
    """
    处理单本书籍
    """
    print(f"\n开始处理文件: {input_file}")
    print(f"输出目录: {output_dir}")
    print(f"书籍类型: {book_type}")
    
    # 创建输出目录
    output_dir.mkdir(exist_ok=True)
    
    # 读取原文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
        return []
    except Exception as e:
        print(f"错误：读取文件失败 - {e}")
        return []
    
    # 根据书籍类型提取章节
    if book_type == 'chinese_history':
        chapters = extract_chapters_chinese_history(content)
    elif book_type == 'game_book':
        chapters = extract_chapters_game_book(content)
    else:
        print(f"错误：不支持的书籍类型 {book_type}")
        return []
    
    if not chapters:
        print("警告：没有找到任何章节")
        return []
    
    print(f"找到 {len(chapters)} 个章节")
    
    # 创建章节文件
    created_files = []
    for chapter in chapters:
        filename = create_chapter_file(chapter, output_dir, book_type)
        created_files.append(filename)
    
    print(f"\n处理完成！共创建了 {len(created_files)} 个文件：")
    for filename in created_files:
        print(f"  - {filename}")
    
    print(f"\n所有文件已保存到: {output_dir}")
    
    return created_files

def main():
    """
    主函数
    """
    # 书籍配置
    books = [
        {
            'input_file': Path("books/中国通史-吕思勉.md"),
            'output_dir': Path("my-website/docs/中国通史"),
            'book_type': 'chinese_history'
        },
        {
            'input_file': Path("books/游戏改变世界：游戏化如何让现实变得更美好.md"),
            'output_dir': Path("my-website/docs/游戏改变世界"),
            'book_type': 'game_book'
        }
    ]
    
    all_created_files = []
    
    for book_config in books:
        created_files = process_book(
            book_config['input_file'],
            book_config['output_dir'],
            book_config['book_type']
        )
        all_created_files.extend(created_files)
    
    print(f"\n=== 总结 ===")
    print(f"总共处理了 {len(books)} 本书")
    print(f"总共创建了 {len(all_created_files)} 个文件")
    print("\n注意事项：")
    print("1. 所有图片引用已被清理")
    print("2. 每个章节都添加了 frontmatter 和 sidebar_position")
    print("3. 文件名已标准化，移除了特殊字符")
    print("4. 支持中文数字和阿拉伯数字章节号")

if __name__ == "__main__":
    main()
