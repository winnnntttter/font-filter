import os
# from fontTools.ttLib import TTFont

input_file = "src/zkhl.TTF"  # 全量字体
output_file = "zkhl.ttf"  # 基础字符集

used_chars = "已经超棒啦！继续保持活跃，发布职位、及时处理简历、参加招聘会、丰富企业简介都能进一步提升你的招聘效果。拥有一个正式清晰的Logo代表这个企业有一个好的形象，看起来也会更正规，求职者会更加信任。丰富企业简介，让求职者更深入了解你的公司。多添加福利标签，会吸引更多求职者哦。排名优先、职位一键刷新，让你的职位排在众多竞争者的前面，让更优秀的人才第一眼看到你的职位。更多会员功能请点击链接降低任职要求，提高薪资福利也是拉拢人才的必要手段，谁愿意看要求又多薪资又少的职位呢？职位收到的简历少，很有可能是职位描述不清晰，导致人才无法判断自己适不适合这个职位。尝试把岗位职责、任职要求、薪资福利写清楚再试试呢！每周每个职位会推荐10封简历，按照职位精准匹配人才并推送简历，这样还会发愁收不到简历？办个国家大学生就业服务平台会员即刻拥有。求职人才往往比较注重自己未来的工作环境，尝试把公司简介描述的详细一些，把公司最好的一面展现给大家会使你招聘人才事半功倍。简历处理速度慢很容易错过优秀的求职者，建议在招聘量大时早晚各登录一次国家大学生就业服务平台，查看最新投递来的简历并及时给予反馈。求职者更青睐于处理简历速度快的企业，不浪费彼此时间，给对方更好的选择余地。养成每天登录国家大学生就业服务平台的习惯，查看最新简历；完善职位信息；加入网络招聘会，招聘人才也很简单。"  # 读取用到的字符
# 去重
used_chars = "".join(set(used_chars))

# 读取用到字的Unicode，通过ord()函数转一下
used_unicodes = [ord(char) for char in used_chars]

font = fontforge.open(input_file)
print(font.familyname)
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
# ttf_font.save("zkhl.woff")
# ttf_font.flavor = "woff2"
# ttf_font.save("zkhl.woff2")
font.close()
