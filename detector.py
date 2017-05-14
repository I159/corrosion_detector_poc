import os
import sys

from scipy import misc, signal
from skimage.feature import greycomatrix, greycoprops


def pixel_patches(file_path, size=32):
    arr = misc.imread(file_path)
    for i in range(0, arr.shape[0], 8):
        for j in range(0, arr.shape[1], 8):
            patch = arr[i: i+8, j: j+8]
            yield patch.reshape(patch.shape[0]*patch.shape[1], patch.shape[2])


def glcm(patches):
    for patch in patches:
        glcm = greycomatrix(patch, [5], [0], 256, symmetric=True, normed=True)
        yield greycoprops(glcm, 'energy')


def iter_images(path):
    data_set_info = next(os.walk(path))
    data_set = [os.path.join(data_set_info[0], i) for i in data_set_info[2]]
    for i in data_set:
        p = pixel_patches(i)
        g = glcm(p)

        for v in g:
            if v[0][0] != 0:
                print("Hooray!")

if __name__ == "__main__":
    iter_images(sys.argv[1])
