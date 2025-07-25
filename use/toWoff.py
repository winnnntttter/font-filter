from fontTools.ttLib import TTFont
ttf_font = TTFont("./dist/simkai.ttf")

ttf_font.flavor = "woff"
ttf_font.save("./dist/simkai.woff")
ttf_font.flavor = "woff2"
ttf_font.save("./dist/simkai.woff2")

