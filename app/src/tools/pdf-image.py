"""
This script converts all pdf from the source folder into images

By default all images are saved into the "output" folder.

With the [--group | -g] option the script will create a folder per pdf into the output and save the images in there

usage: pdf-image.py [-h] [--group] source
"""

import os
import argparse
import pathlib
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image

def create_folder_structure(path):
    """
    Create the folder structure using the {path}

    Parameters
    ----------
    path str: Path to be created

    Returns
    -------
    path str: Path created
    """
    
    if not Path(path).exists():
        os.makedirs(path)

    return path

def get_pdf_files(source_path):
    """
    Get all pdf files from the {source_path}

    Parameters
    ----------
    source_path str: path that contains the files to be converted

    Returns
    -------
    pdf_list list: list with the path to the pdf files
    """

    pdf_list = []

    for root, _, files in os.walk(source_path):
        for f in files:
            if f.endswith(".pdf"):
                pdf_list.append(Path(root, f))
    
    return pdf_list

def save_images(images, start_id, output_path):
    """
    Save the images using the {start_id} as name into {output_path}

    Parameters
    ----------
    images list: list of PIL images
    start_id: start number used as a name image
    output_path str: destination folder to save the images

    Returns
    start_id int: counter updated
    """

    for img in images:
        img.save(Path(output_path, str(start_id)), format="JPEG")
        start_id += 1

    return start_id

parser = argparse.ArgumentParser(description="Convert pdf files from source location to JPEG images")
parser.add_argument("source", help="Folder that contains the pdf files")
parser.add_argument("--group", "-g", action="store_true", help="Save the images on its own folder inside the output folder")

args = parser.parse_args()

base_output_path = create_folder_structure(Path(Path.cwd(), "output"))

if Path(args.source).exists():
    # Counter used for the image name
    img_next_id = 1 

    pdf_list = get_pdf_files(args.source)

    for i, f in enumerate(pdf_list):
        if args.group:
            # Create the output folder with the pdf name
            output_folder = os.path.splitext(f)[0].split(pathlib.os.sep)[-1]
            destination_path = create_folder_structure(Path(base_output_path, output_folder))
            img_next_id = 1
        else:
            destination_path = base_output_path
            
        print(f"\n# [{i+1}/{len(pdf_list)}] Converting {f} ", end="")
        images = convert_from_path(f)
        
        print(f" ==> Saving into {destination_path}", end="")
        img_next_id = save_images(images, img_next_id, destination_path)

print("\n\n# Conversion finished!")