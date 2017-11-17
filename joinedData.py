import numpy as np

def read_data():
    """ read the data from whereever
        remove """
    data = np.genfromtxt('./data/joined.csv', delimiter=',')
    names = np.genfromtxt('./data/joined_names.csv', delimiter='@@@', dtype=None) 
    tags = np.genfromtxt('./data/joined_labels.csv', delimiter=',', dtype=None) 
    return (data, names, tags)


def to_color(num):
    if num <= -2:
        return 'red'
    if num == -1:
        return 'orange'
    if num == 0:
        return 'gray'
    if num == 1:
        return 'blue'
    if num >= 2:
        return 'green'