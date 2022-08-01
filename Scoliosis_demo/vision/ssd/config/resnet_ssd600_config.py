import numpy as np

from vision.utils.box_utils_v2 import SSDSpec, SSDBoxSizes, generate_ssd_priors  ### Modification ###


image_size = 600
image_mean = np.array([127, 127, 127])  # RGB layout
image_std = 128.0
iou_threshold = 0.45
center_variance = 0.1
size_variance = 0.2

specs = [
    SSDSpec(19, 32, SSDBoxSizes(60, 105), [3]),
    SSDSpec(10, 60, SSDBoxSizes(105, 150), [3]),
    SSDSpec(5, 120, SSDBoxSizes(150, 195), [3]),
    SSDSpec(3, 200, SSDBoxSizes(195, 240), [3]),
    SSDSpec(2, 300, SSDBoxSizes(240, 285), [3])
]


priors = generate_ssd_priors(specs, image_size)