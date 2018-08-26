# nuts_detect

Simple project to merge and display one background image with several object images by defining specific regions of interest (ROI) on the former.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them. Python3 libraries are in requirements.txt for easy installation with pip.

- Linux >= 4.17.11
- Bash >= 4.4.23
- Python >= 3.7.0
- Numpy >= 1.15.0
- opencv-python >= 3.4.2.17

Earlier program/package versions might work too but haven't been tested.

### Installing

A step by step series of examples that tell you how to get a development env running.

Simply clone the repository and ensure that you're on the **master** branch.

```bash
git clone https://github.com/eamsjulien/nuts_detect.git ; cd nuts_detect ; git checkout origin/master
```

Create imgs/data/ folders on the main project path.
```bash
mkdir -p imgs/data
```

Ensure that the background image and objects are populated in the above folder as .jpeg extension.

Ensure that the ND_DSET_FOLDER is corresponding to the location where you will launch the launch.sh script.
Ensure that other environment variables are accurate as well.

```bash
cd src ; vim setup_env.sh
```

And good to go !

### Running

This section will introduce a quick way to get the program running:

```bash
./launch.sh --number 50 --scale 0.25 --threshold 50 --filename 'test_bg.jpeg'
```

Replace the first 50 by the number of objects you would like to merge with the base image.
Replace 0.25 by the scaling effect you would like to put on all merged image. Recommendation is to keep 0.25.
Replace the second 50 by the threshold value you would like to apply when creating object mask for merging.
Replace test_bg.jpeg by the filename of the image you would like to save.
