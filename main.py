from tsne import Reducer
from member import Member
import numpy as np

gen_size = 20

def read_data():
    """read the data from whereever"""
    return np.random.rand(10,7)

def create

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

def next_generation(data, current):
    """
    Create the next generation from the previous one
    Args:
        data (np.array):    the matrix representing the input
        current (list):     the current generation 

    Returns:
        list: The generation of results with their respective quality and features."""
    return []

if __name__ == '__main__':
    main_data = read_data()
    generation = create_first_generation(main_data)
    for iteration in range(0, 20):
        generation = next_generation(main_data, generation)
    
    # the first result of the last generation is the best.
    