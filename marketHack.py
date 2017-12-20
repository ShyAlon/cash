import urllib2
import time
import getopt
import sys
import json
import csv
import os
from multiprocessing import Process, Queue

API_KEY = '114e933ff74d41b9f4bddeeb74c81ccd&symbol'
ITERATIONS = 5
CHUNK_SIZE = 100
SAMPLES = 100

def get_data(url, finished, counter):
    try:
        finished.put(urllib2.urlopen(url).read().strip())
    except Exception:
        print("failed retrieving url {}".format(counter))
        finished.put(0)
    return 0

def define_url():
    fields = ''
    global symbolList
    symbolList = []
    global urls
    global fieldList
    global sample_
    fieldList = []
    
    with open('resources/field_list.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            fieldList.append(row[0])
    
    for i in range(0, len(fieldList)):
        fields = fields +fieldList[i]+ ','
    
    with open('resources/snp_constituents.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            symbolList.append(row[0])
    
    symbols = ['', '', '', '', '']
    chunk_size = len(symbolList)/ITERATIONS
    for i in range(0, chunk_size):
        for offset in range(0, ITERATIONS):
            symbols[offset] = symbols[offset] + symbolList[offset * chunk_size + i]+','

    urls =[]
    for offset in range(0, ITERATIONS):
        suffix = (API_KEY, symbols[offset], fields)
        urls.append('http://marketdata.websol.barchart.com/getQuote.json?apikey=%s&symbols=%s&fields=%s' % suffix)

def create_files():
    stock_data = []
    del stock_data[:]

    fileNames = []
    runTime = time.strftime("%Y%m%d-%H%M%S")
    os.chdir("stockdata")
    os.makedirs(runTime)
    os.chdir(runTime)
    for i in range(0, len(symbolList)):
        fileNames.append(symbolList[i]+runTime+'.csv')

    filedata = {fileName: open(fileName, 'wb') for fileName in fileNames}
    finished = Queue()
    processes = []
    counter = 1

    for i in range(ITERATIONS):
        p = Process(target=get_data, args=(urls[i], finished, i))
        p.start()
        processes.append(p)
        time.sleep(1)
    
    while finished.qsize() < ITERATIONS:
        if counter % 10 == 0:
            print ("waiting for {} members to finish".format(ITERATIONS - finished.qsize()))
        counter += 1
        time.sleep(1)
    
    print ("done retrieving all urls")
    for i in range(0, ITERATIONS):
        stock_data.append(finished.get())
    # while not finished.empty():
    #     stock_data.append(finished.get())

    for process in processes:
        process.terminate()
    
    jsons = []
    for i in range(0, ITERATIONS):
        jsons.append(json.loads(stock_data[i]))
    
    results = []
    for i in range(0, ITERATIONS):
        results.append(jsons[i]["results"])

    writer = {k: csv.writer(filedata[fileNames[k]]) for k in range(0, len(fileNames))}
    for i in range(0, len(symbolList)):
        writer[i].writerow(results[0][0].keys())

    for sample in range(0, SAMPLES):
        finished = Queue()
        for i in range(ITERATIONS):
            p = Process(target=get_data, args=(urls[i], finished, i))
            p.start()
            processes.append(p)
            time.sleep(1)
        
        counter = 1
        while finished.qsize() < ITERATIONS:
            if counter % 10 == 0:
                print ("waiting for {} members to finish".format(ITERATIONS - finished.qsize()))
            counter += 1
            time.sleep(1)
        
        del stock_data[:]
        for i in range(0, ITERATIONS):
            stock_data.append(finished.get())
        
        # while not finished.empty():
        #     stock_data.append(finished.get())
        
        for process in processes:
            process.terminate()
        
        del jsons[:]
        for i in range(0, ITERATIONS):
            jsons.append(json.loads(stock_data[i]))

        del results[:]
        for i in range(0, ITERATIONS):
            results.append(jsons[i]["results"])

        for i in range(0, len(results[0])):
            for j in range(0, ITERATIONS):
                writer[i+j*len(symbolList)/5].writerow(results[j][i].values())
                
        print(sample)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
    except getopth.GetoptError, err:
        print (str(err))
        sys.exit(2)
    define_url()
    create_files()
    
if __name__ == "__main__":
    main()