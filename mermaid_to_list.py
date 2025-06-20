#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid Mindmap to Unordered List Converter

This script converts Mermaid mindmap syntax to markdown unordered lists.
It preserves the hierarchical structure and handles Chinese text properly.
"""

import re
import sys
from typing import List, Tuple


class MermaidToListConverter:
    def __init__(self):
        self.lines = []
        self.result = []
    
    def parse_mermaid_content(self, content: str) -> List[Tuple[int, str]]:
        """
        解析 Mermaid mindmap 内容，提取层级结构
        """
        lines = content.strip().split('\n')
        parsed_lines = []

        for line_text in lines:
            # 跳过空行和 mermaid 声明行
            if not line_text.strip() or line_text.strip() == 'mindmap':
                continue

            # 计算缩进层级 - 使用原始行来计算缩进
            indent_level = 0
            for char in line_text:
                if char == ' ':
                    indent_level += 1
                else:
                    break

            # 提取节点内容
            node_content = self.extract_node_content(line_text.strip())
            if node_content:
                parsed_lines.append((indent_level, node_content))

        return parsed_lines
    
    def extract_node_content(self, line: str) -> str:
        """
        从 Mermaid 节点语法中提取实际内容
        """
        line = line.strip()
        
        # 处理 root() 语法
        if line.startswith('root(') and line.endswith(')'):
            return line[5:-1]
        
        # 处理普通的 () 语法
        if line.startswith('(') and line.endswith(')'):
            return line[1:-1]
        
        # 处理其他格式，直接返回
        return line
    
    def convert_to_list(self, parsed_lines: List[Tuple[int, str]]) -> List[str]:
        """
        将解析后的层级结构转换为无序列表
        """
        result = []

        if not parsed_lines:
            return result

        # 找到最小缩进作为基准
        min_indent = min(indent for indent, _ in parsed_lines)

        for indent_level, content in parsed_lines:
            # 计算相对层级
            relative_level = (indent_level - min_indent) // 2

            # 生成对应层级的列表项
            prefix = '  ' * relative_level + '- '
            result.append(prefix + content)

        return result
    
    def process_file(self, input_file: str, output_file: str = None):
        """
        处理文件，从输入文件读取 Mermaid mindmap，输出为无序列表
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取 mermaid 代码块
            mermaid_content = self.extract_mermaid_block(content)
            if not mermaid_content:
                print("未找到 mermaid mindmap 内容")
                return
            
            # 解析并转换
            parsed_lines = self.parse_mermaid_content(mermaid_content)
            list_result = self.convert_to_list(parsed_lines)
            
            # 输出结果
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(list_result))
                print(f"转换完成，结果已保存到: {output_file}")
            else:
                print("转换结果:")
                print('\n'.join(list_result))
                
        except FileNotFoundError:
            print(f"文件未找到: {input_file}")
        except Exception as e:
            print(f"处理文件时出错: {e}")
    
    def extract_mermaid_block(self, content: str) -> str:
        """
        从 markdown 内容中提取 mermaid 代码块
        """
        # 查找 ```mermaid 代码块
        pattern = r'```mermaid\s*\n(.*?)\n```'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1)
        
        # 如果没找到代码块，假设整个内容就是 mermaid
        return content
    
    def process_text(self, mermaid_text: str) -> str:
        """
        直接处理 mermaid 文本，返回无序列表字符串
        """
        parsed_lines = self.parse_mermaid_content(mermaid_text)
        list_result = self.convert_to_list(parsed_lines)
        return '\n'.join(list_result)


def main():
    """
    主函数，处理命令行参数
    """
    converter = MermaidToListConverter()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python mermaid_to_list.py <输入文件> [输出文件]")
        print("  如果不指定输出文件，结果将打印到控制台")
        print()
        print("示例:")
        print("  python mermaid_to_list.py input.md")
        print("  python mermaid_to_list.py input.md output.md")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    converter.process_file(input_file, output_file)


if __name__ == "__main__":
    main()
