# 转换TTF字体为WOFF和WOFF2格式

import os
import json
from fontTools.ttLib import TTFont

# 配置
input_dir = "dist"
font_info_file = os.path.join(input_dir, "font_info.json")

# 加载字体信息
with open(font_info_file, 'r', encoding='utf-8') as f:
    font_info = json.load(f)

# 转换每个TTF字体为WOFF和WOFF2
for info in font_info:
    ttf_path = os.path.join(input_dir, info['file'])
    woff_path = os.path.join(input_dir, info['woff'])
    woff2_path = os.path.join(input_dir, info['woff2'])

    # 打开TTF字体
    font = TTFont(ttf_path)

    # 转换为WOFF
    font.flavor = "woff"
    font.save(woff_path)
    print(f"生成 {info['woff']}")

    # 转换为WOFF2
    font.flavor = "woff2"
    font.save(woff2_path)
    print(f"生成 {info['woff2']}")

    font.close()

print("所有字体转换完成!")
