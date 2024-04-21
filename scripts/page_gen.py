import argparse
import os

import cv2


def generate_pixels(img_path):
    img = cv2.imread(img_path)
    temp_img = img.copy()

    flag = True
    flag2 = True

    arr = []

    for k in range(4):
        flag = flag2
        if flag2:
            start1, finish1, step1 = 0, 32, 1
        else:
            start1, finish1, step1 = 31, -1, -1
        for j in range(start1, finish1, step1):
            for i in range(k * 8, (k + 1) * 8, 1):

                if flag:
                    color = img[i, j][::-1]  # Reverse the order of BGR to RGB
                    temp_img[i, j] = 0
                else:
                    color = img[((k + 1) * 8) - (i - k * 8) - 1, j][::-1]
                    temp_img[((k + 1) * 8) - (i - k * 8) - 1, j] = 0

                html = "0x{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                arr.append(html)

            flag = not flag
        flag2 = not flag2

        return ", ".join(list(map(str, arr)))


parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, nargs='+', help='')
parser.add_argument("-d", "--delay", type=int, help="delay between images", default=1000)
parser.add_argument("-f", "--file", type=str, help="output file name", default="matrix_image.txt")
args = parser.parse_args()

with open(args.file, "w") as f:
    f.write(str(len(args.path)) + '\n')
    f.write(str(args.delay) + '\n')
    for path in args.path:
        f.write(generate_pixels(path) + '\n')
