from fontTools.ttLib import TTFont
ttf_font = TTFont("./dist/ysbth.ttf")

ttf_font.flavor = "woff"
ttf_font.save("./dist/ysbth.woff")
ttf_font.flavor = "woff2"
ttf_font.save("./dist/ysbth.woff2")

