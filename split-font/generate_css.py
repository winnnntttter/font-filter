# 生成CSS文件

import os
import json

# 配置
font_family = "YSBiaoTiHei"  # 字体名称
input_dir = "dist"
css_file = os.path.join(input_dir, "ysbth-font.css")
font_info_file = os.path.join(input_dir, "font_info.json")

# 加载字体信息
with open(font_info_file, 'r', encoding='utf-8') as f:
    font_info = json.load(f)

# 生成CSS内容
css_content = f"""/* {font_family} 字体CSS，自动生成 */
"""

# 为每个子集字体生成@font-face规则
for info in font_info:
    # 计算unicode范围字符串
    unicode_range = ", ".join(info['unicode_range'])

    css_content += f"""
@font-face {{
  font-family: '{font_family}';
  src: url('./{info['woff2']}') format('woff2'),
       url('./{info['woff']}') format('woff'),
       url('./{info['file']}') format('truetype');
  font-weight: normal;
  font-style: normal;
  unicode-range: {unicode_range};
}}
"""

# 写入CSS文件
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(css_content)

print(f"CSS文件已生成: {css_file}")
