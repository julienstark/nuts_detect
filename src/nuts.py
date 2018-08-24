# pylint: disable=missing-docstring

import cv2

class Nuts:

    def __init__(self, img_path):
        self.img_path = img_path
        self.image = cv2.imread(img_path)

    def scale_nut(self, height_scale=1.25, width_scale=1.25):
        height, width = self.image.shape[:2]
        self.image = cv2.resize(self.image,
                                (width_scale*width,
                                 height_scale*height))

    def rotate_nut(self, rotate_angle=90):
        rows, cols = self.image.shape
        r_mat = cv2.getRotationMatrix2D((cols/2, rows/2),
                                        rotate_angle, 1)
        self.image = cv2.warpAffine(self.image, r_mat, (cols, rows))

    def get_mask(self):
        nut_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _ret, mask = cv2.threshold(nut_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        return (mask, mask_inv)
