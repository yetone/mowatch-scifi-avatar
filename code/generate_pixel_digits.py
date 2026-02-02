#!/usr/bin/env python3
"""
生成像素点阵风格数字 (8-bit 复古风格)
20x32 像素，适合 MoWatch e-ink 显示
"""

from PIL import Image, ImageDraw

# 数字尺寸
WIDTH = 20
HEIGHT = 32

# 像素块大小 (每个"大像素"由多少实际像素组成)
PIXEL_SIZE = 4

def create_pixel_digit(pattern):
    """根据模式创建像素数字图像"""
    img = Image.new('1', (WIDTH, HEIGHT), 1)  # 1 = 白色背景
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(pattern):
        for x, pixel in enumerate(row):
            if pixel == 1:
                # 绘制一个大像素块
                x0 = x * PIXEL_SIZE
                y0 = y * PIXEL_SIZE
                x1 = x0 + PIXEL_SIZE - 1
                y1 = y0 + PIXEL_SIZE - 1
                draw.rectangle([x0, y0, x1, y1], fill=0)  # 0 = 黑色

    return img

# 5x8 的像素点阵模式 (会被放大到 20x32)
PIXEL_PATTERNS = {
    0: [
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
    ],
    1: [
        [0, 0, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1],
    ],
    2: [
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    3: [
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
    ],
    4: [
        [0, 0, 0, 1, 1],
        [0, 0, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ],
    5: [
        [1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
    ],
    6: [
        [0, 1, 1, 1, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
    ],
    7: [
        [1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0],
    ],
    8: [
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
    ],
    9: [
        [0, 1, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0],
    ],
}

def image_to_c_array(img, digit):
    """将图像转换为 C 数组"""
    width, height = img.size
    pixels = list(img.getdata())
    byte_width = (width + 7) // 8  # = 3 for 20px

    data = []
    for y in range(height):
        for bx in range(byte_width):
            byte = 0
            for bit in range(8):
                x = bx * 8 + bit
                if x < width:
                    idx = y * width + x
                    if pixels[idx] == 0:  # 黑色像素
                        byte |= (128 >> bit)
            data.append(byte)

    return data

def main():
    print("// 像素点阵风格数字 20x32px (8-bit 复古风格)")
    print("#define NUM_WIDTH 20")
    print("#define NUM_HEIGHT 32")
    print("")
    print("const unsigned char big_numbers[10][96] = {")

    for digit in range(10):
        img = create_pixel_digit(PIXEL_PATTERNS[digit])

        # 保存预览
        img.save(f"digit_{digit}_preview.png")

        # 转换为 C 数组
        data = image_to_c_array(img, digit)

        print(f"    // 数字 {digit}")
        print("    {")
        for i in range(0, len(data), 3):
            chunk = data[i:i+3]
            line = "        " + ", ".join(f"0x{b:02X}" for b in chunk) + ","
            print(line)
        print("    },")

    print("};")

    # 创建预览图
    preview = Image.new('1', (WIDTH * 10 + 20, HEIGHT + 10), 1)
    for digit in range(10):
        img = create_pixel_digit(PIXEL_PATTERNS[digit])
        preview.paste(img, (5 + digit * (WIDTH + 2), 5))
    preview.save("digits_preview.png")
    print("\n// 预览图已保存到 digits_preview.png", file=__import__('sys').stderr)

if __name__ == "__main__":
    main()
