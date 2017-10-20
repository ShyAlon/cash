from tsne import Reducer
import pandas as pd

def read_data():
    """read the data from whereever"""
    return []

def create_first_generation(data):
    """
    Create the first generation of the data
    Args:
        data (np.array): the matrix representing the input

    Returns:
        list of results: The generation of results with their respective quality and features."""
    return []

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
    data = read_data()
    generation = create_first_generation(data)
    for iteration in range(0, 20):
        generation = next_generation(data, generation)
    
    # the first result of the last generation is the best.
