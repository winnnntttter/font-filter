import fontforge

# 指定要提取的字符
chars_to_extract = "我你他"

# 加载字体文件
font = fontforge.open("src/AlibabaPuHuiTi-3-55-Regular.ttf")

# 创建一个新字体文件
new_font = fontforge.font()

# 将要提取的字符添加到新字体文件中
for char in chars_to_extract:
    glyph = font[char]
    new_font.selection.select(("more", None), glyph)
    new_font.copy()

# 将新字体文件保存为ttf格式
new_font.generate("new_font.ttf")

# 关闭字体文件
font.close()
new_font.close()