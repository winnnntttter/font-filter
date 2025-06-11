import os
# from fontTools.ttLib import TTFont

input_file = "src/ysbth.ttf"  # 全量字体
output_file = "dist/ysbth.ttf"  # 提取后的字体

used_chars = "如何结合国家战略及区域发展选专业？"  # 读取用到的字符

# unicode \u2F6C或者\u2F6D的也保留
# used_chars += "\u2F6C\u319F"

# 去重
used_chars = "".join(set(used_chars))

# 读取用到字的Unicode，通过ord()函数转一下
used_unicodes = [ord(char) for char in used_chars]

font = fontforge.open(input_file)
print("fontFamily:", font.familyname)
for char_name in font:
    glyph = font[char_name]
    unicode = glyph.unicode
    alt_unicodes = [alt[0] for alt in glyph.altuni] if glyph.altuni else []
    all_unicodes = [unicode] + alt_unicodes
    if any(unicode in used_unicodes for unicode in all_unicodes):
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



""" Unicode字符\u2F6C和\u76EE分别对应的是“⽬”和“目”。其中：

\u2F6C 是一个康熙部首字符，表示“目”部首。
\u76EE 是一个常用汉字，表示“目”。
在某些字体（如思源宋体）中，这两个字符可能会被设计成相同或非常相似的形状，因为它们在视觉上代表相同的概念，即“目”。这种设计选择是为了在字体中保持一致性和美观。 """