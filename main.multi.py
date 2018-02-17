from tsne import Reducer
from member import Member
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import time
from mongoStockData import read_data
# from solarData import read_data
# from stockData import read_data
# from joinedData import read_data
# from bitterData import read_data
import json
import calendar
import traceback
import os
from glob import glob

gen_size = 20
iterations_per_file = 30

def create_full_member(data):
    member = Member()
    columns = data.shape[1]
    vectors = []
    for column_index in range(0, columns):
        member.features.append(column_index)
        vectors.append(data[:, column_index])
    member.map = np.column_stack(vectors)
    return member

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
    result = [create_full_member(data)]
    for gen_member_index in range(1, gen_size):
        new_member = create_new_member(data)
        result.append(new_member)

    # First member is always all the features

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

def get_nearest_points(point_index, x, y):
    distances = []
    for index in range(0, len(x)):
        if index != point_index:
            distance_squared = (x[point_index] - x[index])**2 + (y[point_index] - y[index])**2
            distances.append((index, distance_squared))
    distances.sort(key=lambda distance: distance[1])
    return distances

def order_by_quality(current, colors):
    finished = Queue(gen_size)
    started = 0
    processes = []
    for member in current:
        if member.quality == 0:
            # counter = 1
            # while started - finished.qsize() > 5:
            #     if counter % 10 == 0:
            #         print ("waiting {} seconds for other processes to finish in order to start".format(counter))
            #     time.sleep(1)
            #     counter += 1
            p = Process(target=set_quality, args=(member, colors, finished, started))
            p.start()
            started += 1
            processes.append(p)
            time.sleep(5)
        else:
            finished.put(member)

    counter = 1
    del current[:]

    while len(current) < gen_size:
        if not finished.empty():
            current.append(finished.get())
        else:
            if counter % 10 == 0:
                print ("waiting for {} members to finish".format(gen_size - len(current)))
            counter += 1
            time.sleep(1)

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
            if colors[point_index] != "gray" and colors[point_index] != "black":
                total += 1.0
                nearest_index = get_nearest_point(point_index, x, y)
                if colors[nearest_index] == colors[point_index]:
                    ratio += 1.0
        member.quality = ratio / total
        for point_index in range(0, len(x)):
            if colors[point_index] == "gray":
                nearest_indice = get_nearest_points(point_index, x, y)
                recommendations = 0
                for i in range(0, 3):
                    if colors[nearest_indice[i][0]] == "lime":
                        recommendations += 1
                if recommendations > 1:
                    colors[point_index] = "black"
                    member.recommendations.append(point_index)
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

def handleDb(file_counter):
    (data, names, colors, assets, date_and_time) = read_data(file_counter)
    last_quality = 0
    no_improvement = 0
    generation = create_first_generation(data, colors)
    for iteration in range(0, iterations_per_file):
        try:
            generation = next_generation(data, generation, colors)
            print ("***\nFinished generation {}\n***").format(iteration)
            directory = "./results/{}".format(date_and_time)
            if not os.path.exists(directory):
                os.makedirs(directory)
            now = calendar.timegm(time.gmtime())
            if generation[0].quality > last_quality:
                last_quality = generation[0].quality
                temp_colors = list(colors)
                for recommended in generation[0].recommendations:
                    temp_colors[recommended] = "black"
                no_improvement = 0
                plt.gcf().clear()
                colorSet = set(temp_colors)
                colorCollections = {}
                for color in colorSet:
                    colorCollections[color] = {"x": [], "y": []}

                for i in range(0, len(generation[0].x)):
                    colorCollections[temp_colors[i]]["x"].append(generation[0].x[i])
                    colorCollections[temp_colors[i]]["y"].append(generation[0].y[i])

                for color in colorSet:
                    plt.scatter(colorCollections[color]["x"], colorCollections[color]["y"], color=color, label=color)

                plt.legend()
                plt.savefig("./results/{}/result_{}_{}_{}.png".format(date_and_time, file_counter, now, generation[0].quality))

                with open('./results/{}/generation_{}_{}_{}_{}.json'.format(date_and_time, file_counter, now, iteration,
                                                                         generation[0].quality), 'w') as fp:
                    save_me = []
                    for member in generation:
                        recommendations = []
                        for x in member.recommendations:
                            try:
                                recommendations.append({
                                        "name": assets[x],
                                        "index": x,
                                        "coordinates": {
                                            "x": member.x[x],
                                            "y": member.y[x]
                                        }
                                    })
                            except Exception as ex:
                                print("failed aooending recommendation {}".format(ex))
                                tb = traceback.format_exc()
                                print(tb)
                        save_me.append({
                            "features": member.features,
                            "quality": member.quality,
                            "recommendations": recommendations
                        })
                    json.dump(save_me, fp)
            else:
                no_improvement += 1
                if no_improvement > 8:  # 4 generations didn't budge
                    print("no improvement - quitting")
                    break
        except Exception as e:
            print("failed calculating next generation {}".format(e))
            tb = traceback.format_exc()
            print(tb)


if __name__ == '__main__':
    for i in range(0, 1):
        handleDb(i)
    #
    # files = glob("./data/old/4*.csv")
    # file_counter = 0
    # for data_file in files:
    #     file_counter += 1
    #     handleDb(file_counter, data_file)

    # the first result of the last generation is the best.