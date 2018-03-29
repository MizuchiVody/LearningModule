from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2


class ColorLabeler:
    def __init__(self):
        # initialiszing colors dictionary, containing the color
        # name as the key and the RGB tuple as the value
        colors = OrderedDict({"Red": (255, 0, 0),
                              "Green": (0, 255, 0),
                              "Blue": (0, 0, 255)})
        # Allocating memory for L*a*b image, then initializing the color name list
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []
        # Looping over the color dictionary
        for (i, (name, rgb)) in enumerate(colors.items()):
            # Updating the lab array and the color name list
            self.lab[i] = rgb
            self.colorNames.append(name)
        # Converting the lab array from RGB color space to lab
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def LabelTheColor(self, image, contour):
        # Constructing a mask for the contour,
        # then computing the average lab value for the masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]
        # initialize the minimum distance found so far
        minDist = (np.inf, None)
        for (i,row) in enumerate(self.lab):
            # computing the distance between the current lab color value and the mean og the image
            d = dist.euclidean(row[0], mean)
            # if the distance is smaller than the current distance, update the bookkeeping variable
            if d < minDist[0]:
                minDist =(d, i)

        return self.colorNames[minDist[1]]
