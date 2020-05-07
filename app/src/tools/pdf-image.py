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
from multiprocessing import Pool
from functools import partial

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

def save_images(images, img_base_name, output_path):
    """
    Save the images using the {start_id} as name into {output_path}

    Parameters
    ----------
    images list: list of PIL images
    img_base_name str: string used as a base name for the image 
    output_path str: destination folder to save the images
    """

    for id, img in enumerate(images):
        img_name = f"{img_base_name}_{id}"

        img.save(Path(output_path, img_name), format="JPEG")

def process_file(file, is_group):
    img_base_name = os.path.splitext(file)[0].split(pathlib.os.sep)[-1]

    if is_group:
        # Create the output folder with the pdf name
        output_folder = img_base_name
        destination_path = create_folder_structure(Path(base_output_path, output_folder))
    else:
        destination_path = base_output_path
    
    try:
        print(f"# Converting {file}...")
        images = convert_from_path(file)
        
        save_images(images, img_base_name, destination_path)
        return {"status": "ok", "message": f"[saved] {file} => {destination_path}"}
    except:
        return {"status": "error", "message": f"ERROR when processing {file}"}

parser = argparse.ArgumentParser(description="Convert pdf files from source location to JPEG images")
parser.add_argument("source", help="Folder that contains the pdf files")
parser.add_argument("--group", "-g", action="store_true", help="Save the images on its own folder inside the output folder")

args = parser.parse_args()

base_output_path = create_folder_structure(Path(Path.cwd(), "output"))

if Path(args.source).exists():
    pdf_list = get_pdf_files(args.source)
    counter = 1

    with Pool(processes=8) as pool:
        for msg in pool.imap_unordered(partial(process_file, is_group=args.group), pdf_list):
            if msg["status"] == "ok":
                print(f"# [{counter}/{len(pdf_list)}] {msg['message']}")
            else:
                print(f"{msg['message']}")

            counter += 1
        
print("\n# Conversion finished!")