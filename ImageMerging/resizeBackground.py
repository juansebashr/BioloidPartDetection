# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:01:13 2018

@author: Pavel
"""

"""
This function will take the whole of SUN database and flaten it into a single 
folder while resizing and cropping all images into given square shape.
If the file is smaller than that, it will be ignored.

"""
import os
from PIL import Image
from resizeimage import resizeimage

def resize_and_crop(image_address, output_address, f_widht, f_height):
    """
    Function for resizing and cropping of single image.
    The image has to be bigger than the desired size.
    If smaller in any dimension, the image will be discarded
    
    Args:
        image_address (string): Image to be resized
        output_address (string): Final destination of the resized image
        f_widht (int): Final desired widht in pixels
        f_height (int): Final desired height in pixels
        
    Returns:
        Nothing
    """
    with open(image_address, 'r+b') as f:
        with Image.open(f) as image:
            widht, height = image.size
            if (widht >= f_widht and height >= f_height):
                cover = resizeimage.resize_cover(image, [f_widht, f_height])
                cover.save(output_address, image.format)
            else:
                print("Image too small to be resized")


def find_all_files(min_pixels, origin_folder, target_folder):
    """
    Function that searches all subfolders of given folder.
    This function assumes that all files in that folder are image files
    If this is not the case errors will occur as no check is carried out.

    For each file, it checks that both of its dimensions are bigger than 
    min_pixels. If so, it will rescale and crop the image to
    min_pixels*min_pixels and save the file to the destination given
    in the top of this file
    
    There is a testing feature count, which allows only few subfolders 
    to be searched, so that this function can be tested
    
    Args:
        min_pixels (int): The final image will be square of this number of pixels 
        origin_folder (string): Path to a folder, which will be searched for
                any images in it or any of its subdirectories
        target_folder (string): path to folder to which the resized images
                should be saved to. This folder will have flat structure.
        
    Returns: 
        root (string): Returns the root address of the original folder
    """
    # count = 0
    for root, dirs, files in os.walk(origin_folder):
        vis_files = [f for f in files if not f[0] == '.']
        copy = True

        if (len(vis_files) > 0 and copy):
            for image_name in vis_files:
                # print(root, dirs, image_name)
                with Image.open(root + "/" + image_name) as tested_image:
                    width, height = tested_image.size
                    if (width >= min_pixels and height >= min_pixels):
                        cover = resizeimage.resize_cover(tested_image, [min_pixels, min_pixels])
                        cover.convert('RGB').save(target_folder + image_name, 'JPEG')

    return root
