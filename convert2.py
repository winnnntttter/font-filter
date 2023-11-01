input_file = "src/AlibabaPuHuiTi-3-55-Regular.ttf"  # 全量字体
output_file = "new_font.ttf"  # 基础字符集

used_chars = "12345你我他"  # 读取用到的字符

# 读取用到的字表，通过ord()函数转一下
used_unicodes = [ord(char) for char in used_chars]

font = fontforge.open(input_file)
print(font.familyname)
for char_name in font:
    glyph = font[char_name]
    unicode = glyph.unicode
    if unicode in used_unicodes:
        # 保留的字符
        pass
    else:
        # 这里假设单个glyph没有被多个unicode使用，如果需要相应处理，过滤一下
        glyph.clear()

font.generate(output_file)
font.close()
