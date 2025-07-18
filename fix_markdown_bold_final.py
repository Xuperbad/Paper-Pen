#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py fix_markdown_bold_final.py my-website/docs/庆余年/第一卷
修复Markdown文件中加粗格式的脚本
将 **"文本"** 格式修正为 "**文本**" 格式
"""

import os
import re
import argparse
from pathlib import Path

def fix_bold_format(content):
    """
    修复Markdown中的加粗格式问题
    将 **"文本"** 转换为 "**文本**"
    将 **'文本'** 转换为 '**文本**'
    """
    # 模式1: 中文左右双引号 Unicode 8220, 8221 (这是我们在文件中发现的)
    pattern1 = r'\*\*\u201c(.+?)\u201d\*\*'
    replacement1 = '\u201c**\\1**\u201d'
    content = re.sub(pattern1, replacement1, content)

    # 模式2: 英文双引号
    pattern2 = r'\*\*"(.+?)"\*\*'
    replacement2 = '"**\\1**"'
    content = re.sub(pattern2, replacement2, content)

    # 模式3: 英文单引号
    pattern3 = r"\*\*'(.+?)'\*\*"
    replacement3 = "'**\\1**'"
    content = re.sub(pattern3, replacement3, content)

    # 模式4: 中文左右单引号 Unicode 8216, 8217
    pattern4 = r'\*\*\u2018(.+?)\u2019\*\*'
    replacement4 = '\u2018**\\1**\u2019'
    content = re.sub(pattern4, replacement4, content)

    # 模式5: 中文双引号 Unicode 12300, 12301
    pattern5 = r'\*\*\u300c(.+?)\u300d\*\*'
    replacement5 = '\u300c**\\1**\u300d'
    content = re.sub(pattern5, replacement5, content)

    # 模式6: 中文单引号 Unicode 12302, 12303
    pattern6 = r'\*\*\u300e(.+?)\u300f\*\*'
    replacement6 = '\u300e**\\1**\u300f'
    content = re.sub(pattern6, replacement6, content)

    # 模式7: 书名号 《》
    pattern7 = r'\*\*《(.+?)》\*\*'
    replacement7 = '《**\\1**》'
    content = re.sub(pattern7, replacement7, content)

    # 模式8: 书名号 〈〉
    pattern8 = r'\*\*〈(.+?)〉\*\*'
    replacement8 = '〈**\\1**〉'
    content = re.sub(pattern8, replacement8, content)

    return content

def process_markdown_file(file_path):
    """
    处理单个Markdown文件
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 修复加粗格式
        fixed_content = fix_bold_format(original_content)
        
        # 检查是否有变化
        if original_content != fixed_content:
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            # 统计修改次数
            patterns = [
                r'\*\*\u201c(.+?)\u201d\*\*',  # 中文左右双引号
                r'\*\*"(.+?)"\*\*',  # 英文双引号
                r"\*\*'(.+?)'\*\*",  # 英文单引号
                r'\*\*\u2018(.+?)\u2019\*\*',  # 中文左右单引号
                r'\*\*\u300c(.+?)\u300d\*\*',  # 中文双引号
                r'\*\*\u300e(.+?)\u300f\*\*',  # 中文单引号
                r'\*\*《(.+?)》\*\*',  # 书名号
                r'\*\*〈(.+?)〉\*\*',  # 书名号
            ]
            
            changes = 0
            for pattern in patterns:
                changes += len(re.findall(pattern, original_content))
            
            print(f"✅ 已修复: {file_path} (修改了 {changes} 处)")
            return True
        else:
            print(f"⏭️  无需修改: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 处理文件失败: {file_path} - {str(e)}")
        return False

def process_directory(directory_path):
    """
    处理指定目录下的所有Markdown文件
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"❌ 目录不存在: {directory_path}")
        return
    
    if not directory.is_dir():
        print(f"❌ 路径不是目录: {directory_path}")
        return
    
    # 查找所有.md文件
    md_files = list(directory.rglob("*.md"))
    
    if not md_files:
        print(f"📁 目录中没有找到Markdown文件: {directory_path}")
        return
    
    print(f"📁 找到 {len(md_files)} 个Markdown文件")
    print("=" * 50)
    
    processed_count = 0
    modified_count = 0
    
    for md_file in md_files:
        processed_count += 1
        if process_markdown_file(md_file):
            modified_count += 1
    
    print("=" * 50)
    print(f"📊 处理完成:")
    print(f"   - 总文件数: {processed_count}")
    print(f"   - 修改文件数: {modified_count}")
    print(f"   - 未修改文件数: {processed_count - modified_count}")

def main():
    parser = argparse.ArgumentParser(
        description="修复Markdown文件中的加粗格式问题",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python fix_markdown_bold_final.py my-website/docs/庆余年/第一卷/test
  python fix_markdown_bold_final.py my-website/docs/庆余年
  python fix_markdown_bold_final.py my-website/docs
        """
    )
    
    parser.add_argument(
        'directory',
        help='要处理的目录路径（相对于当前工作目录）'
    )
    
    args = parser.parse_args()
    
    print("🔧 Markdown加粗格式修复工具 (最终版)")
    print(f"📂 目标目录: {args.directory}")
    print("🔍 正在搜索Markdown文件...")
    print()
    
    process_directory(args.directory)

if __name__ == "__main__":
    main()
