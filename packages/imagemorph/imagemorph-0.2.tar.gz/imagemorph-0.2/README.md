# imagemorph

This is a Python wrapper of the
[imagemorph](https://github.com/GrHound/imagemorph.c) [1] repository, a 
program to apply random elastic rubbersheet transforms to images for
augmenting training sets in machine learning/deep learning. 

Rather than running a compiled executable and
writing the resulting image to disk as in the original repo, this wrapper 
performs the same random elastic morphing as in the original repo, but 
instead returns the resulting image as a numpy array, which can then be 
used for further processing in, for example, a machine learning pipeline.

Any image type can be processed (not just .ppm), as long as it can be
loaded with OpenCV.

## How to install

Install using pip:

```
pip install imagemorph
```

## Example usage

```python
import cv2 as cv
from imagemorph import elastic_morphing

amp, sigma = 0.9, 9
img_name = "img/sample-input.png"

# load image
img = cv.imread(img_name)
h, w, _ = img.shape

# apply random elastic morphing
res = elastic_morphing(img, amp, sigma, h, w)

# write result to disk
cv.imwrite('img/out.png', res)
```

## References

Original Author: Marius Bulacu (.pgm version for characters). Adapted for .ppm
and color: Lambert Schomaker.

Please cite:

[1] M Bulacu, A Brink, T van der Zant, L Schomaker (2009).
Recognition of handwritten numerical fields in a 
large single-writer historical collection,
10th International Conference on Document Analysis and Recognition, 
pp. 808-812, DOI: 10.1109/ICDAR.2009.8 
