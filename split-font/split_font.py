#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 分割字体文件

import os
import math
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter
import json
from collections import defaultdict

# 配置参数
input_font = "src/ysbth.ttf"  # 输入字体文件
output_dir = "dist"           # 输出目录
common_chars_file = "常用字符3500.txt"  # 常用字符文件
font_prefix = "ysbth-font"    # 输出字体文件名前缀
target_count = 10             # 目标分割数量
target_size_kb = 100          # 目标每个文件大小(KB)

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取常用字符
with open(common_chars_file, 'r', encoding='utf-8') as f:
    common_chars = f.read().strip()

# 打开字体文件
font = TTFont(input_font)

# 获取字体中的所有字符编码
all_unicodes = set()
for table in font['cmap'].tables:
    for code, name in table.cmap.items():
        all_unicodes.add(code)

print(f"字体中共有 {len(all_unicodes)} 个字符")

# 将所有字符分类
# 1. 基本ASCII（英文、数字、基本标点：这些几乎总是需要的）
basic_ascii = [u for u in all_unicodes if 0x0020 <= u <= 0x007F]  # 空格到~

# 2. 中文标点和常见符号
chinese_punct = []
punct_ranges = [
    (0x3000, 0x303F),  # CJK符号和标点
    (0xFF00, 0xFFEF),  # 全角字符
    (0x2000, 0x206F),  # 常用标点
    (0x25A0, 0x25FF),  # 几何图形
]
for start, end in punct_ranges:
    chinese_punct.extend([u for u in all_unicodes if start <= u <= end])

# 3. 常用汉字（按照unicode code point范围分组，保证相关汉字在一起）
common_unicodes = [ord(char) for char in common_chars if ord(char) > 0x007F]
common_unicodes = [u for u in common_unicodes if u in all_unicodes]

# 根据Unicode码点的范围分组
unicode_groups = defaultdict(list)
for u in common_unicodes:
    # 按每1000个码点一组进行分组
    group_key = u // 1000
    unicode_groups[group_key].append(u)

# 提取分组的常用汉字
grouped_common_chars = []
for group_key in sorted(unicode_groups.keys()):
    grouped_common_chars.append(unicode_groups[group_key])

# 4. 其他Unicode字符（非ASCII，非中文标点，非常用汉字）
other_unicodes = [u for u in all_unicodes if u > 0x007F and u not in common_unicodes and u not in chinese_punct]

print(f"基本ASCII: {len(basic_ascii)} 个")
print(f"中文标点和符号: {len(chinese_punct)} 个")
print(f"常用汉字: {len(common_unicodes)} 个")
print(f"其他字符: {len(other_unicodes)} 个")

# 准备分块
chunks = []

# 第1块：基本ASCII + 中文标点（这些几乎总是需要的）
first_block = basic_ascii + chinese_punct
chunks.append(first_block)

# 更平衡的分配策略
# 所有字符（基本ASCII和中文标点已经在第一个文件中）
all_remaining_chars = common_unicodes + other_unicodes

# 计算每个文件的大致字符数量
total_remaining_chars = len(all_remaining_chars)
files_needed = target_count - 1  # 第一个文件已用于ASCII和标点
chars_per_file = total_remaining_chars // files_needed + 1

# 均匀分配所有剩余字符
for i in range(0, total_remaining_chars, chars_per_file):
    chunk = all_remaining_chars[i:i + chars_per_file]
    if chunk:  # 确保块不为空
        chunks.append(chunk)

# 如果产生的分块超过了目标数量，合并最后几个块
if len(chunks) > target_count:
    # 合并最后的块
    last_chunks = chunks[target_count-1:]
    merged_last_chunk = []
    for chunk in last_chunks:
        merged_last_chunk.extend(chunk)
    chunks = chunks[:target_count-1] + [merged_last_chunk]

# 保存分割信息，用于生成CSS
font_info = []

# 处理每个分割块，生成子集字体
for i, chunk in enumerate(chunks):
    if not chunk:  # 跳过空块
        continue

    # 创建子集
    subsetter = Subsetter()
    subsetter.populate(unicodes=chunk)
    font_subset = TTFont(input_font)
    subsetter.subset(font_subset)

    # 输出文件名
    output_name = f"{font_prefix}{i+1}.ttf"
    output_path = os.path.join(output_dir, output_name)    # 保存子集字体
    font_subset.save(output_path)

    # 计算unicode范围，用于CSS的unicode-range
    ranges = []
    chunk.sort()
    start = chunk[0]
    end = start

    for code in chunk[1:]:
        if code == end + 1:
            end = code
        else:
            # 添加一个范围
            if start == end:
                ranges.append(f"U+{start:04X}")
            else:
                ranges.append(f"U+{start:04X}-{end:04X}")
            # 开始新的范围
            start = code
            end = code

    # 添加最后一个范围
    if start == end:
        ranges.append(f"U+{start:04X}")
    else:
        ranges.append(f"U+{start:04X}-{end:04X}")

    font_info.append({
        'file': output_name,
        'woff': output_name.replace('.ttf', '.woff'),
        'woff2': output_name.replace('.ttf', '.woff2'),
        'unicode_range': ranges,
        'char_count': len(chunk)
    })

    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"生成 {output_name}: {len(chunk)} 个字符, 文件大小: {file_size_kb:.2f}KB")

# 保存字体信息到JSON文件，方便转换脚本使用
with open(os.path.join(output_dir, "font_info.json"), "w", encoding="utf-8") as f:
    json.dump(font_info, f, ensure_ascii=False, indent=2)

print(f"共生成 {len(font_info)} 个子集字体文件")
