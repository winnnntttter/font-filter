from fontTools.ttLib import TTFont
ttf_font = TTFont("./dist/DingTalk-JinBuTi.ttf")

ttf_font.flavor = "woff"
ttf_font.save("./dist/DingTalk-JinBuTi.woff")
ttf_font.flavor = "woff2"
ttf_font.save("./dist/DingTalk-JinBuTi.woff2")

