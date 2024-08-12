from fontTools.ttLib import TTFont
ttf_font = TTFont("./dist/SourceHanSerifCN-Regular.ttf")

ttf_font.flavor = "woff"
ttf_font.save("./dist/SourceHanSerifCN-Regular.woff")
ttf_font.flavor = "woff2"
ttf_font.save("./dist/SourceHanSerifCN-Regular.woff2")

