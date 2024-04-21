import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='')
parser.add_argument("-v", "--visual", action="store_true", help="Visualize")
parser.add_argument("-w", "--write", type=str, help="write pixels to file")
parser.add_argument("-q", "--quiet", action="store_true", help="no print in terminal")
args = parser.parse_args()

img = cv2.imread(args.path)
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

            if args.visual == True:
                cv2.imshow("test", cv2.resize(temp_img, (320, 320)))
                cv2.waitKey(1)
        flag = not flag
    flag2 = not flag2

if args.write:
    with open(args.write, 'w') as f:
        f.write(", ".join(list(map(str, arr))))

if not args.quiet:
    print(", ".join(list(map(str, arr))))
