import numpy as np
from db import Database

def read_data(index):
    """ read the data from whereever
        remove """
    # file_name = './data/20171017-214145_combined_data_try_0.csv'
    db = Database()
    data_object = db.read_data(index)
    data = np.array(data_object["rows"].values())[:, 1:].astype(np.float)
    names = data_object["headers"]
    priceChange = data[:, 1]
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
