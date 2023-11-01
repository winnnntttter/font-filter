# from fontforge import *
import fontforge
import os

# 指定要提取的字符
chars_to_extract = "12345"

# 加载字体文件
font = fontforge.open("src/AlibabaPuHuiTi-3-55-Regular.ttf")
print(font.familyname)

# 创建一个新字体文件
new_font = fontforge.font()

# 将要提取的字符添加到新字体文件中
for char in chars_to_extract:
    try:
        glyph = font[char]
        new_font.selection.select(("more", None), glyph)
        new_font.copy()
    except TypeError:
        print(f"Skipping character '{char}' because it does not exist in the font.")

# 将新字体文件保存为ttf、woff和woff2格式
new_font.generate("AlibabaPuHuiTi-3-55-Regular-extracted.ttf")
os.system("pyftsubset AlibabaPuHuiTi-3-55-Regular-extracted.ttf --output-file=AlibabaPuHuiTi-3-55-Regular-extracted.woff --flavor=woff --with-zopfli")
os.system("pyftsubset AlibabaPuHuiTi-3-55-Regular-extracted.ttf --output-file=AlibabaPuHuiTi-3-55-Regular-extracted.woff2 --flavor=woff2 --with-zopfli")