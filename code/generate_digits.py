#!/usr/bin/env python3
"""
生成现代简洁数字字体 - 圆角风格
"""
from PIL import Image, ImageDraw

WIDTH = 20
HEIGHT = 32

def create_digit(draw_func):
    img = Image.new('L', (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(img)
    draw_func(draw)
    return img

# 使用圆角矩形和椭圆来绘制现代风格数字

def draw_0(d):
    # 椭圆形的0
    d.ellipse([3, 2, 16, 29], outline=0, width=2)

def draw_1(d):
    # 简洁的1
    d.line([(10, 2), (10, 29)], fill=0, width=2)
    d.line([(6, 7), (10, 2)], fill=0, width=2)
    d.line([(6, 29), (14, 29)], fill=0, width=2)

def draw_2(d):
    # 顶部圆弧 + 斜线 + 底部横线
    d.ellipse([3, 2, 16, 15], outline=0, width=2)
    # 只保留上半圆，用白色覆盖下半
    d.rectangle([2, 9, 17, 16], fill=255)
    d.line([(15, 9), (4, 29)], fill=0, width=2)
    d.line([(4, 29), (16, 29)], fill=0, width=2)

def draw_3(d):
    # 两个向左开口的弧 - 用椭圆+遮罩实现
    # 上半部分
    d.ellipse([3, 2, 18, 16], outline=0, width=2)
    d.rectangle([2, 2, 9, 16], fill=255)  # 遮住左边
    # 下半部分
    d.ellipse([3, 15, 18, 29], outline=0, width=2)
    d.rectangle([2, 15, 9, 30], fill=255)  # 遮住左边

def draw_4(d):
    # 简洁的4
    d.line([(13, 2), (3, 20)], fill=0, width=2)
    d.line([(3, 20), (16, 20)], fill=0, width=2)
    d.line([(13, 2), (13, 29)], fill=0, width=2)

def draw_5(d):
    # 顶横 + 左竖 + 中横 + 下半圆
    d.line([(4, 2), (16, 2)], fill=0, width=2)
    d.line([(4, 2), (4, 15)], fill=0, width=2)
    d.line([(4, 15), (11, 15)], fill=0, width=2)
    # 下半圆弧
    d.ellipse([3, 15, 18, 29], outline=0, width=2)
    d.rectangle([2, 15, 9, 22], fill=255)  # 遮住左上

def draw_6(d):
    # 上弧 + 下圆圈
    d.ellipse([3, 2, 18, 16], outline=0, width=2)
    d.rectangle([9, 2, 19, 16], fill=255)  # 只保留左边弧
    d.line([(4, 9), (4, 22)], fill=0, width=2)  # 左边竖线连接
    d.ellipse([3, 15, 16, 29], outline=0, width=2)

def draw_7(d):
    # 简洁的7
    d.line([(3, 2), (16, 2)], fill=0, width=2)
    d.line([(16, 2), (8, 29)], fill=0, width=2)

def draw_8(d):
    # 两个圆圈
    d.ellipse([3, 2, 16, 15], outline=0, width=2)
    d.ellipse([3, 14, 16, 29], outline=0, width=2)

def draw_9(d):
    # 上圆圈 + 下弧
    d.ellipse([3, 2, 16, 16], outline=0, width=2)
    d.line([(15, 9), (15, 22)], fill=0, width=2)  # 右边竖线
    d.ellipse([2, 15, 17, 29], outline=0, width=2)
    d.rectangle([2, 15, 10, 23], fill=255)  # 只保留右下弧

digits = [draw_0, draw_1, draw_2, draw_3, draw_4, draw_5, draw_6, draw_7, draw_8, draw_9]
digit_images = []

for i, func in enumerate(digits):
    img = create_digit(func)
    digit_images.append(img)

# 保存预览
preview = Image.new('L', (WIDTH * 10 + 20, HEIGHT + 10), 255)
for i, img in enumerate(digit_images):
    preview.paste(img, (i * (WIDTH + 2) + 5, 5))
preview.save("/Users/yetone/Downloads/123pan/Downloads/小程序开发环境/app_projects_extracted/app_projects/app_avatar/code/digits_preview.png")

# 生成C数组
byte_width = (WIDTH + 7) // 8
output = []
output.append(f"// 现代数字 {WIDTH}x{HEIGHT}px")
output.append(f"#define NUM_WIDTH {WIDTH}")
output.append(f"#define NUM_HEIGHT {HEIGHT}")
output.append("")
output.append(f"const unsigned char big_numbers[10][{HEIGHT * byte_width}] = {{")

for idx, img in enumerate(digit_images):
    img_1bit = img.point(lambda x: 0 if x < 128 else 255)
    pixels = list(img_1bit.getdata())
    output.append(f"    // 数字 {idx}")
    output.append("    {")
    for y in range(HEIGHT):
        row = []
        for bx in range(byte_width):
            byte_val = 0
            for bit in range(8):
                x = bx * 8 + bit
                if x < WIDTH and pixels[y * WIDTH + x] == 0:
                    byte_val |= (0x80 >> bit)
            row.append(f"0x{byte_val:02X}")
        output.append("        " + ", ".join(row) + ",")
    output.append("    }," if idx < 9 else "    }")
output.append("};")

with open("/Users/yetone/Downloads/123pan/Downloads/小程序开发环境/app_projects_extracted/app_projects/app_avatar/code/digits_new.h", "w") as f:
    f.write("\n".join(output))

print("✓ 数字完成")
