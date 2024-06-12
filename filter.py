import os
# from fontTools.ttLib import TTFont

input_file = "src/AlibabaPuHuiTi-3-85-Bold.ttf"  # 全量字体
output_file = "dist/ali-bold.ttf"  # 基础字符集

used_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:'\"!@#$%^&*?,.;"  # 读取用到的字符
# 去重
used_chars = "".join(set(used_chars))

# 读取用到字的Unicode，通过ord()函数转一下
used_unicodes = [ord(char) for char in used_chars]

font = fontforge.open(input_file)
print("fontFamily:", font.familyname)
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

# 转成woff和woff2
# ttf_font = TTFont(output_file)
# ttf_font.flavor = "woff"
# ttf_font.save("./dist/zkhl.woff")
# ttf_font.flavor = "woff2"
# ttf_font.save("./dist/zkhl.woff2")
font.close()
