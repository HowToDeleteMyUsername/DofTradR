#train a mmodel to do OCR
import pickle 
import numpy as np
import sklearn, matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


def preprocess(data_filename):
    array = np.load(data_filename, allow_pickle=True)
    X = array[0]
    y = array[1]

    X_clean = []
    y_clean = []

    for i in range(len(X)):
    #    ignore the non digits
    #    if y[i] == '.':
    #        continue
        X_clean.append(X[i])
        y_clean.append(y[i])

    max_x = 0
    max_y = 0
    max_z = 0
    for i in range(len(X_clean)):
        x_shape, y_shape, z_shape = tuple(X_clean[i].shape)
        max_x = max(x_shape, max_x)
        max_y = max(y_shape, max_y)
        max_z = max(z_shape, max_z)
    print(max_x,max_y,max_z) 
    exit(0)
    X_padded = np.zeros((len(X_clean) ,max_x*max_y*max_z))
    y_padded = np.array(y_clean).reshape(-1,)

    for i in range(len(X_clean)):
        x_shape, y_shape, z_shape = tuple(X_clean[i].shape)
        pad_x, pad_y,pad_z = max_x-x_shape, max_y-y_shape, max_z-z_shape 
        X_padded[i] = np.pad(X_clean[i], [(0, pad_x), (0, pad_y),(0,pad_z)],
                mode='constant').reshape(-1)

    return X_padded, y_padded

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    clf = KNeighborsClassifier(n_neighbors=1)
    clf.fit(X_train, y_train)
    return clf

def save_model(model, filename:str):
    pickle.dump(model, open(filename,"wb"))                      

def load_model(filename:str): 
    return pickle.load(open(filename, 'rb'))

if __name__ == "__main__":
    X,y = preprocess("dataset.csv.npy")
#    clf = train_model(X, y)
#    save_model(clf, 'trained_knn')
    clf = load_model("trained_knn")
    print("Score: %lf" % clf.score(X, y))
