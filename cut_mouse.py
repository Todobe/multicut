import cv2
import numpy as np
import os
import sys



def in_box(pos, left_up_corner, rec_shape):
    return left_up_corner[0] <= pos[0] <= left_up_corner[0] + rec_shape[0] and left_up_corner[1] <= pos[1] <= \
           left_up_corner[1] + rec_shape[1]


def mouse_handler(event, x, y, flags, data):
    if event == cv2.EVENT_LBUTTONDOWN:
        data['lu_corner'] = (-1, -1)
        data['img'] = data['origin'].copy()
        for pos in data['pos']:
            if in_box((x, y), pos, data['shape']):
                data['lu_corner'] = (x-pos[0], y-pos[1])
                break
        if data['lu_corner'] != (-1,-1):
            for pos in data['pos']:
                cv2.circle(data['img'], (pos[0]+data['lu_corner'][0],pos[1]+data['lu_corner'][1]), 3, (0, 0, 255), 5, 16)
        cv2.imshow('multicut', data['img'])
    elif event == cv2.EVENT_MOUSEMOVE:
        if data['lu_corner'] != (-1, -1) and flags == cv2.EVENT_FLAG_LBUTTON:
            data['img'] = data['origin'].copy()
            data['rd_corner'] = (-1, -1)
            for pos in data['pos']:
                if in_box((x, y), pos, data['shape']):
                    data['rd_corner'] = (x-pos[0], y-pos[1])
                    break
            if data['rd_corner'] != (-1, -1):
                for pos in data['pos']:
                    cv2.rectangle(data['img'], (pos[0]+data['lu_corner'][0], pos[1]+data['lu_corner'][1]),
                                  (pos[0]+data['rd_corner'][0], pos[1]+data['rd_corner'][1]), (0, 0, 255), 2)
            cv2.imshow('multicut',data['img'])
    elif event == cv2.EVENT_RBUTTONDOWN:
        if data['lu_corner'] != (-1, -1) and data['rd_corner'] != (-1, -1):
            lu = (min(data['lu_corner'][0], data['rd_corner'][0]), min(data['lu_corner'][1], data['rd_corner'][1]))
            rd = (max(data['lu_corner'][0], data['rd_corner'][0]), max(data['lu_corner'][1], data['rd_corner'][1]))
            print(lu, rd)
            for pos, filename in zip(data['pos'], data['name']):
                tmp = data['origin'][pos[1]+lu[1]:pos[1]+rd[1], pos[0]+lu[0]:pos[0]+rd[0]]
                cv2.imwrite(os.path.join("output", "cut_"+filename), tmp)


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
        data['pos'].append((imgs[0].shape[1]*i, 0))

    print("img size:", imgs[0].shape)
    cv2.namedWindow('multicut', cv2.WINDOW_AUTOSIZE)

    img = np.hstack(imgs)
    cv2.imshow("multicut", img)


    data['origin'] = img
    data['shape'] = (imgs[0].shape[1], imgs[0].shape[0])
    data['lu_corner'] = (-1, -1)
    data['rd_corner'] = (-1, -1)

    cv2.setMouseCallback("multicut", mouse_handler, data)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()


