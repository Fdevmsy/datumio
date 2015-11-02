"""
Test image transformations from transforms to see if they're doing exactly
what we're want...
"""

import datumio.transforms as dtf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# load up image
img_path = 'test_data/cat.jpg'
img = np.array(Image.open(img_path, mode = 'r'))

# set up augmentation parameters
hw = (img.shape[0], img.shape[1])
crop_percentage = 0.5
crop_hw = (hw[0] - int(hw[0]*crop_percentage), hw[1] - int(hw[1]*crop_percentage))

augmentation_params = dict( rotation = 45,
                            zoom = (0.5, 2.),
                            shear = 45,
                            translation = (int(hw[0]*0.1), -int(hw[1]*0.1)),
                            flip_lr = True,
                            )
augmentation_keys = augmentation_params.keys()
nAugmentations = len(augmentation_params)

# set up plotting. nPlots = original image + len(augmentations) + all_augment + all_augment_crop
nPlots = nAugmentations + 3
nrows = int(np.ceil(np.sqrt(nPlots)))
ncols = int(np.ceil(nPlots/float(nrows)))

fig, axes = plt.subplots(nrows= nrows, ncols= ncols, num = 1)
axes = axes.flatten()

# Plot the original image
axes[0].imshow(img)
axes[0].set_title("Original Image")

# Plot each augmentation parameter, isolated
for it, (key, param) in enumerate(augmentation_params.iteritems()):
    ax = axes[it + 1]
    augmentation_param = {key: param}
    
    # transform image
    img_wf = dtf.transform_image(img, **augmentation_param)
    
    # plot image
    ax.imshow(img_wf.astype(np.uint8))
    ax.set_title("Augmentation Param: %s = %s"%(key, param))
    ax.set_xticks([])
    ax.set_yticks([])

# plot image with all augmentations at once
ax = axes[it + 1]
img_wf = dtf.transform_image(img, **augmentation_params)
ax.imshow(img_wf.astype(np.uint8))
ax.set_title("All Augmentations")
ax.set_xticks([])
ax.set_yticks([])

# plot image with all augmentations & center crop
ax = axes[it + 2]
img_wf = dtf.transform_image(img, output_shape=crop_hw, **augmentation_params)
ax.imshow(img_wf.astype(np.uint8))
ax.set_title("All Augmentation + Crop")