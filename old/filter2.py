# from fontforge import *
import fontforge
import os

# 指定要提取的字符
used_chars = "12345你我他"  # 读取用到的字符
# 读取用到的字表，通过ord()函数转一下
used_unicodes = [ord(char) for char in used_chars]

# 加载字体文件
font = fontforge.open("src/AlibabaPuHuiTi-3-55-Regular.ttf")
print(font.familyname)

# 创建一个新字体文件
new_font = fontforge.font()

# 将要提取的字符添加到新字体文件中
for unicode in used_unicodes:
    try:
        print(f"Extracting character '{chr(unicode)}' (unicode: {unicode})")
        # font 中 Unicode 为 unicode 的字符
        glyph = font[unicode]
        print(glyph)
        new_font.selection.select(("more", None), glyph)
        new_font.copy()
    except TypeError:
        print(f"Skipping character '{char}' because it does not exist in the font.")

# 将新字体文件保存为ttf、woff和woff2格式
new_font.generate("AlibabaPuHuiTi-3-55-Regular-extracted.ttf")
os.system("pyftsubset AlibabaPuHuiTi-3-55-Regular-extracted.ttf --output-file=AlibabaPuHuiTi-3-55-Regular-extracted.woff --flavor=woff --with-zopfli")
os.system("pyftsubset AlibabaPuHuiTi-3-55-Regular-extracted.ttf --output-file=AlibabaPuHuiTi-3-55-Regular-extracted.woff2 --flavor=woff2 --with-zopfli")


# 暂时不能用

# Alibaba PuHuiTi 3.0 55 Regular
# Extracting character '1' (unicode: 49)
# <Glyph one in font AlibabaPuHuiTi_3_55_Regular>
# Extracting character '2' (unicode: 50)
# <Glyph two in font AlibabaPuHuiTi_3_55_Regular>
# Extracting character '3' (unicode: 51)
# <Glyph three in font AlibabaPuHuiTi_3_55_Regular>
# Extracting character '4' (unicode: 52)
# <Glyph four in font AlibabaPuHuiTi_3_55_Regular>
# Extracting character '5' (unicode: 53)
# <Glyph five in font AlibabaPuHuiTi_3_55_Regular>
# Extracting character '你' (unicode: 20320)
# <Glyph uni4F60 in font AlibabaPuHuiTi_3_55_Regular>
# Traceback (most recent call last):
#   File "E:\test\字体选取指定\convert.py", line 24, in <module>
#     new_font.selection.select(("more", None), glyph)
# ValueError: Encoding is out of range