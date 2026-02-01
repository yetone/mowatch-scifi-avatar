#!/usr/bin/env python3
"""
处理头像 - 干净的面部内部，保留脸部轮廓
"""
from PIL import Image, ImageFilter, ImageEnhance

INPUT_IMAGE = "/Users/yetone/Downloads/avatar.jpg"
OUTPUT_SIZE = 120

# 加载并预处理
img = Image.open(INPUT_IMAGE).convert('RGB')
w, h = img.size
size = min(w, h)
img = img.crop(((w-size)//2, (h-size)//2, (w+size)//2, (h+size)//2))
img = img.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)

# 增强对比度
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.3)

pixels = list(img.getdata())
gray = img.convert('L')

# 边缘检测
edges = gray.filter(ImageFilter.FIND_EDGES)
edges = edges.point(lambda x: 255 if x > 35 else 0)
edge_pixels = list(edges.getdata())
gray_pixels = list(gray.getdata())

def is_skin_color(r, g, b):
    return (r > 170 and g > 130 and b > 110 and r > b and r > g - 40)

def is_blue_bg(r, g, b):
    return (b > 180 and r < 80 and g < 180 and b > r + 100)

def get_pixel(x, y):
    if 0 <= x < OUTPUT_SIZE and 0 <= y < OUTPUT_SIZE:
        return pixels[y * OUTPUT_SIZE + x]
    return (0, 0, 255)  # 边界外当作蓝色背景

def has_non_skin_neighbor(x, y):
    """检查周围是否有非皮肤色像素（背景或头发）"""
    for dy in [-2, -1, 0, 1, 2]:
        for dx in [-2, -1, 0, 1, 2]:
            if dx == 0 and dy == 0:
                continue
            r, g, b = get_pixel(x + dx, y + dy)
            if is_blue_bg(r, g, b) or gray_pixels[max(0, min((y+dy)*OUTPUT_SIZE + (x+dx), OUTPUT_SIZE*OUTPUT_SIZE-1))] < 100:
                return True
    return False

# 生成结果
result_pixels = []

for i in range(OUTPUT_SIZE * OUTPUT_SIZE):
    y = i // OUTPUT_SIZE
    x = i % OUTPUT_SIZE
    r, g, b = pixels[i]
    lum = gray_pixels[i]
    edge = edge_pixels[i]

    if is_blue_bg(r, g, b):
        result_pixels.append(255)
    elif is_skin_color(r, g, b):
        # 皮肤区域：只在边缘且有非皮肤邻居时显示边缘（脸部轮廓）
        if edge > 128 and has_non_skin_neighbor(x, y):
            result_pixels.append(0)
        else:
            result_pixels.append(255)
    elif edge > 128:
        result_pixels.append(0)
    elif lum < 100:
        result_pixels.append(0)
    else:
        result_pixels.append(255)

result = Image.new('L', (OUTPUT_SIZE, OUTPUT_SIZE))
result.putdata(result_pixels)

# 保存预览
result.save("/Users/yetone/Downloads/123pan/Downloads/小程序开发环境/app_projects_extracted/app_projects/app_avatar/code/avatar_preview.png")

# 生成C数组
pixels_1bit = list(result.getdata())
byte_width = (OUTPUT_SIZE + 7) // 8

lines = ["// 头像 120x120px", f"const unsigned char avatar_face[{OUTPUT_SIZE * byte_width}] = {{"]
for y in range(OUTPUT_SIZE):
    row = []
    for bx in range(byte_width):
        byte_val = 0
        for bit in range(8):
            x = bx * 8 + bit
            if x < OUTPUT_SIZE and pixels_1bit[y * OUTPUT_SIZE + x] == 0:
                byte_val |= (0x80 >> bit)
        row.append(f"0x{byte_val:02X}")
    lines.append("    " + ", ".join(row) + ("," if y < OUTPUT_SIZE - 1 else ""))
lines.append("};")

with open("/Users/yetone/Downloads/123pan/Downloads/小程序开发环境/app_projects_extracted/app_projects/app_avatar/code/avatar_new.h", "w") as f:
    f.write("\n".join(lines))

print("✓ 头像完成")
