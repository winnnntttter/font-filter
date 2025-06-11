#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 生成测试HTML文件

import os

# 配置
font_family = "YSBiaoTiHei"
output_dir = "dist"
html_file = os.path.join(output_dir, "test.html")
common_chars_file = "常用字符3500.txt"

# 读取常用字符
with open(common_chars_file, 'r', encoding='utf-8') as f:
    common_chars = f.read().strip()

# 准备HTML内容
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{font_family} 字体测试</title>
  <link rel="stylesheet" href="font.css">
  <style>
    body {{
      font-family: '{font_family}', sans-serif;
      line-height: 1.8;
      margin: 0;
      padding: 20px;
    }}
    h1, h2 {{
      color: #333;
    }}
    .sample {{
      font-size: 24px;
      margin: 20px 0;
      padding: 15px;
      border: 1px solid #ddd;
      border-radius: 5px;
    }}
    .common {{
      color: #2c3e50;
    }}
    .info {{
      font-family: Arial, sans-serif;
      font-size: 14px;
      color: #666;
      margin-top: 40px;
    }}
    .breakdown {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 20px;
    }}
    .char-block {{
      border: 1px solid #eee;
      padding: 5px;
      font-size: 28px;
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
  </style>
</head>
<body>
  <h1>{font_family} 字体测试页面</h1>

  <h2>常用字符示例</h2>
  <div class="sample common">
    {common_chars[:100]}...
  </div>

  <h2>字符使用示例</h2>
  <div class="sample">
    那是一个秋天的黄昏，现在想起来，仍能看见夕阳染红的天空下，大雁成行南飞的情景。
    <br><br>
    这里有数字：1234567890
    <br>
    这里有英文字母：ABCDEFGabcdefg
    <br>
    这里有标点符号：，。？！：；''""（）《》【】
  </div>

  <h2>字符一览</h2>
  <div class="breakdown">
    {"".join([f'<div class="char-block">{c}</div>' for c in common_chars[:200]])}
    <div style="width:100%">...等更多字符</div>
  </div>

  <div class="info">
    <p>此页面使用了分割后的多个字体文件，通过CSS的unicode-range特性按需加载。</p>
  </div>
</body>
</html>
"""

# 写入HTML文件
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"测试HTML文件已生成: {html_file}")
