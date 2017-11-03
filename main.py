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

def create_new_member(data):
    member = Member()
    columns = data.shape[1] 
    vectors = []
    for column_index in range(0, columns):
        if np.random.randint(0,2) > 0:
            member.features.append(column_index)
            vectors.append(data[:, column_index])
    member.map = np.column_stack(vectors)
    return member

def create_first_generation(data, colors):
    """
    Create the first generation of the data.
    Args:
        data (np.array): the matrix representing the input

    Returns:
        list of results: The generation of results with their respective quality and features."""
    rows = data.shape[0]
    result = []
    for gen_member_index in range(0, gen_size):
        result.append(create_new_member(data))

    order_by_quality(result, colors)
    return result

def get_nearest_point(point_index, x, y):
    result = -1
    min_distance = float("inf")
    for index in range(0, len(x)):
        if index != point_index:
            distance_squared = (x[point_index] - x[index])**2 + (y[point_index] - y[index])**2 
            if distance_squared < min_distance:
                result = index
                min_distance = distance_squared
    return result

def order_by_quality(current, colors):
    for member in current:
        set_quality(member, colors)

    current.sort(key = lambda x: x.quality, reverse=True)
    print("Top quality {}".format(current[0].quality))

def set_quality(member, colors):
    output = TSNE().fit_transform(member.map)
    x,y = output.T
    member.x = x
    member.y = y
    total = 0.0
    ratio = 0.0
    for point_index in range(0, len(x)):
        if colors[point_index] != "gray":
            total += 1.0
            nearest_index = get_nearest_point(point_index, x, y)
            if colors[nearest_index] == colors[point_index]:
                ratio += 1.0
    member.quality = ratio / total

def cross_breed(father, mother, data):
    member = Member()
    features = list(set(mother.features + father.features))
    vectors = []
    for column_index in range(0, len(features)):
        if np.random.randint(0,2) > 0:
            member.features.append(column_index)
            vectors.append(data[:, column_index])
    member.map = np.column_stack(vectors)
    return member

def next_generation(data, current, colors):
    """
    Create the next generation from the previous one
    Args:
        data (np.array):    the matrix representing the input
        current (list):     the current generation 

    Returns:
        list: The generation of results with their respective quality and features."""
    next = []
    for copies in range(0, gen_size/3):
        next.append(current[copies])

    for cross in range(0, gen_size/4):
        next.append(cross_breed(current[cross], current[cross+1], data))
        next.append(cross_breed(current[cross], current[cross+2], data))
    
    for new in range(0, gen_size - len(next)):
        next.append(create_new_member(data))

    order_by_quality(next, colors)
       
    # print (dataBase_emb)
    return next

if __name__ == '__main__':
    (data, names, columns, colors) = read_data('./data/20171017-214145_combined_data_try_0.csv')
    generation = create_first_generation(data, colors)
    for iteration in range(0, 20):
        generation = next_generation(data, generation, colors)
    
    matplotlib.pyplot.scatter(generation[0].x,generation[0].y, color = colors)
    matplotlib.pyplot.show()
    # the first result of the last generation is the best.