# Benchmark the different methods for OCR
from sklearn.metrics import accuracy_score 
import numpy as np
import re
from trader import * 
from separate_number import get_digits
import sklearn_digits
from PIL import Image
import matplotlib.pyplot as plt
data_folder = "data/"
filename = "etiquettes.csv"

# Using only pytessaract
def guess_lot(pic):
    lot_1   = read_image(filename = pic, box =
            (220,43,311,63)).replace("\n\x0c", "")
    lot_10  = read_image(filename = pic,  box =
            (220,85,311,105)).replace("\n\x0c", "")
    lot_100 = read_image(filename = pic,  box =
            (220,125,311,145)).replace("\n\x0c", "")
    #keep only digits
    lot_1 = re.sub('[^0-9]', '', lot_1)
    lot_10 = re.sub('[^0-9]', '', lot_10)
    lot_100 = re.sub('[^0-9]', '', lot_100)
    return lot_1, lot_10, lot_100

def get_most_frequent(l):
    if len(l) == 0:
        return ''
    cnt_map = {}
    max_c = l[0]
    max_cnt = 0
    for c in l:
        if c in cnt_map:
            cnt_map[c] += 1
            if cnt_map[c]>max_cnt:
                max_c = c
                max_cnt = cnt_map[c]
        else :
            cnt_map[c] = 0
    return max_c

# Using a trained KNN model
def guess_lot_handmade(f):
    clf = sklearn_digits.load_model("trained_knn") 
    d1 = get_digits(filename = f, box = (220,43,311,63))
    d10 = get_digits(filename = f, box = (220,85,311,105))
    d100 = get_digits(filename = f, box = (220,125,311,145))
    

    max_x, max_y, max_z= 9, 11, 3
    #same pad as knn is trained for
    X_1 = np.array([np.pad(d, [(0, max_x - d.shape[0]),
                               (0, max_y - d.shape[1]),
                               (0, max_z - d.shape[2])],
                           mode='constant').reshape(-1) for d in d1])
    X_10 = np.array([np.pad(d, [(0, max_x - d.shape[0]),
                               (0, max_y - d.shape[1]),
                               (0, max_z - d.shape[2])],
                           mode='constant').reshape(-1) for d in d10])
    X_100 = np.array([np.pad(d, [(0, max_x - d.shape[0]),
                               (0, max_y - d.shape[1]),
                               (0, max_z - d.shape[2])],
                           mode='constant').reshape(-1) for d in d100])
    y1, y10, y100 = ('','','')
    if(len(d1)>0):
        y1 = clf.predict(np.array(X_1))
    if(len(d10)>0):
        y10 = clf.predict(np.array(X_10))
    if(len(d100)>0):
        y100 = clf.predict(np.array(X_100))

    y_1reconstructed = "" 
    y_10reconstructed = "" 
    y_100reconstructed = "" 
    for y in y1:
        y_1reconstructed += y 
    for y in y10:
        y_10reconstructed += y 
    for y in y100:
        y_100reconstructed += y 
    return y_1reconstructed, y_10reconstructed, y_100reconstructed

# Using pytessaract on multiple images, 
# and outputting most frequent 
def guess_lot_mean(pic):
    lot_1_all = []
    lot_10_all = []
    lot_100_all = []
    for x_diff in [0]:
        for y_diff in [-2,-1,0,1,2]:
            l1 = read_image(filename = pic, box =
                             (220 +x_diff,
                              43  +y_diff,
                              311 +x_diff,
                              63  +y_diff)).replace("\n\x0c", "")
            l2 = read_image(filename = pic, box =
                           (220 +x_diff,
                            85  +y_diff,
                            311 +x_diff,
                            105 +y_diff)).replace("\n\x0c", "")
            l3 =read_image(filename = pic, box =
                         (220 +x_diff,
                          125 +y_diff,
                          311 +x_diff,
                          145 +y_diff)
                         ).replace("\n\x0c", "")

            l1 = re.sub('[^0-9]', '', l1)
            l2 = re.sub('[^0-9]', '', l2)
            l3 = re.sub('[^0-9]', '', l3)


            lot_1_all.append(l1)
            lot_10_all.append(l2)
            lot_100_all.append(l3)

    lot_1 = get_most_frequent(lot_1_all)
    lot_10 = get_most_frequent(lot_10_all)
    lot_100 = get_most_frequent(lot_100_all)
    return lot_1, lot_10, lot_100

def test_guess_fct(fct): 
    with open(data_folder+filename,"r") as f:
        lot_1X=[]
        lot_10X=[]
        lot_100X=[]

        lot_1Y=[]
        lot_10Y=[]
        lot_100Y=[]
        for line in f:
            pic, lot1, lot10, lot100 = line.replace('\n','').split(",")

            lot_1X.append(lot1)
            lot_10X.append(lot10)
            lot_100X.append(lot100)

            guessed_1, guessed_10, guessed_100 = fct(data_folder+pic+".png")
            lot_1Y.append(guessed_1)
            lot_10Y.append(guessed_10)
            lot_100Y.append(guessed_100)

            print(guessed_1,guessed_10,guessed_100)
            
            if lot1 != guessed_1 or lot10 != guessed_10 or lot100!= guessed_100:
                img=Image.open(data_folder+pic+".png")
                plt.imshow(img)
                plt.show()
    lot_stacked = lot_1X + lot_10X +lot_100X
    lot_guessed_stacked = lot_1Y + lot_10Y +lot_100Y


    for i in range(len(lot_stacked)):
        print(lot_stacked[i], lot_guessed_stacked[i])
    return accuracy_score(lot_stacked, lot_guessed_stacked)
        
if __name__ == '__main__':
    print(test_guess_fct(guess_lot_handmade))
