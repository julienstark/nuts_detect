"""
Main handler for the Nuts Detection dataset creation.

Usage: python3 main.py --number NUMBER --scale SCALE --threshold THRESHOLD
"""

import os
import argparse

from random import randint
from random import uniform

import nuts as nt
import background as bg
import operations as op

def main(): # pylint: disable=too-many-locals
    """Main function for client loop."""

    # PYTHON PARSER VIA ARGPARSE #

    parser = argparse.ArgumentParser(description="Nuts Detect Dset Main.")
    parser.add_argument("-n", "--number", required=True,
                        help="Nuts number to input.", type=int)
    parser.add_argument("-i", "--iter", required=True,
                        help="Number of iterations.", type=int)
    parser.add_argument("-s", "--scale", help="Scale modification.",
                        nargs='?', default=0.25, type=float)
    parser.add_argument("-t", "--threshold", help="Threshold for nuts mask.",
                        nargs='?', default=50, type=int)
    parser.add_argument("-f", "--filename", help="Name for the saved image.",
                        nargs='?', default='test_bg.jpeg', type=str)
    args = vars(parser.parse_args())

    nuts_nbr = args['number']
    iter_nbr = args['iter']
    scale = float(args['scale'])
    threshold = int(args['threshold'])
    filename = args['filename']

    # ENVIRON VAR INITIALIZATION #

    img_loc = os.environ['ND_DSET_FOLDER'] + 'imgs/data/'
    object_name = os.environ['ND_DSET_OBJ_NAME']
    resize = int(os.environ['ND_DSET_RESIZE_FLAG'])
    rszx = int(os.environ['ND_DSET_RESIZE_COL'])
    rszy = int(os.environ['ND_DSET_RESIZE_ROW'])
    cls = int(os.environ['ND_DSET_CLASS'])

    # MAIN LOOP - OBJECT CREATION AND INPUT #
    for itera in range(1, iter_nbr):

        # Initialize background
        random_bg_nbr = randint(1, op.get_file_number(img_loc + "backgrounds/"))
        background = bg.Background(img_loc + "backgrounds/" +
                                   os.environ['ND_DSET_BG_NAME'] +
                                   str(random_bg_nbr) + '.jpeg')

        if resize == 1:
            background.image = op.resize_image(background.image, (rszx, rszy))
            background.mask = op.resize_image(background.mask, (rszx, rszy))

            # Get resize multiplier
            mult_col, mult_row = op.get_resize_prop(320, 240, rszx, rszy)

            # Resize ROI
            new_roi = (int(background.rois[0][0]*mult_col),
                       int(background.rois[0][1]*mult_row),
                       int(background.rois[0][2]*mult_col),
                       int(background.rois[0][3]*mult_row))
            background.rois = [new_roi]

        background.init_mask()

        # Initialize text path
        file_path = (os.environ['ND_DSET_FOLDER'] + 'txt/iter' + str(itera) +
                     ".txt")

        # Start nuts loop
        for _nut_nbr in range(nuts_nbr):

            # Initialize locals
            nut = nt.Nuts(img_loc + "nuts/" + object_name +
                          str(randint(1, 10)) + '.jpeg')
            rows, cols, _channels = nut.image.shape

            if resize == 1:
                nut.image = op.resize_image(nut.image,
                                            (int(cols*mult_col), int(rows*mult_row)))
                rows, cols, _channels = nut.image.shape

            nut_placer_row, nut_placer_col = background.get_nut_placer()

            # Apply nut transformation
            random_scale = uniform(1 - scale, 1 + scale)
            random_rot = randint(0, 180)
            nut.scale_nut(height_scale=random_scale, width_scale=random_scale)
            nut.rotate_nut(rotate_angle=random_rot)

            # Merge the nut in the background image and retrieve the mask
            background.input_nut(nut, nut_placer_row, nut_placer_col,
                                 threshold)
            background.msk_input_nut(nut, nut_placer_row, nut_placer_col,
                                     threshold)

            # Smooth some ugly edges
            background.smoothing(nut, nut_placer_row, nut_placer_col)

            # Write nuts info to the file
            line = "1 {} {} {} {}\n".format(nut_placer_row, nut_placer_col,
                                            cols, rows)
            with open(file_path, 'a') as filen:
                filen.write(line)


        # Save the final image and the final mask
        background.save_background(img_loc + filename + str(itera) + '.jpeg')
        background.save_background_mask(img_loc + "mask_" + filename +
                                        str(itera) + '.jpeg')


if __name__ == '__main__':
    main()
