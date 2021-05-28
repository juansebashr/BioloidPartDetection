# -*- coding: utf-8 -*-
"""
Created on May 09 of 2021

@author: Sebastian Hernandez

This file includes functionality for combination of flying distractors with
background images.
"""
import os
import random

import numpy as np
from PIL import Image
from resizeimage import resizeimage

class ImageError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def add_random_offset_distractor(foreground_image, pad_ratio=0.0):
    """
    Function that adds a translation to the object pose, before merging
    with the background. An occlusion is also introduced by allowing part
    of the object to move outside of the image frame. This leads to only part
    of the object being visible in the final image. The amount of possible
    occlusion is controlled by the pad_ratio. A temporary frame is created
    that is larger on each side than the original image by
    original_dim*pad_ratio. E.g. 300*300 pixel image with pad_ratio 0.1
    will create a 320*320 frame. The object is then moved to a random position
    within this frame. A final image is created by taking the original sized
    image, cutting out any part of the object being outside of this image.

    Arguments:
        foreground_image (PIL image): An object pose to be translated
        pad_ratio (float): Additional padding around the original image.
                        Introduced for the purpose of occlusion. See above.

    Returns:
        Translated Image (PIL image):
        A object bounding box coordinates (tuple): (x0,x1),(y0,y1)
    """

    # extract subject square
    size = foreground_image.size
    foreground_image = foreground_image.resize(size)
    fg_arr = np.array(foreground_image)
    R, C = np.nonzero(fg_arr[:, :, 3])
    y0 = np.min(R)
    y1 = np.max(R)
    x0 = np.min(C)
    x1 = np.max(C)
    subject_square = fg_arr[y0:y1 + 1, x0:x1 + 1, :]

    # determine range of motion
    padding = (int(np.round(pad_ratio * size[0])), int(np.round(pad_ratio * size[1])))
    padded_size = (size[0] + 2 * padding[0], size[1] + 2 * padding[1])
    w = x1 - x0
    h = y1 - y0
    dw_max = padded_size[1] - w
    dh_max = padded_size[0] - h
    dw = np.random.randint(0, dw_max)
    dh = np.random.randint(0, dh_max)

    fg_arr_pad = np.zeros(shape=(padded_size[0], padded_size[1], 4), dtype=fg_arr.dtype)
    # compute the foreground bb's in the padded image
    x0_pad = dw
    x1_pad = w + dw + 1
    y0_pad = dh
    y1_pad = h + dh + 1
    fg_arr_pad[y0_pad:y1_pad, x0_pad:x1_pad, :] = subject_square
    fg_arr_new = fg_arr_pad[padding[0]:(padding[0] + size[0]), padding[1]:(padding[1] + size[1]), :]

    return Image.fromarray(fg_arr_new)


def add_background_distractor(foreground_name, background_name, save_as, img_size=412):
    """
    Function that give an RGBA and any image file merges them into one.
    It ensures that the final image is of the specified size.
    If either of the given images is too small, an error is returned.
    The brightness of the background can be adjusted to be better
    correspond to the brightness of the foreground. This is optional
    functionality that is triggered by the corresponding input parameter.

    Args:
        foreground_name (string): The name of the RGBA image
        background_name (string): Name of the background image
        save_as (string): Complete path with name under which the final image
            is to be saved

    Return:
        Nothing
    """
    try:
        foreground = Image.open(foreground_name)
        foreground = add_random_offset_distractor(foreground, pad_ratio=0.1)
    except:
        print("Invalid foreground images, skipping", foreground_name)
        raise ImageError(("Invalid foreground images, skipping", foreground_name))
    try:
        background = Image.open(background_name)
    except:
        # This is technically problematic as we might throw away
        # valid object poses because of invalid backgrounds
        print("Invalid background image skipping", background_name)
        raise ImageError(("Invalid background image skipping", background_name))

    bc_size = background.size
    if img_size > bc_size[0] or img_size > bc_size[1]:
        background = background.resize((img_size, img_size), resample=Image.BICUBIC)

    elif img_size < bc_size[0] or img_size < bc_size[1]:
        background = resizeimage.resize_cover(background, [img_size, img_size])

    background.paste(foreground, (0,0), foreground)
    background = background.convert('RGB')
    background.save(save_as, "JPEG", quality=80, optimize=True, progressive=True)
    return


def merge_all_distractors(distractors_folder, background_folder, final_folder, n_of_images, img_size=412, n_of_distractors=3):
    """
    This function takes every image in objects_folder, merge it
    with a random image from background_folder and saves it in final_folder.
    It works for any images sizes but for consistency of scale it is
    advised to rescale the images

    Args:
        distractors_folder (string): Folder containing the foreground RGBA images
        background_folder (string): Folder containing background images
        final_folder (string): Folder to which save the final images
        img_size (int): Width and height of the resulting image
        n_of_distractors (int): Number of the resultant distractors in the image
    Return:
        Nothing
    """
    all_backgrounds = os.listdir(background_folder)
    all_distractors = os.listdir(distractors_folder)
    for j in range(n_of_images):
        one_object = random.choice(all_backgrounds)
        for i in range(n_of_distractors):
            random_distractor = random.choice(all_distractors)
            if i == 0:
                try:
                    add_background_distractor(distractors_folder + "/" + random_distractor, background_folder + "/" + one_object,
                                              final_folder + "/" + 'distractors' + str(j) + ".jpg", img_size)
                except Exception as e:
                    print("The following error occurred during background addition:", e)
                    raise e
            else:
                try:
                    add_background_distractor(distractors_folder + "/" + random_distractor, final_folder + "/" + 'distractors' + str(j) + ".jpg",
                                              final_folder + "/" + 'distractors' + str(j) + ".jpg", img_size)
                except Exception as e:
                    print("The following error occurred during background addition:", e)
                    raise e

    return
