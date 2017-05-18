import os
import sys

import colorsys

sys.path.append('/usr/local/lib/python3.5/site-packages')

import cv2
import numpy as np
from scipy import misc, signal, ndimage
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
    i, j, v, k = crds
    patch = ndimage.filters.gaussian_filter(hsv[i:j, v:k], np.std(hsv[i:j, v:k]))

    lower_white_mask = np.array([0, 0, 80])
    upper_white_mask = np.array([360, 25, 100])
    white = cv2.inRange(patch, lower_white_mask, upper_white_mask)

    lower_black_mask = np.array([0, 0, 0])
    upper_black_mask = np.array([360, 100, 10])
    black = cv2.inRange(patch, lower_black_mask, upper_black_mask)

    lower_rust_mask = np.array([0, 30, 10])
    upper_rust_mask = np.array([35, 80, 65])
    rust = cv2.inRange(patch, lower_rust_mask, upper_rust_mask)

    out_patch = patch.copy()

    out_patch[np.where(white!=0)] = 0
    out_patch[np.where(black!=0)] = 0
    out_patch[np.where(rust==0)] = 0

    nonzero = np.count_nonzero(out_patch)

    if nonzero > 0:
        if nonzero / (nonzero/100) >= 50:
            return crds


def item_detect(file_path):
    hsv = get_hsv_matrix(file_path)
    patches = rough_patches(file_path)
    corroded = []
    for i in patches:
        prediction = patch_detect(i, hsv)
        if prediction:
            corroded.append(prediction)

    if corroded:
        print(corroded)


def data_set(path):
    data_set_info = next(os.walk(path))
    return (os.path.join(data_set_info[0], i) for i in data_set_info[2])


if __name__ == "__main__":
    ds = data_set(sys.argv[1])
    for j in ds:
        item_detect(j)
