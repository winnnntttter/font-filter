#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 主脚本，用于运行整个字体分割和生成流程

import os
import sys
import subprocess

# 工作目录设置为脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 确保dist目录存在
if not os.path.exists("dist"):
    os.makedirs("dist")

# 定义执行脚本的函数
def run_script(script_name):
    print(f"执行 {script_name}...")
    result = subprocess.run([sys.executable, script_name], check=True)
    if result.returncode != 0:
        print(f"执行 {script_name} 失败！")
        sys.exit(1)
    print(f"{script_name} 执行完成\n")

# 按顺序执行所有脚本
try:
    # 步骤1：分割字体
    run_script("split_font.py")

    # 步骤2：转换为WOFF和WOFF2格式
    run_script("to_woff.py")

    # 步骤3：生成CSS文件
    run_script("generate_css.py")

    print("="*50)
    print("所有处理完成！字体分割和文件生成已成功。")
    print(f"生成的文件位于 {os.path.abspath('dist')} 目录")
    print("="*50)

except Exception as e:
    print(f"错误：{e}")
    sys.exit(1)
