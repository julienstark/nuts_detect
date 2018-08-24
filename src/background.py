# pylint: disable=missing-docstring

from random import randint

import cv2

class Background:

    def __init__(self, img_path, selection="auto"):
        self.img_path = img_path
        self.image = cv2.imread(img_path)
        self.selection = selection
        self.rois = [(522, 1257, 1084, 193),
                     (413, 1151, 279, 209),
                     (1326, 1123, 316, 277)]

    def init_roi(self):
        if self.rois is not None:
            if input("ROI already present. Override? (Y/N)") == 'Y':
                rois = cv2.selectROI(self.img_path)
                k = cv2.waitKey(0)
                if k == 27:
                    cv2.destroyAllWindows()
                self.rois = []
                self.rois = self.rois.append(rois)
            else:
                print("Aborting ROI creation..")

    def get_nut_placer(self):
        selected_delimiter = self.rois[randint(0, len(self.rois) - 1)]
        delim_row_b = selected_delimiter[1]
        delim_row_e = selected_delimiter[1] + selected_delimiter[3]
        delim_col_b = selected_delimiter[0]
        delim_col_e = selected_delimiter[0] + selected_delimiter[2]

        nut_placer_row = randint(delim_row_b, delim_row_e)
        nut_placer_col = randint(delim_col_b, delim_col_e)

        return (nut_placer_row, nut_placer_col)

    def input_nut(self, nut):
        background = self.image

        rows, cols, _channels = nut.image.shape

        nut_placer_row, nut_placer_col = self.get_nut_placer()

        roi = background[nut_placer_row:rows, nut_placer_col:cols]

        mask, mask_inv = nut.get_mask()

        background_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        nut_fg = cv2.bitwise_and(nut.image, nut.image, mask=mask)

        dst = cv2.add(background_bg, nut_fg)
        background[nut_placer_row:rows, nut_placer_col:cols] = dst

        self.image = background

    def save_background(self, save_path):
        cv2.imwrite(save_path, self.image)
