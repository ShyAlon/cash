import numpy as np

def to_color(name):
    if name == 'Non-Bitter' :
        return 'blue'
    else:
        return 'green'

def read_data():
    """ read the data from whereever
        remove """
    all = np.genfromtxt('./data/bitter dataBase.csv', delimiter=',')
    data = all[1:, 4:]
    txt = np.genfromtxt('./data/bitter dataBase.csv', delimiter=',', dtype=None)
    columns = txt[0, :]
    names = txt[1:, 1]
    tags = txt[1:, 3]
    vfunc = np.vectorize(to_color)
    colors = vfunc(tags)
    return (data, names, colors)

