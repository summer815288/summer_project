from lxml import etree
import pytesseract
from PIL import Image
import tesserocr
from PIL import Image
import time, string, os
from scipy import spatial

with open('/Users/edz/Documents/pongo/python_test/code/amazon_detail.html') as f:
    # readline()每一次读取一行数据，并指向该行末尾
    body = f.readline().rstrip()  # 读取第一行数据（此时已经指向第一行末尾）
    tree = etree.HTML(body)
    src = tree.xpath('.//div[@class="a-row a-text-center"]/img/@src')
    if src:
        src = src[0]
        # image = Image.open('/Users/edz/Documents/pongo/python_test/code/1.jpg')
        # text = pytesseract.image_to_string(image, lang='eng', config='--psm 9 ')  # 使用简体中文解析图片
        # print(111)
        # print(text)


def get_x_coord(image) -> '返回切割的x坐标':
    image_width = image.size[0]
    image_height = image.size[1]

    crop_list = []
    start_pos = 0
    is_start_one_char = False

    for x in range(image_width):
        is_black_pos = False
        for y in range(image_height):
            pixel = image.getpixel((x, y))
            if pixel == 0:
                if is_start_one_char == False:
                    start_pos = x
                is_black_pos = True
                is_start_one_char = True
                break
        if is_start_one_char == True and is_black_pos == False:
            end_pos = x
            is_start_one_char = False
            crop_list.append((start_pos, end_pos))

    return crop_list


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        # print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False


image = Image.open('/Users/edz/Documents/pongo/python_test/code/1.jpg')
# result = tesserocr.image_to_text(image)
# print(result)

im = image

im = im.convert('P')

im_size = im.size

new_im = Image.new('P', im_size, 255)

im_width = im_size[0]
im_height = im_size[1]

for y in range(im_height):
    for x in range(im_width):
        pixel = im.getpixel((x, y))
        if pixel == 0:
            new_im.putpixel((x, y), pixel)
print(new_im)
match_captcha = []
crop_list = get_x_coord(image)
print(111)
print(crop_list)
for crop in crop_list:
    crop_im = new_im.crop((crop[0], 0, crop[1], im_height))  # （左上x， 左上y， 右下x， 右下y）
    filename = '/Users/edz/Documents/pongo/python_test/code/crop/' + str(time.time()) + '.gif'
    crop_im.save(filename)

    all_result = []  # 单个切片的所有字母的相似性

    remove_letter = ['d', 'i', 'o', 'q', 's', 'v', 'w', 'z']

    for letter in list(set(string.ascii_lowercase) - set(remove_letter)):

        refer_image_dir = r'/Users/edz/Documents/pongo/python_test/code/training_library/%s' % letter
        mkdir(refer_image_dir)
        print('xixi')
        print(os.listdir(refer_image_dir))
        for refer_image in os.listdir(refer_image_dir):
            print(333)
            print(os.path.join(refer_image_dir, refer_image))
            print(refer_image)
            refer_im = image.open(os.path.join(refer_image_dir, refer_image))

            crop_list = list(crop_im.getdata())
            refer_list = list(refer_im.getdata())
            min_count = min(len(crop_list), len(refer_list))

            result = 1 - spatial.distance.cosine(crop_list[:min_count - 1], refer_list[:min_count - 1])
            all_result.append({'letter': letter, 'result': result})

    print(111)
    print(all_result)
    if len(all_result)>0:
        match_letter = max(all_result, key=lambda x: x['result']).get('letter')

        match_captcha.append(match_letter)

print('验证码为：{0}'.format(''.join(match_captcha)))
