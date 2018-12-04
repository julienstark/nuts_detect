"""
Module supporting the Background class needed for generating a background
image for the Nuts Detect (ND) project.

class Background: Creates a cv2 image based on a .jpeg and allows object
merge and region of interest (ROI) definiton.
"""

from random import randint

import cv2
import numpy as np


class Background:
    """Create and manage a background image.

    This is one of the main class of the ND project and is needed all the
    time. It creates a cv2 image based on a .jpeg image with no constraints
    on the size and channels. Also includes input object and ROI definition
    methods.

    Attributes:
        img_path: A string representing the background image location.
        image: A cv2 image (numpy array) representing the background image.
        selection: A string representing whether or not ROI definition
        is automatic or manuel. Currently unused attribute.
        rois: A list containing tuples representing different ROIS (row_start,
        row_end, col_start, col_end).
    """


    def __init__(self, img_path, selection="auto"):
        """Init background image with img_path and selection mode"""

        self.img_path = img_path
        self.image = cv2.imread(img_path)
        self.mask = cv2.imread(img_path)
        self.selection = selection
        # self.rois = [(522, 1257, 1084, 193),
        #             (413, 1151, 279, 209),
        #             (1326, 1123, 316, 277)]
        # (colb, rowb, cole, rowel)
        #self.rois = [(35, 49, 245, 144)]
        self.rois = [(28, 53, 287, 195)]


    def init_mask(self):
        """Init background mask.

        Args:
            None

        Returns:
            None
        """

        self.mask[:] = (255, 255, 255)


    def init_roi(self):
        """Allow new ROI creation.

        This will override default ROI list and only populate the self.rois
        attribute with one element. Dependency on cv2.selectROI function.

        Args:
            None

        Returns:
            None
        """

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


    def get_item_placer(self):
        """Randomly select a ROI and a position in this ROI for item placement.

        Args:
            None

        Returns:
            A tuple representing the row and the column in the background
            image matrix for the object to be input.
        """

        selected_delimiter = self.rois[randint(0, len(self.rois) - 1)]
        delim_row_b = selected_delimiter[1]
        delim_row_e = selected_delimiter[1] + selected_delimiter[3]
        delim_col_b = selected_delimiter[0]
        delim_col_e = selected_delimiter[0] + selected_delimiter[2]

        item_placer_row = randint(delim_row_b, delim_row_e)
        item_placer_col = randint(delim_col_b, delim_col_e)

        return (item_placer_row, item_placer_col)


    def input_item(self, item, item_placer_row, item_placer_col, threshold=50):
        """Take one object and merge it with the background image.

        Args:
            item: An item object representing the object to merge.
            threshold: An int representing the threshold when creating
            object mask.
            item_placer_row: An int representing a position in the matrix
            item_placer_col: An int representing a position same as above
            but for column.

        Returns:
            None
        """

        rows, cols, _channels = item.image.shape

        roi = self.image[item_placer_row:item_placer_row + rows,
                         item_placer_col:item_placer_col + cols]

        mask, mask_inv = item.get_mask(threshold)

        background_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        item_fg = cv2.bitwise_and(item.image, item.image, mask=mask)

        dst = cv2.add(background_bg, item_fg)
        self.image[item_placer_row:item_placer_row + rows,
                   item_placer_col:item_placer_col + cols] = dst


    def smoothing(self, item, item_placer_row, item_placer_col):
        """Smooth some edges on the nut.

        If the grayscale picture of the nut has one pixel level below a
        specific value, apply some smoothing on this pixel with a 3x3 filter.

        Args:
            item: A nut object representing the object to smooth.
            item_placer_row: An int representing a position in the matrix.
            item_placer_col: An int representing a position same as above
            but for column.

        Returns:
            None
        """

        kernel = np.ones((3, 3), np.float32)/9
        item_gray = cv2.cvtColor(item.image, cv2.COLOR_BGR2GRAY)
        height, width = item_gray.shape[:2]
        for i in range(height):
            for j in range(width):
                if item_gray[i, j] < 30:
                    input_zone = self.image[item_placer_row + i - 1:item_placer_row + i + 1,
                                            item_placer_col + j - 1:item_placer_col + j + 1]
                    dst = cv2.filter2D(input_zone, -1, kernel)
                    self.image[item_placer_row + i - 1:item_placer_row + i + 1,
                               item_placer_col + j - 1:item_placer_col + j + 1] = dst


    def msk_input_item(self, item, item_placer_row, item_placer_col, threshold=50):
        """Take one object and merge it with the background image mask.

        Args:
            item: An item object representing the object to merge.
            threshold: An int representing the threshold when creating
            object mask.
            item_placer_row: An int representing a position in the matrix
            item_placer_col: An int representing a position same as above
            but for column.

        Returns:
            None
        """

        rows, cols, _channels = item.image.shape

        roi = self.mask[item_placer_row:item_placer_row + rows,
                        item_placer_col:item_placer_col + cols]

        _mask, mask_inv = item.get_mask(threshold)

        mask_background_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        self.mask[item_placer_row:item_placer_row + rows,
                  item_placer_col:item_placer_col + cols] = mask_background_bg


    def save_background(self, save_path):
        """Save the background image.

        Args:
            save_path: A string representing the filename and location to
            save to.

        Returns:
            None
        """

        cv2.imwrite(save_path, self.image)


    def save_background_mask(self, save_path):
        """Save the background image mask.

        Args:
            save_path: A string representing the filename and location to
            save to.

        Returns:
            None
        """

        cv2.imwrite(save_path, self.mask)
