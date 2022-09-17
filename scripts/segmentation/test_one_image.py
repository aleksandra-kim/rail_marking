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

CURRENT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".")
sys.path.append(os.path.join(CURRENT_DIR, "../../"))
try:
    from rail_marking.segmentation.deploy import RailtrackSegmentationHandler
    from cfg import BiSeNetV2Config
except Exception as e:
    print(e)
    sys.exit(0)


def get_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-snapshot", type=str, required=True)
    parser.add_argument("-image_path", type=str, required=True)
    parser.add_argument("-output_image_path", type=str, default="result.png")
    parser.add_argument("-num_test", type=int, default=1)

    args = parser.parse_args()

    return args


def find_coor(level):
    try:
        lblue = np.where(level == BLUE)[0][0]
        rblue = np.where(level == BLUE)[0][-1]
        len_lred = np.where(level[lblue:0:-1] == BLACK)[0][0]
        len_rred = np.where(level[rblue:, ] == BLACK)[0][0]
        print(len_lred, len_rred)
        y_left = lblue - len_lred//2
        y_right = rblue + len_rred//2
        return y_left, y_right
    except:
        return None, None


def get_line_points(m):
    x_top = m.shape[0]//2
    level_top = m[x_top, :]
    y_top_left, y_top_right = find_coor(level_top)

    if y_top_left is None or y_top_right is None:
        return {
            "tracks": False,
        }

    x_bottom = int(2*m.shape[0]//3)
    level_bottom = m[x_bottom, :]
    y_bottom_left, y_bottom_right = find_coor(level_bottom)

    if y_bottom_left is None or y_bottom_right is None:
        return {
            "tracks": False,
        }

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
            [int(y_bottom_left), int(x_bottom)],
            [int(y_top_left), int(x_top)],
        ],
        "right": [
            [int(y_bottom_right), int(x_bottom)],
            [int(y_top_right), int(x_top)],
        ],
        "tracks": True,
    }


def interface(image, return_overlay=False):
    start = datetime.datetime.now()
    snapshot = "bisenetv2_checkpoint_BiSeNetV2_epoch_300.pth"
    segmentation_handler = RailtrackSegmentationHandler(snapshot, BiSeNetV2Config())
    mask, overlay = segmentation_handler.run(image, only_mask=False)
    data = get_line_points(mask)
    _processing_time = datetime.datetime.now() - start

    print("processing time one frame {}[ms]".format(_processing_time.total_seconds() * 1000))

    if return_overlay:
        return data, overlay
    else:
        return data


def image2image(image):

    data, overlay = interface(image, return_overlay=True)

    if data['tracks']:
        cv2.circle(overlay, data['left'][0], 5, (255, 0, 255), 3)
        cv2.circle(overlay, data['left'][1], 5, (255, 0, 255), 3)
        cv2.circle(overlay, data['right'][0], 5, (255, 0, 0), 3)
        cv2.circle(overlay, data['right'][1], 5, (255, 0, 0), 3)

    return overlay


def main():
    args = get_args()
    segmentation_handler = RailtrackSegmentationHandler(args.snapshot, BiSeNetV2Config())
    image = cv2.imread(args.image_path)

    start = datetime.datetime.now()
    for i in range(args.num_test):
        mask, overlay = segmentation_handler.run(image, only_mask=False)
    _processing_time = datetime.datetime.now() - start

    # cv2.imshow("result", overlay)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(args.output_image_path, overlay)

    print("processing time one frame {}[ms]".format(_processing_time.total_seconds() * 1000 / args.num_test))


if __name__ == "__main__":
    # main()
    interface()
