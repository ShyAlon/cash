import numpy as np

def read_data(file_name):
    """ read the data from whereever
        remove """
    # file_name = './data/20171017-214145_combined_data_try_0.csv'
    raw = np.genfromtxt(file_name,delimiter=',')
    data = raw[3:, 1:]
    strings = np.genfromtxt(file_name,delimiter=',', dtype=None)
    names = strings[1:, 0]
    columns = strings[0, 3:]
    priceChange = raw[1:, 2]
    mean = priceChange.mean()
    std = priceChange.std()
    priceDev = (priceChange - mean) / std
    tags = (priceDev > 2).astype(int)
    tags = tags + (priceDev > 1).astype(int)
    tags = tags - (priceDev < -1).astype(int)
    tags = tags - (priceDev < -2).astype(int)
    vfunc = np.vectorize(to_color)
    colors = vfunc(tags)
    return (data, names, colors)

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
        return 'lime'
