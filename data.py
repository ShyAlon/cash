import urllib2, time, getopt, sys, json, csv, os, math, numpy
from sklearn.manifold import TSNE
import matplotlib.pyplot

def readFile(file_name):
    colors = []
    price_change = []
    with open(file_name, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            price_change.append(float(row['priceChange%']))
        avg_price_change = numpy.mean(price_change)
        std_price_change = numpy.std(price_change)
        print (avg_price_change, std_price_phange)
    with open(file_name, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            change = float(row['priceChange%'])
            if change > avg_price_change + 2*std_price_change:
                
            
            if float(row['priceChange%']) < avg_price_change-std_price_phange:
                colors.append('red')
            else:
                if float(row['priceChange%']) > avg_price_change+std_price_phange:
                    colors.append('green')
                else:
                    colors.append('yellow')              
    print (colors)
    return 

def readDatabase():
    os.chdir("..")
    os.chdir(timeTag)
    fileName = '%s_combined_data_try_0.csv' %timeTag
    colors = []
    priceChange = []
    with open(fileName, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            priceChange.append(float(row['priceChange%']))
        avgPriceChange = numpy.mean(priceChange)
        varPriceChange = numpy.var(priceChange)
        print (avgPriceChange, varPriceChange)
    with open(fileName, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if float(row['priceChange%']) < avgPriceChange-varPriceChange:
                colors.append('red')
            else:
                if float(row['priceChange%']) > avgPriceChange+varPriceChange:
                    colors.append('green')
                else:
                    colors.append('yellow')              
    print (colors)
    # inputFileName = '%s_combined_data_try_0.csv' %timeTag
    # outputFileName = '%s_dataOnly.csv' %timeTag
    # with open (inputFileName, 'rb') as inputFile:
    #     reader = csv.reader(inputFile)
    #     with open (outputFileName, 'wb') as outputFile:
    #         inputFile.next()
    #         writer = csv.writer(outputFile)
    #         for row in reader:
    #             writer.writerow((row[3],row[4]))
    dataBase = numpy.genfromtxt (fileName, skip_header=1, usecols= range(3,42) , delimiter=",")
    print (dataBase)
    dataBase_emb = TSNE().fit_transform(dataBase)
    x,y = dataBase_emb.T
    matplotlib.pyplot.scatter(x,y, color = colors)
    matplotlib.pyplot.show()
    print (dataBase_emb)

def main():
    global timeTag
    timeTag = '20170929-163244'
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
    # except getopth.GetoptError, err:
    #     print (str(err))
    #     sys.exit(2)
    readDatabase()
    
if __name__ == "__main__":
    main()
    print ('done')