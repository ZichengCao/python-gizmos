"""
@Description :   用 Python 实现朋友圈中的九宫格图片

效果：
选择一张图片，选择输出文件夹，程序将一张图片均匀的切分成9份。
在微信朋友圈依次选择9张图片，发出去后别人将看到一张巨大的图片。

原理：
1. 读取图片，基于如cv2、PIL、matplotlib等库
3. 将图片使用横向和纵向均匀切分9份
4. 分别将每一份保存为单独的图片

@Author      :   Evan
@Time        :   2024/02/27 10:49:16
@Version     :   1.0
"""
from PIL import Image
import os
# 定义函数，用于将输入的图片切分成9份
def split_image(image_path, output_folder):
    # 打开输入的图片
    img = Image.open(image_path)
    # 获取图片的宽度和高度
    width, height = img.size
    # 计算每份图片的宽度和高度
    box_width = width // 3
    box_height = height // 3

    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 循环切分图片为9份
    for i in range(3):
        for j in range(3):
            # 计算切分区域的坐标
            box = (j * box_width, i * box_height, (j + 1) * box_width, (i + 1) * box_height)
            # 切分图片并保存为单独的图片
            region = img.crop(box)
            region.save(f"{output_folder}/image_{i}_{j}.png")

# 定义函数，用于将切分后的9张图片合并成一张完整的图片
def combine_images(input_folder, output_path):
    images = []
    # 循环读取切分后的9张图片
    for i in range(3):
        row_images = []
        for j in range(3):
            # 读取单张切分后的图片
            image_path = f"{input_folder}/image_{i}_{j}.png"
            img = Image.open(image_path)
            row_images.append(img)
        images.append(row_images)

    # 计算合并后图片的宽度和高度
    box_width = images[0][0].width
    box_height = images[0][0].height
    width = box_width * 3
    height = box_height * 3

    # 创建新的图片对象
    new_img = Image.new("RGB", (width, height))

    # 循环将切分后的图片合并成一张完整的图片
    for i in range(3):
        for j in range(3):
            new_img.paste(images[i][j], (j * box_width, i * box_height))

    # 保存合并后的图片
    new_img.save(output_path)
if __name__ == "__main__":
    image_path = "input_image.jpg"
    output_folder = "output_images"
    split_image(image_path, output_folder)
    
    # 调用函数并传入切分后的图片文件夹路径和输出合并后的图片路径
    combine_images(output_folder, "combined_image.jpg")


