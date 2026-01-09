import os
# from fontTools.ttLib import TTFont

# input_file = "src/AlibabaPuHuiTi-3-85-Bold.ttf"  # 全量字体
# output_file = "dist/ali-bold.ttf"  # 基础字符集

# input_file = "src/AlibabaPuHuiTi-3-55-Regular.ttf"  # 全量字体
input_file = "src/AlibabaPuHuiTi-3-55-RegularL3.ttf"  # 全量字体
output_file = "dist/ali.ttf"  # 基础字符集

used_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:'\"!@#$%^&*?,.;"  # 读取用到的字符
# 去重
used_chars = "".join(set(used_chars))

# 读取用到字的Unicode，通过ord()函数转一下
used_unicodes = [ord(char) for char in used_chars]

font = fontforge.open(input_file)
print("fontFamily:", font.familyname)

# 添加调试：查看字体包含哪些字符
print("=" * 50)
print("检查字体中是否包含所需字符:")
matched_count = 0
total_glyphs = 0
for char_name in font:
    glyph = font[char_name]
    unicode = glyph.unicode
    total_glyphs += 1
    if unicode != -1 and unicode in used_unicodes:
        matched_count += 1
        print(f"找到匹配字符: {chr(unicode)} (U+{unicode:04X})")

print(f"总字形数: {total_glyphs}")
print(f"匹配字符数: {matched_count}")
print("=" * 50)

# 如果没有匹配的字符，不进行过滤
if matched_count == 0:
    print("警告：字体中不包含任何所需字符！")
    print("L3版本可能只包含中文字符，请使用完整版字体")
    font.close()
    import sys
    sys.exit(1)

# 开始过滤
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
