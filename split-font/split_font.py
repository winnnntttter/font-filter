#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 分割字体文件

import os
import math
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter
import json

# 配置参数
input_font = "src/ysbth.ttf"  # 输入字体文件
output_dir = "dist"           # 输出目录
common_chars_file = "常用字符3500.txt"  # 常用字符文件
font_prefix = "font"          # 输出字体文件名前缀
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

# 将常用字符转换为unicode编码
common_unicodes = [ord(char) for char in common_chars]
common_unicodes = [u for u in common_unicodes if u in all_unicodes]

# 剩余的字符
other_unicodes = [u for u in all_unicodes if u not in common_unicodes]

print(f"常用字符: {len(common_unicodes)} 个")
print(f"其他字符: {len(other_unicodes)} 个")

# 大致估算每个文件应包含多少字符
total_chars = len(all_unicodes)
common_ratio = 0.6  # 常用字符占比，可以调整
common_fonts_count = math.ceil(target_count * 0.3)  # 常用字符分配到前30%的文件
chars_per_common_font = math.ceil(len(common_unicodes) / common_fonts_count)
chars_per_other_font = math.ceil(len(other_unicodes) / (target_count - common_fonts_count))

# 分割常用字符和其他字符
common_chunks = []
for i in range(0, len(common_unicodes), chars_per_common_font):
    common_chunks.append(common_unicodes[i:i + chars_per_common_font])

other_chunks = []
for i in range(0, len(other_unicodes), chars_per_other_font):
    other_chunks.append(other_unicodes[i:i + chars_per_other_font])

# 合并分组形成最终的字符块列表
chunks = common_chunks + other_chunks

# 限制块数量不超过目标数量
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
    output_path = os.path.join(output_dir, output_name)

    # 保存子集字体
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
