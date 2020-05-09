"""
This script split the data from a source folder into a training set and validation set.

source: Folder that contains the files to be split
train: Percentage value of the data that will be part of the training set
(optional) validation: Percentage value of the data that will be part of the validation dataset. If omitted, the value will be the remaing part

usage: split-data.py [-h] [--validation VALIDATION] source train
"""

import os
import argparse
import shutil
from pathlib import Path
from multiprocessing import Pool
from functools import partial

# Output paths
base_path = Path(Path.cwd(), "output")
training_path = Path(base_path, "training")
validation_path = Path(base_path, "validation")

# Create output path for training set
if not Path(training_path).exists():
    os.makedirs(Path(training_path))

# Create output path for validation set
if not Path(validation_path).exists():
    os.makedirs(Path(validation_path))

def get_files(path):
    """
    Get all images files from {path}

    Parameters
    ----------
    path str: Source path that contains the images

    Returns
    -------
    file_list list: List of images full path
    """
    file_list = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".jpg"):
                file_list.append(Path(root, f))

    return file_list

def copy_files(source, destination):
    """
    Copy a file from source to the destination

    Parameter
    ---------
    source str: file path
    destination str: destination folder
    """
    # Add the filename to the destination path
    dst_path = Path(destination, Path(source).name)
    
    print(f"# Copying {source} => {dst_path}")
    shutil.copyfile(source, dst_path)

# Configure parameters
parser = argparse.ArgumentParser(description="Split data from source folder into training and validation")
parser.add_argument("source", help="Folder that contains all files to be split")
parser.add_argument("train", type=int, help="Percentage value of the data that will be part of the training dataset")
parser.add_argument("--validation", "-val", type=int, default=0, help=("Percentage value of the data that will be part of the validation dataset. If omitted, the value will be the remaing part"))

args = parser.parse_args()

if Path(args.source).exists:
    source_files = get_files(args.source)

    # Get the amount of files for training set 
    train_amount = int((len(source_files) * args.train) / 100)
    train_files = source_files[:train_amount]

    # Get the amount of files for validation set. By default is the ramaining after extract the training amount
    if args.validation > 0:
        validation_amount = int((len(source_files) * args.validation) / 100)
        validation_files = source_files[train_amount:train_amount+validation_amount]
    else:
        validation_files = source_files[train_amount:]


    # Run the copy process for training set
    with Pool(processes=8) as pool:
        pool.map(partial(copy_files, destination=training_path), train_files)

    # Run the copy process for validation set
    with Pool(processes=8) as pool:
        pool.map(partial(copy_files, destination=validation_path), validation_files)

    print(f"\n# Total files: {len(source_files)}")
    print(f"# Total training: {len(train_files)}")
    print(f"# Total validation: {len(validation_files)}")
else:
    print(f"# ERROR: {args.source} does not exists.")

print("\n# Finished!")
