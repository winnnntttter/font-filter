from fontTools.ttLib import TTFont
ttf_font = TTFont("./dist/NotoSerifSC-Black.ttf")

ttf_font.flavor = "woff"
ttf_font.save("./dist/NotoSerifSC-Black.woff")
ttf_font.flavor = "woff2"
ttf_font.save("./dist/NotoSerifSC-Black.woff2")

