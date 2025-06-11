py --version   3.11.4

python --version    3.10.2
python3 --version  无反应

pip --version  pip 23.3.1 from C:\Users\Hwm\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)
pip3 --version 同上

解决办法：环境变量path中将3.11.4的上移


1、fontforge版本
直接用下面两个
fontforge -script filter-fontforge.py
<!-- pip install fontTools -->
<!-- pip install brotli -->
python toWoff.py


或者
2、fontTools版本
使用默认参数：python filter.py



指定字符集：python filter.py -c "你好世界"
从文件读取字符集：python filter.py -f characters.txt
指定输入输出文件：python filter.py -i input.ttf -o output.ttf
```
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='生成字体子集')
    parser.add_argument('--input', '-i', type=str, default="src/NotoSerifSC-Black.ttf",
                        help='输入字体文件路径')
    parser.add_argument('--output', '-o', type=str, default="dist/NotoSerifSC-Black.ttf",
                        help='输出字体文件路径')
    parser.add_argument('--chars', '-c', type=str, default=None,
                        help='要包含的字符，直接指定字符串')
    parser.add_argument('--chars-file', '-f', type=str, default=None,
                        help='要包含的字符，从文件读取')
    return parser.parse_args()

# 解析命令行参数
args = parse_args()

# 配置
input_file = args.input
output_file = args.output

# 确定要保留的字符
used_chars = ""
if args.chars:
    # 如果在命令行指定了字符
    used_chars = args.chars
elif args.chars_file:
    # 如果指定了字符文件
    try:
        with open(args.chars_file, 'r', encoding='utf-8') as f:
            used_chars = f.read()
    except Exception as e:
        print(f"读取字符文件时出错: {e}")
        used_chars = "如何结合国家战略及区域发展选专业？"  # 使用默认字符
else:
    # 如果没有指定，使用默认字符
    # used_chars = "如何结合国家战略及区域发展选专业？"
    used_chars = "教育部供需对接就业育人项目"
```
