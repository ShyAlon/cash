import numpy as np

def read_data(file_name):
    """ read the data from whereever
        remove """
    # file_name = './data/20171017-214145_combined_data_try_0.csv'
    raw = np.genfromtxt(file_name,delimiter=',')
    data = raw[1:, 2:]
    strings = np.genfromtxt(file_name,delimiter=',', dtype=None)
    names = strings[1:, 0]
    tags = strings[1:, 1]
    vfunc = np.vectorize(to_color)
    colors = vfunc(tags)
    return (data, names, colors)

def to_color(num):
    if num == "Ag":
        return 'red'
    if num == "Co":
        return 'orange'
    if num == "Cu":
        return 'blue'
    if num == "Ni":
        return 'lime'
