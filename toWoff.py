from fontTools.ttLib import TTFont
ttf_font = TTFont("zkhl.ttf")

ttf_font.flavor = "woff"
ttf_font.save("zkhl.woff")
ttf_font.flavor = "woff2"
ttf_font.save("zkhl.woff2")