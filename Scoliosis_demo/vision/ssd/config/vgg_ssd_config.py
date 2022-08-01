import numpy as np

from vision.utils.box_utils_v2 import SSDSpec, SSDBoxSizes, generate_ssd_priors


image_size = 300
image_mean = np.array([123, 117, 104])  # RGB layout
image_std = 1.0

iou_threshold = 0.45
center_variance = 0.1
size_variance = 0.2

# specs = [
#     SSDSpec(38, 8, SSDBoxSizes(30, 60), [3]),   ### 2
#     SSDSpec(19, 16, SSDBoxSizes(60, 111), [3]),   ### 2,3
#     SSDSpec(10, 32, SSDBoxSizes(111, 162), [3]),  ### 2,3
#     SSDSpec(5, 64, SSDBoxSizes(162, 213), [3]),   ### 2,3
#     SSDSpec(3, 100, SSDBoxSizes(213, 264), [3]),     ### 2
#     SSDSpec(1, 300, SSDBoxSizes(264, 315), [3])      
# ]

specs = [
    SSDSpec(38, 8, SSDBoxSizes(30, 60), [2]),   ### 2
    SSDSpec(19, 16, SSDBoxSizes(60, 111), [2]),   ### 2,3
    SSDSpec(10, 32, SSDBoxSizes(111, 162), [2]),  ### 2,3
    SSDSpec(5, 64, SSDBoxSizes(162, 213), [2]),   ### 2,3
    SSDSpec(3, 100, SSDBoxSizes(213, 264), [2]),     ### 2
    SSDSpec(1, 300, SSDBoxSizes(264, 315), [2])      
]


priors = generate_ssd_priors(specs, image_size)