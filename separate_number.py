import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
import pandas

#separate on empty lines and big gaps ?
# gaps > 8pixel, on split sur celle ayant la plus petite comme ?
def separate(img):
    imgs = []
    if img.sum == 0:
        return img

    y_old = 0

    digits = []

    for y in range(img.shape[1]):
        if ( np.sum(img[:, y]) == 0 or y == img.shape[1]-1):
            if img[:, y_old:y+1, :].sum() == 0:
                continue
            digits.append(reshape(img[:, y_old:y+1, :]))
            y_old = y
    return digits

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
    return img[x_min:x_max+1, y_min:y_max+1]

def get_digits(filename:str, box):
    img=Image.open(filename)

    img=img.crop(box=box)
    np_img = np.array(img)

    #plt.imshow(np_img)
    #plt.show()

    np_img[np_img.min(axis=2)<125]=0
    np_img[np_img.min(axis=2)>=125]=255

    np_img = reshape(np_img)
    digits = separate(np_img)

    for d in digits:
        d=255-d

    return digits

# making a dataset from separated digits
if __name__ == '__main__':
    images = []
    etiquettes = []
    for i in range(100):#108
        f = "../data/out%.4d.png"%i
        try :
            d1 = get_digits(filename = f, box = (220,43,311,63))
        except :
            continue
        try:
            d10 = get_digits(filename = f, box = (220,85,311,105))
        except :
            continue
        try:
            d100 = get_digits(filename = f, box = (220,125,311,145))
        except :
            continue
        for d in d1:#, d10, d100:
            images.append(d)
            digit = np.pad(d, [(1, 1), (1, 1),(0,0)], mode='constant')
            plt.imshow(digit)
            plt.show(block=False)
            etiquettes.append(input())
            plt.close()

    np.save('dataset.csv', np.array([images,etiquettes]))

