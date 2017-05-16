import os
import sys

import colorsys
import numpy as np
from scipy import misc, signal
from skimage.feature import greycomatrix, greycoprops


TH = .5


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


def data_set(path):
    data_set_info = next(os.walk(path))
    return (os.path.join(data_set_info[0], i) for i in data_set_info[2])


def rough_patches(image):
    p = pixel_patches(image)
    energy_coords = energy(p)

    for enr, coords in energy_coords:
        if np.any(np.greater(enr, np.array(TH))):
            yield coords


def get_hsv_matrix(file_path):
    colorful = misc.imread(file_path, mode='RGB')
    return np.apply_along_axis(lambda x: colorsys.rgb_to_hsv(*x), 2, colorful)


if __name__ == "__main__":
    ds = data_set(sys.argv[1])
    for j in ds:
        cl = get_hsv_matrix(j)
        import pdb
        pdb.set_trace()
        # for i in rough_patches(j):
            # print(i)
