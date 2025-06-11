#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
字体子集化工具 - 使用fontTools实现
本脚本可以从一个大字体文件中提取指定的字符集，生成更小的字体文件
"""

import os
import json
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter
import logging

# 配置日志 - 如果不需要详细日志，可以将级别设置为WARNING
logging.basicConfig(level=logging.INFO)

# 添加命令行参数支持
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='生成字体子集')
    parser.add_argument('--input', '-i', type=str, default="src/NotoSerifSC-Black.ttf",
                        help='输入字体文件路径')
    parser.add_argument('--output', '-o', type=str, default="dist/NotoSerifSC-Black.ttf",
                        help='输出字体文件路径')
    parser.add_argument('--chars', '-c', type=str, default=None,
                        help='要包含的字符，直接指定字符串')
    parser.add_argument('--chars-file', '-f', type=str, default=None,
                        help='要包含的字符，从文件读取')
    return parser.parse_args()

# 解析命令行参数
args = parse_args()

# 配置
input_file = args.input
output_file = args.output

# 确定要保留的字符
used_chars = ""
if args.chars:
    # 如果在命令行指定了字符
    used_chars = args.chars
elif args.chars_file:
    # 如果指定了字符文件
    try:
        with open(args.chars_file, 'r', encoding='utf-8') as f:
            used_chars = f.read()
    except Exception as e:
        print(f"读取字符文件时出错: {e}")
        used_chars = "如何结合国家战略及区域发展选专业？"  # 使用默认字符
else:
    # 如果没有指定，使用默认字符
    # used_chars = "如何结合国家战略及区域发展选专业？"
    used_chars = "教育部供需对接就业育人项目"

# 如果需要保留特定Unicode值的字符，可以这样添加
# 例如，康熙部首"目"(U+2F6C)
# used_chars += "\u2F6C\u319F"

# 去重字符
used_chars = "".join(set(used_chars))
print(f"需要保留的字符数量: {len(used_chars)}")

# 将字符转换为Unicode码点
used_unicodes = [ord(char) for char in used_chars]

# 确保输出目录存在
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# 打开字体文件
font = TTFont(input_file)
print(f"加载字体: {input_file}")

# 获取字体名称
name_table = font['name']
for record in name_table.names:
    if record.nameID == 1:  # Font Family name
        try:
            print(f"fontFamily: {record.toUnicode()}")
            break
        except:
            pass

# 创建用于保存字符到字形ID的映射
char_to_glyph_map = {}
glyph_id_to_keep = set()

# 处理所有映射表以获取所有可能的字符映射
# (类似于fontforge中的glyph.altuni功能)
for table in font['cmap'].tables:
    for unicode_value, glyph_name in table.cmap.items():
        if unicode_value not in char_to_glyph_map:
            char_to_glyph_map[unicode_value] = []
        if glyph_name not in char_to_glyph_map[unicode_value]:
            char_to_glyph_map[unicode_value].append(glyph_name)

# fontTools.subset模块的正确用法
found_chars = False
unicodes_to_keep = set()

for unicode_value in used_unicodes:
    unicodes_to_keep.add(unicode_value)
    found_chars = True
    if unicode_value in char_to_glyph_map:
        print(f"保留字符 U+{unicode_value:04X}: {chr(unicode_value)}")

if not found_chars:
    print("警告: 没有找到任何需要保留的字符!")

# 创建子集化器并配置
subsetter = Subsetter()
# 填充要保留的Unicode码点
subsetter.populate(unicodes=unicodes_to_keep)

# 执行子集化
subsetter.subset(font)

# 保存子集化后的字体
font.save(output_file)
print(f"生成子集字体: {output_file}")

# 转换为WOFF和WOFF2格式
# 如果只需要TTF文件，可以将下面的代码注释掉
# WOFF格式
font.flavor = "woff"
woff_output = output_file.replace(".ttf", ".woff")
font.save(woff_output)
print(f"生成WOFF: {woff_output}")

# WOFF2格式
font.flavor = "woff2"
woff2_output = output_file.replace(".ttf", ".woff2")
font.save(woff2_output)
print(f"生成WOFF2: {woff2_output}")

# 打印文件大小对比
original_size = os.path.getsize(input_file) / 1024
subset_size = os.path.getsize(output_file) / 1024
woff_size = os.path.getsize(woff_output) / 1024
woff2_size = os.path.getsize(woff2_output) / 1024

print("\n文件大小对比:")
print(f"原始TTF: {original_size:.2f}KB")
print(f"子集TTF: {subset_size:.2f}KB (缩减了 {(original_size - subset_size) / original_size * 100:.1f}%)")
print(f"子集WOFF: {woff_size:.2f}KB")
print(f"子集WOFF2: {woff2_size:.2f}KB")



""" Unicode字符\u2F6C和\u76EE分别对应的是“⽬”和“目”。其中：

\u2F6C 是一个康熙部首字符，表示“目”部首。
\u76EE 是一个常用汉字，表示“目”。
在某些字体（如思源宋体）中，这两个字符可能会被设计成相同或非常相似的形状，因为它们在视觉上代表相同的概念，即“目”。这种设计选择是为了在字体中保持一致性和美观。 """