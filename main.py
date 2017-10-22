from tsne import Reducer
from member import Member
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot

gen_size = 20

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

def read_data(file_name):
    """ read the data from whereever
        remove """
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
    return (data, names, columns, colors)

def create_first_generation(data):
    """
    Create the first generation of the data.
    Args:
        data (np.array): the matrix representing the input

    Returns:
        list of results: The generation of results with their respective quality and features."""
    rows = data.shape[0]
    columns = data.shape[1] 
    result = []
    for gen_member_index in range(0, gen_size):
        member = Member()
        result.append(member)
        vectors = [];
        for column_index in range(0, columns):
            if np.random.randint(0,2) > 0:
                member.features.append(column_index)
                vectors.append(data[:, column_index])
        member.map = np.column_stack(vectors)
    return result

def next_generation(data, current, colors):
    """
    Create the next generation from the previous one
    Args:
        data (np.array):    the matrix representing the input
        current (list):     the current generation 

    Returns:
        list: The generation of results with their respective quality and features."""
    for member in current:
        output = TSNE().fit_transform(member.map)
        x,y = output.T
        # matplotlib.pyplot.scatter(x,y, color = colors)
        # matplotlib.pyplot.show()
    # print (dataBase_emb)
    return []

if __name__ == '__main__':
    (data, names, columns, colors) = read_data('./data/20170929-180854_combined_data_try_0.csv')
    generation = create_first_generation(data)
    for iteration in range(0, 20):
        generation = next_generation(data, generation, colors)
    
    # the first result of the last generation is the best.