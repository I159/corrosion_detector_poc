import os
import sys

import colorsys
import numpy as np
from scipy import misc, signal
from skimage.feature import greycomatrix, greycoprops


ROUGH_TH = .5
WHITE_S_TH = 0.2
WHITE_V_TH = 252
BLACK_V_TH = 0.2


def pixel_patches(file_path, size=32):
    grey = misc.imread(file_path, mode='L')
    for i in range(0, grey.shape[0], 8):
        for j in range(0, grey.shape[1], 8):
            grey_patch = grey[i: i+8, j: j+8]
            yield grey_patch, (i, i+8, j, j+8)


def energy(patches):
    for patch, coordinates in patches:
        glcm = greycomatrix(patch, [5], [0, np.pi/2], 256, normed=True)
        yield greycoprops(glcm, 'energy'), coordinates


def rough_patches(file_path):
    p = pixel_patches(file_path)
    energy_coords = energy(p)

    for enr, coords in energy_coords:
        if np.any(np.greater(enr, np.array(ROUGH_TH))):
            yield coords


def get_hsv_matrix(file_path):
    colorful = misc.imread(file_path, mode='RGB')
    return np.array([[colorsys.rgb_to_hsv(*j) for j in i] for i in colorful])


def patch_detect(crds, hsv):
    lower_white_mask = np.array([0, 0, 80])
    upper_white_mask = np.array([360, 25, 100])

    lower_black_mask = np.array([0, 0, 0])
    upper_black_mask = np.array([360, 100, 5])


    # TODO:
    # Smooth with Gaussian Filter
    # Apply cv2 masks to determine rust color range
    # Calculate percetage of rotten area in a patch
    raise NotImplementedError


def item_detect(file_path):
    hsv = get_hsv_matrix(file_path)
    patches = rough_patches(file_path)
    corroded = [patch_detect(i, hsv) for i in patches]


def data_set(path):
    data_set_info = next(os.walk(path))
    return (os.path.join(data_set_info[0], i) for i in data_set_info[2])


if __name__ == "__main__":
    ds = data_set(sys.argv[1])
    for j in ds:
        item_detect(j)
