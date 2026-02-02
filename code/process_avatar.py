#!/usr/bin/env python3
"""
处理动漫头像 - 区分头发和眼睛
头发：暖棕色 R>>G>>B
眼睛：灰黑色 R≈G≈B
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

enhanced = ImageEnhance.Contrast(img).enhance(1.4)
gray = enhanced.convert('L')

edges = gray.filter(ImageFilter.FIND_EDGES)
edges_strong = gray.filter(ImageFilter.Kernel((3, 3), [-1, -1, -1, -1, 8, -1, -1, -1, -1], 1, 0))

pixels = list(img.getdata())
gray_pixels = list(gray.getdata())
edge_pixels = list(edges.getdata())
edge_strong_pixels = list(edges_strong.getdata())

def get_rgb(x, y):
    if 0 <= x < OUTPUT_SIZE and 0 <= y < OUTPUT_SIZE:
        return pixels[y * OUTPUT_SIZE + x]
    return (0, 0, 255)

def get_lum(x, y):
    if 0 <= x < OUTPUT_SIZE and 0 <= y < OUTPUT_SIZE:
        return gray_pixels[y * OUTPUT_SIZE + x]
    return 255

def is_blue_bg(r, g, b):
    return b > 180 and r < 100 and b > r + 80

def is_skin(r, g, b, lum):
    return lum > 200 and r > 230 and g > 200 and b > 180

def is_hair(r, g, b, lum):
    """头发：暖棕色，R > G > B，差异大"""
    if lum > 80:
        return False
    # 头发特征：R明显大于B，颜色偏暖
    r_minus_b = r - b
    r_minus_g = r - g
    return r_minus_b > 15 and r_minus_g > 5 and lum < 70

def is_eye_dark(r, g, b, lum):
    """眼睛深色部分：灰黑色，R≈G≈B"""
    if lum > 100 or lum < 20:
        return False
    # 眼睛特征：RGB接近，偏灰
    diff_rg = abs(r - g)
    diff_gb = abs(g - b)
    diff_rb = abs(r - b)
    max_diff = max(diff_rg, diff_gb, diff_rb)
    return max_diff < 25 and lum < 90

def is_eyebrow(r, g, b, lum):
    """眉毛：比眼睛稍深，也是灰黑色"""
    if lum > 60:
        return False
    diff = max(r, g, b) - min(r, g, b)
    return diff < 20 and lum < 50

def near_skin(x, y, radius=5):
    """检查周围是否有皮肤（用于判断是否在脸部）"""
    for dy in range(-radius, radius + 1, 2):
        for dx in range(-radius, radius + 1, 2):
            r, g, b = get_rgb(x + dx, y + dy)
            lum = get_lum(x + dx, y + dy)
            if is_skin(r, g, b, lum):
                return True
    return False

def near_bg_or_hair(x, y, radius=4):
    """检查周围是否有背景或头发"""
    for dy in range(-radius, radius + 1, 2):
        for dx in range(-radius, radius + 1, 2):
            r, g, b = get_rgb(x + dx, y + dy)
            lum = get_lum(x + dx, y + dy)
            if is_blue_bg(r, g, b) or is_hair(r, g, b, lum):
                return True
    return False

# 生成结果
result_pixels = []

for i in range(OUTPUT_SIZE * OUTPUT_SIZE):
    y = i // OUTPUT_SIZE
    x = i % OUTPUT_SIZE
    r, g, b = pixels[i]
    lum = gray_pixels[i]
    edge = max(edge_pixels[i], edge_strong_pixels[i])

    # 1. 蓝色背景 -> 白色
    if is_blue_bg(r, g, b):
        result_pixels.append(255)
        continue

    # 2. 头发（暖棕色）-> 黑色
    if is_hair(r, g, b, lum):
        result_pixels.append(0)
        continue

    # 3. 眉毛 -> 黑色
    if is_eyebrow(r, g, b, lum):
        result_pixels.append(0)
        continue

    # 4. 眼睛深色部分（灰黑色，在脸部附近）
    if is_eye_dark(r, g, b, lum):
        # 确认在脸部区域
        if near_skin(x, y):
            # 只画眼睛轮廓，中间留白让眼睛清澈
            if edge > 30 or lum < 50:
                result_pixels.append(0)
            else:
                result_pixels.append(255)
        else:
            # 不在脸部，可能是其他深色区域
            result_pixels.append(0)
        continue

    # 5. 皮肤区域
    if is_skin(r, g, b, lum):
        # 脸部轮廓
        if near_bg_or_hair(x, y) and edge > 20:
            result_pixels.append(0)
        # 面部强边缘
        elif edge > 60:
            result_pixels.append(0)
        else:
            result_pixels.append(255)
        continue

    # 6. 非常深的区域
    if lum < 50:
        result_pixels.append(0)
        continue

    # 7. 中等深度区域 + 边缘
    if lum < 120 and edge > 40:
        result_pixels.append(0)
        continue

    # 8. 其他边缘
    if edge > 50:
        result_pixels.append(0)
    else:
        result_pixels.append(255)

# 创建结果图像
result = Image.new('L', (OUTPUT_SIZE, OUTPUT_SIZE))
result.putdata(result_pixels)
result.save("/Users/yetone/Downloads/123pan/Downloads/小程序开发环境/app_projects_extracted/app_projects/app_avatar/code/avatar_preview.png")

# 生成C数组
pixels_1bit = list(result.getdata())
byte_width = (OUTPUT_SIZE + 7) // 8

lines = ["// 头像 120x120px", f"const unsigned char avatar_face[{OUTPUT_SIZE * byte_width}] = {{"]
for row_y in range(OUTPUT_SIZE):
    row = []
    for bx in range(byte_width):
        byte_val = 0
        for bit in range(8):
            px = bx * 8 + bit
            if px < OUTPUT_SIZE and pixels_1bit[row_y * OUTPUT_SIZE + px] == 0:
                byte_val |= (0x80 >> bit)
        row.append(f"0x{byte_val:02X}")
    lines.append("    " + ", ".join(row) + ("," if row_y < OUTPUT_SIZE - 1 else ""))
lines.append("};")

with open("/Users/yetone/Downloads/123pan/Downloads/小程序开发环境/app_projects_extracted/app_projects/app_avatar/code/avatar_new.h", "w") as f:
    f.write("\n".join(lines))

print("✓ 完成 - 头发/眼睛已区分")
