import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract

def reshape(img):
    x_min, y_min = 0, 0

    while np.sum(img[x_min,:]) == 0 and x_min < img.shape[0]-2:
        x_min += 1

    while np.sum(img[:,y_min]) == 0 and y_min < img.shape[1]-2:
        y_min += 1

    x_max, y_max = img.shape[0]-1, img.shape[1]-1
    while np.sum(img[x_max,:]) == 0 and x_max >= x_min + 1:
        x_max -= 1

    while np.sum(img[:,y_max]) == 0 and y_max >= y_min + 1:
        y_max -= 1
    print(x_min-1,y_min-1)
    return img[x_min-8:x_max+9, y_min-3:y_max+4]

def read_image(filename:str, box, reshape_allowed=False):
    img=Image.open(filename)
    img=img.crop(box=box)
    np_img = np.array(img)

    #plt.imshow(np_img)
    #plt.show()

    np_img[np_img.min(axis=2)<125]=0
    np_img[np_img.min(axis=2)>=125]=255

    if reshape_allowed:
        np_img = reshape(np_img)
    np_img=255-np_img

    img=Image.fromarray(np_img)

    text = pytesseract.image_to_string(img, config='--oem 1 --psm 6')
    img.close()
    return text
