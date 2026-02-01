#!/usr/bin/env python3
"""
科幻HUD风格方形表盘背景
Cyberpunk/Sci-Fi Dashboard Style
"""
from PIL import Image, ImageDraw
import math
import random

random.seed(42)

WIDTH = HEIGHT = 200
img = Image.new('L', (WIDTH, HEIGHT), 255)
draw = ImageDraw.Draw(img)

BLACK = 0
GRAY = 128
LIGHT_GRAY = 192

# ============ 科幻HUD设计 ============

# 1. 外边框 - 双层技术感边框
draw.rectangle([0, 0, 199, 199], outline=BLACK, width=2)
draw.rectangle([4, 4, 195, 195], outline=GRAY)

# 2. 角落装饰 - 切角效果
corner_size = 15
corners = [
    # 左上
    [(0, corner_size), (0, 0), (corner_size, 0)],
    # 右上
    [(199-corner_size, 0), (199, 0), (199, corner_size)],
    # 左下
    [(0, 199-corner_size), (0, 199), (corner_size, 199)],
    # 右下
    [(199-corner_size, 199), (199, 199), (199, 199-corner_size)],
]
for pts in corners:
    draw.line(pts, fill=BLACK, width=2)

# 3. 顶部状态栏区域
draw.line([(8, 18), (192, 18)], fill=GRAY)
# 顶部小刻度
for i in range(10):
    x = 20 + i * 18
    draw.line([(x, 14), (x, 18)], fill=BLACK if i % 3 == 0 else GRAY)

# 4. 左侧数据面板区域
draw.rectangle([6, 24, 45, 95], outline=GRAY)
# 左侧小格子
for i in range(5):
    y = 30 + i * 13
    draw.line([(8, y), (43, y)], fill=LIGHT_GRAY)
# 左侧标签区
draw.rectangle([8, 26, 43, 36], outline=BLACK)

# 5. 右侧数据面板区域
draw.rectangle([154, 24, 193, 95], outline=GRAY)
# 右侧小格子
for i in range(5):
    y = 30 + i * 13
    draw.line([(156, y), (191, y)], fill=LIGHT_GRAY)
# 右侧标签区
draw.rectangle([156, 26, 191, 36], outline=BLACK)

# 6. 中央头像区域框
draw.rectangle([50, 22, 149, 98], outline=BLACK)
draw.rectangle([52, 24, 147, 96], outline=GRAY)

# 7. 中央分隔线
draw.line([(8, 100), (192, 100)], fill=BLACK)
# 分隔线装饰
draw.polygon([(95, 97), (100, 93), (105, 97), (100, 100)], fill=BLACK)
draw.polygon([(95, 103), (100, 107), (105, 103), (100, 100)], fill=BLACK)

# 8. 时间显示区域
draw.rectangle([8, 104, 192, 148], outline=BLACK)
# 时间区域内部装饰线
draw.line([(10, 130), (50, 130)], fill=GRAY)
draw.line([(150, 130), (190, 130)], fill=GRAY)

# 9. 底部数据区域 - 多个小面板
# 日期面板
draw.rectangle([8, 152, 70, 172], outline=GRAY)
draw.line([(10, 154), (68, 154)], fill=BLACK)

# 状态面板
draw.rectangle([74, 152, 126, 172], outline=GRAY)
draw.line([(76, 154), (124, 154)], fill=BLACK)

# 电量面板
draw.rectangle([130, 152, 192, 172], outline=GRAY)
draw.line([(132, 154), (190, 154)], fill=BLACK)

# 10. 最底部信息栏
draw.line([(8, 176), (192, 176)], fill=GRAY)
# 底部装饰点
for i in range(20):
    x = 15 + i * 9
    if i % 4 == 0:
        draw.ellipse([x-1, 178, x+1, 180], fill=BLACK)
    else:
        draw.point((x, 179), fill=GRAY)

# 11. 科幻装饰元素
# 左上角信号图标区
draw.line([(10, 8), (10, 14)], fill=BLACK)
draw.line([(14, 10), (14, 14)], fill=BLACK)
draw.line([(18, 6), (18, 14)], fill=BLACK)

# 右上角指示灯
for i in range(3):
    x = 178 + i * 7
    draw.ellipse([x, 8, x+4, 12], outline=BLACK)

# 12. 网格装饰 - 在空白区域添加细网格
# 左侧面板网格
for i in range(4):
    for j in range(3):
        x = 12 + j * 10
        y = 42 + i * 12
        draw.point((x, y), fill=LIGHT_GRAY)

# 右侧面板网格
for i in range(4):
    for j in range(3):
        x = 160 + j * 10
        y = 42 + i * 12
        draw.point((x, y), fill=LIGHT_GRAY)

# 13. 扫描线效果 - 底部
for i in range(5):
    y = 184 + i * 3
    alpha = GRAY if i % 2 == 0 else LIGHT_GRAY
    draw.line([(20 + i*5, y), (180 - i*5, y)], fill=alpha)

# 14. 数据流装饰 - 侧边
for i in range(8):
    y = 105 + i * 5
    w = random.randint(3, 12)
    draw.line([(10, y), (10 + w, y)], fill=GRAY)
    w = random.randint(3, 12)
    draw.line([(189 - w, y), (189, y)], fill=GRAY)

# ============ 输出 ============
img_1bit = img.convert('1')
pixels = list(img_1bit.getdata())
byte_width = (WIDTH + 7) // 8

output = ["// 科幻HUD风格背景 200x200px", f"const unsigned char background[{HEIGHT * byte_width}] = {{"]
for y in range(HEIGHT):
    row = []
    for bx in range(byte_width):
        byte_val = 0
        for bit in range(8):
            x = bx * 8 + bit
            if x < WIDTH and pixels[y * WIDTH + x] == 0:
                byte_val |= (0x80 >> bit)
        row.append(f"0x{byte_val:02X}")
    output.append("    " + ", ".join(row) + ("," if y < HEIGHT-1 else ""))
output.append("};")

with open("background.h", "w") as f:
    f.write("#ifndef BACKGROUND_H\n#define BACKGROUND_H\n\n" + "\n".join(output) + "\n\n#endif\n")

print("✓ 科幻HUD背景完成")
img.save("background_preview.png")
