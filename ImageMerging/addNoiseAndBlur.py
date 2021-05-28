"""
This file contains functions for adding blur and noise to the images, actually is not
being used
"""

import os
import random
import cv2
import numpy as np


def sp_Noise(image, prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


def Gaussian_Noise(image, var):
    row, col, ch = image.shape
    mean = 0
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = image + gauss
    cv2.normalize(noisy, noisy, 0, 255, cv2.NORM_MINMAX, dtype=-1)
    return noisy.astype(np.uint8)


def AddNoiseandBlur(base_path, final_path):
    list = os.listdir(base_path)
    i = 0
    for file in list:
        img = cv2.imread(os.path.join(base_path, file))
        kSize = np.random.randint(6)
        if 3 < kSize < 6:
            kSize = 3
        elif kSize == 6:
            kSize = 6
        else:
            kSize = 1
        blurImg = cv2.GaussianBlur(img, (kSize, kSize), cv2.BORDER_DEFAULT)
        noisyImg = Gaussian_Noise(blurImg, np.random.randint(0, 90))
        cv2.imwrite(os.path.join(final_path, file), noisyImg)
        i += 1


'''
base_path = 'C:\\Users\\juans\\PycharmProjects\\SyntheticImageBlender\\render_workspace\\ConFondoMesas\\Motor'
final_path = 'C:\\Users\\juans\\PycharmProjects\\SyntheticImageBlender\\render_workspace\\Finales\\Motor'
AddNoiseandBlur(base_path, final_path)
'''