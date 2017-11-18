import urllib2, time, getopt, sys, json, csv, os

API_KEY = '114e933ff74d41b9f4bddeeb74c81ccd&symbol'
ITERATIONS = 5
CHUNK_SIZE = 100

def get_data(url):
    try:
        data = urllib2.urlopen(url).read()
    except:
        return 'cant open url'
    try:
        data = data.strip()
    except:
        return 'cant strip url output'
    return data

def define_url():
    fields = ''
    global symbolList
    symbolList = []
    global url
    global fieldList
    global sample_
    fieldList = []
    with open('field_list.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            fieldList.append(row[0])
    for i in range(0,len(fieldList)):
        fields = fields +fieldList[i]+ ','
    with open('snp_constituents.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            symbolList.append(row[0])
    symbols = ['','','','','']
    chunk_length = len(symbolList)/ITERATIONS
    for i in range(0, len(symbolList)/ITERATIONS):
        for offset in range(0, 5):
            symbols[offset] = symbols[offset] + symbolList[offset * chunk_length + i]+','

    url = []
    for offset in range(0, 5):
        suffix = (API_KEY, symbols[offset], fields)
        url.append('http://marketdata.websol.barchart.com/getQuote.json?apikey=%s&symbols=%s&fields=%s' % suffix)

def create_files():
    fileNames = []
    runTime = time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(runTime)
    os.chdir(runTime)
    for i in range(0,len(symbolList)):
        fileNames.append(symbolList[i]+runTime+'.csv')
    filedata = {fileName: open(fileName, 'wb') for fileName in fileNames}
    stock_data = []
    for index in range(0, 5):
        stock_data.append(get_data(url[index]))

    jsons = []
    for index in range(0, 5):
        jsons.append(json.loads(stock_data[index]))

    results = []
    for index in range(0, 5):
        results.append(jsons[index]["results"])

    writer = {k: csv.writer(filedata[fileNames[k]]) for k in range(0, len(fileNames))}
    for i in range(0,len(symbolList)):
        writer[i].writerow(results[0][0].keys())

    ***** Refcator this ******
    for sample in range(0, CHUNK_SIZE):
        for chunk in range(0, ITERATIONS):
            for i in range(0, len(results[chunk])):
                writer[i].writerow(results[chunk][i].values())
                writer[i+len(symbolList)/5].writerow(results2[i].values())
                writer[i+2*len(symbolList)/5].writerow(results3[i].values())
                writer[i+3*len(symbolList)/5].writerow(results4[i].values())
                writer[i+4*len(symbolList)/5].writerow(results5[i].values())
            print(sample)


    for sample in range(0,100):
        for i in range(0,len(results1)):
            writer[i].writerow(results1[i].values())
            writer[i+len(symbolList)/5].writerow(results2[i].values())
            writer[i+2*len(symbolList)/5].writerow(results3[i].values())
            writer[i+3*len(symbolList)/5].writerow(results4[i].values())
            writer[i+4*len(symbolList)/5].writerow(results5[i].values())
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
