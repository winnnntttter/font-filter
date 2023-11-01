from fontTools.ttLib import TTFont
ttf_font = TTFont("./dist/zkhl.ttf")

ttf_font.flavor = "woff"
ttf_font.save("./dist/zkhl.woff")
ttf_font.flavor = "woff2"
ttf_font.save("./dist/zkhl.woff2")
print("转换完成")