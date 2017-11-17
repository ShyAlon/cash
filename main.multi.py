from tsne import Reducer
from member import Member
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import time
from stockData import read_data
# from joinedData import read_data
# from bitterData import read_data
import json
import calendar

gen_size = 20

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
        new_member = create_new_member(data)
        result.append(new_member)

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
    finished = Queue()
    started = 0
    processes = []
    for member in current:
        if member.quality == 0:
            counter = 1
            while started - finished.qsize() > 5:
                if counter % 10 == 0:
                    print ("waiting {} seconds for other processes to finish in order to start".format(counter))
                time.sleep(1)
                counter += 1
            p = Process(target=set_quality, args=(member, colors, finished, started))
            p.start()
            started += 1
            processes.append(p)
        else:
            finished.put(member)

    counter = 1
    while finished.qsize() < gen_size:
        if counter % 10 == 0:
            print ("waiting for {} members to finish".format(gen_size - finished.qsize()))
        counter += 1
        time.sleep(1)

    del current[:]
    while not finished.empty():
        current.append(finished.get()) # data is OK

    for process in processes:
        process.terminate()

    current.sort(key=lambda x: x.quality, reverse=True) # still ok
    print("Top quality {}".format(current[0].quality))


def set_quality(member, colors, finished, started):
    try:
        print("starting calculating t-SNE member {}".format(started))
        output = TSNE().fit_transform(member.map)
        x,y = output.T
        member.set_x(x)
        member.set_y(y)
        total = 0.0
        ratio = 0.0
        for point_index in range(0, len(x)):
            if colors[point_index] != "gray":
                total += 1.0
                nearest_index = get_nearest_point(point_index, x, y)
                if colors[nearest_index] == colors[point_index]:
                    ratio += 1.0
        member.quality = ratio / total
        print("finished calculating t-SNE member {} quality {}".format(started, member.quality))
        finished.put(member)
    except Exception :
        print("failed calculating t-SNE member {}".format(started))
        member.quality = 0
        finished.put(member)
    return 0

def cross_breed(father, mother, data):
    member = Member()
    features = list(set(mother.features + father.features))
    vectors = []
    for column_index in range(0, len(features)):
        if features[column_index] in mother.features and features[column_index] in father.features:
            member.features.append(column_index)
            vectors.append(data[:, column_index])
        elif np.random.randint(0,2) > 0:
            member.features.append(column_index)
            vectors.append(data[:, column_index])
    member.map = np.column_stack(vectors)
    return member

def mutate(source, data):
    member = Member()
    vectors = []
    random = create_new_member(data)
    for column_index in range(0, len(source.features)):
        if  np.random.randint(0, 10) > 3:
            member.features.append(column_index)
            vectors.append(data[:, column_index])
    for column_index in range(0, len(random.features)):
        if np.random.randint(0, 10) > 6:
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
    
    for mutant in range(0, gen_size - len(next)):
        next.append(mutate(current[mutant], data))

    order_by_quality(next, colors)
       
    # print (dataBase_emb)
    return next

if __name__ == '__main__':
    (data, names, colors) = read_data()
    last_quality = 0
    no_improvement = 0
    generation = create_first_generation(data, colors)
    for iteration in range(0, 10):
        generation = next_generation(data, generation, colors)
        print ("***\nFinished generation {}\n***").format(iteration)
        now = calendar.timegm(time.gmtime())
        plt.scatter(generation[0].x, generation[0].y, color=colors)
        plt.savefig("./results/result{}_{}.png".format(now, generation[0].quality))
        with open('./results/generation_{}_{}.json'.format(now, iteration, generation[0].quality), 'w') as fp:
            save_me = []
            for member in generation:
                save_me.append({
                    "features": member.features,
                    "quality": member.quality
                })
            json.dump(save_me, fp)
        if generation[0].quality > last_quality:
            last_quality = generation[0].quality
            no_improvement = 0
        else:
            no_improvement += 1
            if no_improvement > 8: # 4 generations didn't budge
                print("no improvement - quitting")
                break
    plt.show()
    # the first result of the last generation is the best.