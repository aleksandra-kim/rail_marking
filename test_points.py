#!/usr/bin/env python
import os
import sys
import cv2
import datetime
import numpy as np
import scipy.io

RED = 0
BLUE = 1
BLACK = 2


def find_coor(level):
    lblue = np.where(level == BLUE)[0][0]
    rblue = np.where(level == BLUE)[0][-1]
    len_lred = np.where(level[lblue:0:-1] == BLACK)[0][0]
    len_rred = np.where(level[rblue:, ] == BLACK)[0][0]
    print(len_lred, len_rred)
    y_left = lblue - len_lred//2
    y_right = rblue + len_rred//2
    return y_left, y_right


def get_line_points(m):
    x_top = m.shape[0]//2
    level_top = m[x_top, :]
    y_top_left, y_top_right = find_coor(level_top)
    print(y_top_left, y_top_right)

    x_bottom = int(2*m.shape[0]//3)
    level_bottom = m[x_bottom, :]
    y_bottom_left, y_bottom_right = find_coor(level_bottom)

    # return {
    #     "left": [
    #         (x_bottom, y_bottom_left),
    #         (x_top, y_top_left)
    #     ],
    #     "right": [
    #         (x_bottom, y_bottom_right),
    #         (x_top, y_top_right)
    #    ],
    # }
    return {
        "left": [
            (y_bottom_left, x_bottom),
            (y_top_left, x_top)
        ],
        "right": [
            (y_bottom_right, x_bottom),
            (y_top_right, x_top)
       ],
    }


def test():
    image = cv2.imread("result.png")
    mask = scipy.io.loadmat('mask.mat')['result_mask']
    print(mask.shape, image.shape)
    data = get_line_points(mask)
    print(data, data['left'][0], data['right'][0])
    cv2.circle(image, data['left'][0], 5, (255, 0, 255), 3)
    cv2.circle(image, data['left'][1], 5, (255, 0, 255), 3)
    cv2.circle(image, data['right'][0], 5, (255, 0, 0), 3)
    cv2.circle(image, data['right'][1], 5, (255, 0, 0), 3)
    cv2.imshow("test", image)
    k = cv2.waitKey(0)


if __name__ == "__main__":
    # main()
    test()