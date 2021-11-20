#Print resource prices
from utils import * 
from read import read_image
import time
from separate_number import get_digits
import numpy as np
import OCR

def cleanup_lot(lot_price:str):
    return lot_price.replace(" ","").replace(".","")


def screen_price(out, win:str):
    screen_capture(width=470, height=160, x=430, y=152,
                   window=win,out=out)

    clf = sklearn_digits.load_model("trained_knn") 
    d1 = get_digits(filename = out, box = (220,43,311,63))
    d10 = get_digits(filename = out, box = (220,85,311,105))
    d100 = get_digits(filename = out, box = (220,125,311,145))

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

def search_resource(resource:str, win:str):
    click(690,350, window=win)
    time.sleep(3)
    click(230, 152, window=win)

    type_in_win(resource, window=win)
    time.sleep(3)
    click(650, 160, window=win)
    time.sleep(1)
    echap(win)
    return screen_price("tmp.png", win)

def read_resource_list(filename:str):
    with open(filename, 'r') as f:
        output = f.read().split('\n')
    return output

if __name__ == "__main__":
    win = get_window_by_name("Dofus 2")[0]
    focus(win)
    #move to 0 0
    for res in read_resource_list('resource.txt'):
        res = res.replace(" ","\ ")
        res = res.replace("\'","\\\'")
        prices = search_resource(res, win)
        print(res, prices)
