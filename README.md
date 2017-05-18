# Weak-classifier Colour-based Corrosion Detector (WCCD)

WCCD is a supervised classifier which has been built around a cascade scheme, although its
two stages can be considered as weak classifiers. The idea is to chain different fast classifiers
with poor performance in order to obtain a global classifier attaining a much better global
performance. To this end, each weak classifier takes profit from different features of the items
to classify, reducing the number of false positive detections at each stage. For a good global
performance, the classifiers must present a false negative percentage close to zero.
The first stage of the cascade is based on the premise that a corroded area presents
a rough texture. Roughness is then related to the energy of the symmetric gray-level
co-occurrence-matrix (GLCM).

The second stage filters the pixels of the patches that have passed the roughness stage. This
stage makes use of the colour information that can be observed from corroded areas. More
precisely, the classifier works over the Hue-Saturation-Value (HSV) space after the realization
that HSV-values that can be observed in corroded areas are confined in a bounded subspace
of the HS plane. Although the V component has been observed neither significant nor
necessary to describe the color of corrosion, it is used to prevent the well-known instabilities
in the computation of hue and saturation when color is close to white or black. In that case,
the pixel is classified as non-corroded.
A training step is performed prior to the application of this second stage of the corrosion
classifier. In this case, training consists of building a bi-dimensional histogram of HS values
for image pixels known to be affected by corrosion in the training image set. The resulting
histogram is subsequently filtered by zeroing entries whose value is below a threshold value of the highest
peak.

Data set formed from free pictures from Google Images: https://www.dropbox.com/sh/wbn5xraxqn3x8dq/AADnFTO_8V_HMd4lsshtkF6La?dl=0
