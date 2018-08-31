"""
Module supporting the Nuts class needed for generating nuts object
images for the Nuts Detect (ND) project.

class Nuts: Creates a cv2 image based on a .jpeg and allows object
modification (scale, rotation) and mask obtention.
"""

import cv2


class Nuts:
    """Create and manage a nut image.

    Main class of the ND project, creates a cv2 image based on a .jpeg and
    represents an object to input. Can be modified in rotation and in scale,
    and can returns its own mask.

    Attributes:
        img_path: A string representing the background image location.
        image: A cv2 image (numpy array) representing a nuts image.
    """

    def __init__(self, img_path):
        """Init nut image with img_path"""

        self.img_path = img_path
        self.image = cv2.imread(img_path)


    def scale_nut(self, height_scale=1.25, width_scale=1.25):
        """Scale the nut based on arg provided.

        Args:
            height_scale: A float representing the scaling to apply to the
            image height.
            width_scale: A float representing the scaling to apply to the
            image scale.

        Returns:
            None
        """

        height, width = self.image.shape[:2]
        self.image = cv2.resize(self.image,
                                (int(width_scale*width),
                                 int(height_scale*height)))


    def rotate_nut(self, rotate_angle=90):
        """Rotate the nut based on the arg provided.

        Args:
            rotate_angle: An int representing the angle used for image
            rotation.

        Returns:
            None
        """

        rows, cols, _channel = self.image.shape
        r_mat = cv2.getRotationMatrix2D((cols/2, rows/2),
                                        rotate_angle, 1)
        self.image = cv2.warpAffine(self.image, r_mat, (cols, rows))


    def get_mask(self, threshold):
        """Retrive object image mask.

        Args:
            threshold: An int representing the threshold value we want to use
            to discriminate the pixels in the object image.

        Returns:
            A tuple representing two numpy arrays with the mask and its
            inverse.
        """

        nut_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _ret, mask = cv2.threshold(nut_gray, threshold, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        return (mask, mask_inv)
