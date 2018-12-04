"""
Main handler for the Nuts Detection dataset creation.

Usage: python3 main.py --number NUMBER --scale SCALE --threshold THRESHOLD
"""

import os
import argparse

from random import randint
from random import uniform

import item as nt
import background as bg
import operations as op

def main(): # pylint: disable=too-many-locals,too-many-statements
    """Main function for client loop."""

    # PYTHON PARSER VIA ARGPARSE #

    parser = argparse.ArgumentParser(description="Nuts Detect Dset Main.")
    parser.add_argument("-n", "--number", required=True,
                        help="Items number to input.", type=int)
    parser.add_argument("-i", "--iter", required=True,
                        help="Number of iterations.", type=int)
    parser.add_argument("-s", "--scale", help="Scale modification.",
                        nargs='?', default=0.25, type=float)
    parser.add_argument("-t", "--threshold", help="Threshold for items mask.",
                        nargs='?', default=50, type=int)
    parser.add_argument("-f", "--filename", help="Name for the saved image.",
                        nargs='?', default='test_bg.jpeg', type=str)
    args = vars(parser.parse_args())

    items_nbr = args['number']
    iter_nbr = args['iter']
    scale = float(args['scale'])
    threshold = int(args['threshold'])
    filename = args['filename']

    # ENVIRON VAR INITIALIZATION #
    print("Initializing environment variables...", end='')
    img_loc = os.environ['ND_DSET_FOLDER'] + 'imgs/data/'
    object_name = os.environ['ND_DSET_OBJ_NAME']
    resize = int(os.environ['ND_DSET_RESIZE_FLAG'])
    rszx = int(os.environ['ND_DSET_RESIZE_COL'])
    rszy = int(os.environ['ND_DSET_RESIZE_ROW'])
    cls = int(os.environ['ND_DSET_CLASS'])

    background_roi = (int(os.environ['ND_DSET_BG_ROI_CS']),
                      int(os.environ['ND_DSET_BG_ROI_RS']),
                      int(os.environ['ND_DSET_BG_ROI_CE']),
                      int(os.environ['ND_DSET_BG_ROI_RE']))
    print("OK")

    # MAIN LOOP - OBJECT CREATION AND INPUT #
    print("\n ** Generating background and objects... **")
    for itera in range(1, iter_nbr + 1):

        # Initialize background
        random_bg_nbr = randint(1, op.get_file_number(img_loc + "backgrounds/"))
        background = bg.Background(img_loc + "backgrounds/" +
                                   os.environ['ND_DSET_BG_NAME'] +
                                   "_" + str(random_bg_nbr) + '.jpeg',
                                   rois=background_roi)

        # Resize if flag set and adapt rois accordingly
        if resize == 1:
            background.image = op.resize_image(background.image, (rszx, rszy))
            background.mask = op.resize_image(background.mask, (rszx, rszy))

            # Get resize multiplier
            mult_col, mult_row = op.get_resize_prop(background.image.shape[0],
                                                    background.image.shape[1],
                                                    rszx, rszy)

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

        # Start items loop
        for _item_nbr in range(items_nbr):

            # Initialize locals
            item = nt.Item(img_loc + "items/" + object_name + "_" +
                           str(randint(1, 10)) + '.jpeg')
            rows, cols, _channels = item.image.shape

            if resize == 1:
                item.image = op.resize_image(item.image,
                                             (int(cols*mult_col), int(rows*mult_row)))
                rows, cols, _channels = item.image.shape

            item_placer_row, item_placer_col = background.get_item_placer()

            # Apply item transformation
            random_scale = uniform(1 - scale, 1 + scale)
            random_rot = randint(0, 180)
            item.scale_item(height_scale=random_scale, width_scale=random_scale)
            item.rotate_item(rotate_angle=random_rot)

            # Merge the item in the background image and retrieve the mask
            background.input_item(item, item_placer_row, item_placer_col,
                                  threshold)
            background.msk_input_item(item, item_placer_row, item_placer_col,
                                      threshold)

            # Smooth some ugly edges
            background.smoothing(item, item_placer_row, item_placer_col)

            # Write items info to the file
            hgt, wid, _chan = background.image.shape
            backshape = (hgt, wid)
            itemshape = (rows, cols)
            placer = (item_placer_row, item_placer_col)
            op.write_item_info_file(cls, placer, itemshape, backshape,
                                    file_path)


        # Save the final image and the final mask
        background.save_background(img_loc + "gen/" + filename + str(itera) +
                                   '.jpg')
        background.save_background_mask(img_loc + "mask/mask_" + filename +
                                        str(itera) + '.jpg')
    print("Done!")


    # VALIDATION PHASE #
    print("\n ** Validation Phase **")
    validate(img_loc, os.environ['ND_DSET_FOLDER'], iter_nbr, cls)


def validate(img_loc, txt_loc, iter_nbr, cls): # pylint: disable=too-many-branches
    """Validate ouputs.

    Args:
        img_loc: A string representing image path.
        txt_loc: A string representing txt path.
        iter_nbr: An int representing the number of iterations.
        cls: An int representing the class.

    Returns:
        None
    """

    gen_error = False

    print("Checking generated image number...", end="")
    if op.validate_img_number(img_loc + "gen/", iter_nbr):
        print("OK")
    else:
        print("ERR")
        gen_error = True

    print("Checking generated mask number...", end="")
    if op.validate_img_number(img_loc + "mask/", iter_nbr):
        print("OK")
    else:
        print("ERR")
        gen_error = True

    print("Checking generated textfile number...", end="")
    if op.validate_img_number(txt_loc + 'txt/', iter_nbr):
        print("OK")
    else:
        print("ERR")
        gen_error = True

    print("Checking textfiles values...")
    err_flag = False
    for file_iter in range(1, op.get_file_number(txt_loc + 'txt/') + 1):
        iter_list = []
        with open(txt_loc + 'txt/iter' + str(file_iter) + '.txt') as fobj:
            for line in fobj:
                row = line.split()
                for item in row:
                    iter_list.append(float(item))
        iter_list = [x for x in iter_list if x != float(cls)]
        for number in iter_list:
            if number > 1.0:
                print("Bad value for iter file {}.".format(file_iter))
                err_flag = True

    if err_flag:
        print("Txt files values error.")
        gen_error = True
    else:
        print("Txt files values OK")

    if not gen_error:
        print("Validation phase succeeded!")


if __name__ == '__main__':
    main()
