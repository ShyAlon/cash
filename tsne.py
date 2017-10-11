import numpy as np
from sklearn.manifold import TSNE

class Reducer:
    def __init__(self):
         self.r = 0
         self.i = 0

    def process(self):
        X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
        X_embedded = TSNE(n_components=2).fit_transform(X)
        return X_embedded.shape