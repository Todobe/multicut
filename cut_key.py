import cv2
import numpy as np
import os
import sys


def in_box(pos, left_up_corner, rec_shape):
    return left_up_corner[0] <= pos[0] <= left_up_corner[0] + rec_shape[0] and left_up_corner[1] <= pos[1] <= \
           left_up_corner[1] + rec_shape[1]


def main():
    img1 = cv2.imread("data/HR.png")
    img2 = cv2.imread("data/baseline.png")
    files = sys.argv[1:]
    if len(files) <= 0:
        print("Please specify file path.")
        exit(0)

    data = {}
    data['name'] = []
    imgs = []
    for file in files:
        imgs.append(cv2.imread(file))
        data['name'].append(os.path.basename(file))

    data['pos'] = [(0, 0)]
    for i in range(1, len(imgs)):
        imgs[i] = cv2.resize(imgs[i], (imgs[0].shape[1], imgs[0].shape[0]))
        data['pos'].append((img1.shape[1]*i, 0))

    print("img size:", imgs[0].shape)
    cv2.namedWindow('multicut', cv2.WINDOW_AUTOSIZE)

    img = np.hstack(imgs)
    cv2.imshow("multicut", img)
    cv2.waitKey(10)

    data['origin'] = img
    data['shape'] = (imgs[0].shape[1], imgs[0].shape[0])
    data['lu_corner'] = (-1, -1)
    data['rd_corner'] = (-1, -1)

    while True:
        line = input("left up right down:")
        pos = line.split(' ')
        if len(pos) == 1 and pos[0]=='0':
            exit(0)
        if len(pos) != 4:
            print("Format wrong.")
        data['lu_corner'] = (int(pos[0]), int(pos[1]))
        data['rd_corner'] = (int(pos[2]), int(pos[3]))
        if not (in_box(data['lu_corner'], (0, 0), data['shape']) and in_box(data['rd_corner'],(0,0),data['shape'])):
            print("out of range, image shape:", data['shape'][0], data['shape'][1])
            continue

        data['img'] = data['origin'].copy()
        for pos in data['pos']:
            cv2.rectangle(data['img'], (pos[0] + data['lu_corner'][0], pos[1] + data['lu_corner'][1]),
                          (pos[0] + data['rd_corner'][0], pos[1] + data['rd_corner'][1]), (0, 0, 255), 2)
        cv2.imshow('multicut', data['img'])
        cv2.waitKey(10)
        line = input("save?(y/n)")
        if line[0]=='y':
            lu = (min(data['lu_corner'][0], data['rd_corner'][0]), min(data['lu_corner'][1], data['rd_corner'][1]))
            rd = (max(data['lu_corner'][0], data['rd_corner'][0]), max(data['lu_corner'][1], data['rd_corner'][1]))
            print(lu, rd)
            for pos, filename in zip(data['pos'], data['name']):
                tmp = data['origin'][pos[1] + lu[1]:pos[1] + rd[1], pos[0] + lu[0]:pos[0] + rd[0]]
                cv2.imwrite(os.path.join("output", "cut_" + filename), tmp)


if __name__ == "__main__":
    main()


