# Main folder:
export ND_DSET_FOLDER=$(pwd)/../
# Prefix of the image name you would like to input:
export ND_DSET_OBJ_NAME=banana
# Prefix of the background images names:
export ND_DSET_BG_NAME=background
# Column start pixel value for the background ROI:
export ND_DSET_BG_ROI_CS=35
# Row start pixel value for the background ROI:
export ND_DSET_BG_ROI_RS=49
# Column end pixel value for the background ROI:
export ND_DSET_BG_ROI_CE=245
# Row end pixel value for the background ROI:
export ND_DSET_BG_ROI_RE=144
# Put 1 if your want to enable img resizing, 0 otherwise:
export ND_DSET_RESIZE_FLAG=1
# If resizing is set, the new col number for the background image:
export ND_DSET_RESIZE_COL=416
# If resizing is set, the new row number for the background image:
export ND_DSET_RESIZE_ROW=416
# The class number needed for the detection algorithm:
export ND_DSET_CLASS=1


