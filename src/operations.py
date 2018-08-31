"""
Module supporting the operations functions needed for various file operations
for the Nuts Detect (ND) project.

function get_file_number: Get the number of files in a folder.
"""

import os

def get_file_number(path):
    """Get file number for a folder.

    Args:
        path: A string representing the folder path.

    Returns:
        An int representing the number of files in a folder.
    """
    nbr = [n for n in os.listdir(path) if os.path.isfile(os.path.join(path, n))]
    return len(nbr)
