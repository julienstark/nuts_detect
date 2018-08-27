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

def main():
    """Main function for client loop."""

    # PYTHON PARSER VIA ARGPARSE #

    parser = argparse.ArgumentParser(description="Nuts Detect Dset Main.")
    parser.add_argument("-n", "--number", required=True,
                        help="Nuts number to input.", type=int)
    parser.add_argument("-s", "--scale", help="Scale modification.",
                        nargs='?', default=0.25, type=float)
    parser.add_argument("-t", "--threshold", help="Threshold for nuts mask.",
                        nargs='?', default=50, type=int)
    parser.add_argument("-f", "--filename", help="Name for the saved image.",
                        nargs='?', default='test_bg.jpeg', type=str)
    args = vars(parser.parse_args())

    nuts_nbr = args['number']
    scale = float(args['scale'])
    threshold = int(args['threshold'])
    filename = args['filename']

    # ENVIRON VAR INITIALIZATION #

    img_loc = os.environ['ND_DSET_FOLDER'] + 'imgs/data/'
    object_name = os.environ['ND_DSET_OBJ_NAME']
    background = bg.Background(img_loc + os.environ['ND_DSET_BG_NAME'] +
                               '.jpeg')
    background.init_mask()

    # MAIN LOOP - OBJECT CREATION AND INPUT #

    for _nut_nbr in range(nuts_nbr):

        nut = nt.Nuts(img_loc + object_name + str(randint(1, 10)) + '.jpeg')

        random_scale = uniform(1 - scale, 1 + scale)
        random_rot = randint(0, 180)

        nut.scale_nut(height_scale=random_scale, width_scale=random_scale)
        nut.rotate_nut(rotate_angle=random_rot)

        nut_placer_row, nut_placer_col = background.get_nut_placer()
        background.input_nut(nut, nut_placer_row, nut_placer_col, threshold)
        background.msk_input_nut(nut, nut_placer_row, nut_placer_col,
                                 threshold)

    background.save_background(img_loc + filename)
    background.save_background_mask(img_loc + "mask_" + filename)

if __name__ == '__main__':
    main()
