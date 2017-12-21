import numpy as np

def to_color(name): #Ag Co Cu Ni
    if name == 'Ag' :
        return 'blue'
    elif name == 'Co':
        return 'red'
    elif name == 'Cu':
        return 'yellow'
    else:
        return 'green'

def read_data():
    """ read the data from whereever
        remove """
    all = np.genfromtxt('./data/solar.csv', delimiter=',')
    data = all[1:, 2:]
    txt = np.genfromtxt('./data/solar.csv', delimiter=',', dtype=None)
    names = txt[1:, 0]
    tags = txt[1:, 1]
    vfunc = np.vectorize(to_color)
    colors = vfunc(tags)
    return (data, names, colors)