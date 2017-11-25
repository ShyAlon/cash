import urllib2, time, getopt, sys, csv, os, math, numpy
import MySQLdb
from db import Database
import json

def get_info():
    global timeTag
    timeTag = "20171113-201721"
    global sampleCount
    sampleCount = 60
    global fieldCount
    fieldCount = 46
    global symbolCount
    symbolCount = 500
    global symbolList
    symbolList = []
    global fieldOfBusiness
    fieldOfBusiness = []
    with open('resources/snp_constituents.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            symbolList.append(row[0])
            fieldOfBusiness.append(row[2])
    global symbols
    symbols = ['']
    for i in range(0,len(symbolList)):
        symbols = [symbols[0]+symbolList[i]+',']
    print (timeTag)

def create_combined_file():
    os.chdir("stockdata")
    os.chdir(timeTag)
    j = 0
    while os.path.exists("%s_combined_data_try_%s.csv" %(timeTag ,j)):
        j += 1
    global combined_file_name
    global json_combined_file_name
    combined_file_name = '%s_combined_data_try_%s.csv' %(timeTag ,j)
    json_combined_file_name = '%s_combined_data_try_%s.json' %(timeTag ,j)
    with open(combined_file_name, 'wb') as f:
        reader = csv.reader(f)

def add_headers():
    headers = ['priceAvg']
    with open(combined_file_name, 'wb') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()

def get_priceChange(comparedPrice):
    priceChange = lastPrice[sampleCount-1]-comparedPrice
    if comparedPrice == 0:
        priceChangePrecentage = 0
    else:
        priceChangePrecentage = priceChange/comparedPrice
    return priceChange, priceChangePrecentage

def get_bidChange(comparedBid):
    bidChange = bid[sampleCount-1]-comparedBid
    if comparedBid == 0:
        bidChangePrecentage = 0
    else:
        bidChangePrecentage = bidChange/comparedBid
    return bidChange, bidChangePrecentage

def get_askChange(comparedAsk):
    askChange = ask[sampleCount-1]-comparedAsk
    if comparedAsk == 0:
        askChangePrecentage = 0
    else:
        askChangePrecentage = askChange/comparedAsk
    return askChange, askChangePrecentage

def add_info():
    fileName = 'A20170929-180854.csv'
    global headers
    headers = ['Symbol' , 'priceChange', 'priceChange%', 'priceAvg', 'variance', 'volatility','previousCloseChange', 'previousCloseChange%', 'openChange', 'openChange%', 'highChange', 'highChange%', 'lowChange', 'lowChange%', 'yearHighChange', 'yearHighChange%', 'yearLowChange', 'yearLowChange%', 'matchedYearHigh', 'matchedYearLow', 'bidAvg', 'bidVar', 'bidVolatility', 'bidChange', 'bidChange%', 'askAvg', 'askVar', 'askVolatility', 'askChange', 'askChange%', 'tradeSizeAvg', 'tradeSizeAvg$', 'bidSizeAvg', 'bidSizeAvg$', 'askSizeAvg', 'askSizeAvg$', 'maxTradeSize', 'maxAskSize', 'maxBidSize', 'maxTradeSize$', 'maxAskSize$', 'maxBidSize$', 'Consumer_Discretionary', 'Consumer_Staples', 'Energy', 'Financials', 'Health_Care', 'Industrials', 'Information Technology', 'Materials', 'Real_Estate', 'Telecommunications_Services', 'Utilities', 'matchedDayHigh', 'matchedDayLow', 'sampleTo20DaysVolume', 'sampleToYearVolume', 'sharesOutstanding', 'maxTradeSizeToSharesOutstanding', 'dividendYieldAnnual', 'dividendRateAnnual']
    newRows = []
    for i in range(0,len(symbolList)):
        with open(symbolList[i]+timeTag+'.csv', 'rb') as f:
            reader = csv.DictReader(f)
            priceSum = 0
            var = 0
            bidVar = 0
            askVar = 0
            volatility = 0
            bidVolatility = 0
            askVolatility = 0
            relativeRate = 1.06 #3month US Gov bonds rate
            global lastPrice 
            lastPrice = []
            global bid
            bid = []
            global ask
            ask = []
            tradeSize = []
            bidSize = []
            askSize = []
            volume = []
            for row in reader:
                if row['lastPrice'] is None or row['lastPrice'] == "":
                    lastPrice.append(0)
                else:
                    lastPrice.append(float(row['lastPrice']))
                if row['bid'] is None or row['bid'] == "":
                    bid.append(0)
                else:
                    bid.append(float(row['bid']))
                if row['ask'] is None or row['ask'] == "":
                    ask.append(0)
                else:
                    ask.append(float(row['ask']))
                if row['tradeSize'] is None or row['tradeSize'] == "":
                    tradeSize.append(0)
                else:
                    tradeSize.append(float(row['tradeSize']))
                if row['bidSize'] is None or row['bidSize'] == "":
                    bidSize.append(0)
                else:
                    bidSize.append(float(row['bidSize']))
                if row['askSize'] is None or row['askSize'] == "":
                    askSize.append(0)
                else:
                    askSize.append(float(row['askSize']))
                #volume
                if row['volume'] is None or row['volume'] == "":
                    volume.append(0)
                else:
                    volume.append(float(row['volume']))
                #closing price
                if row['previousClose'] is None or row['previousClose'] == "":
                    previousClose = 0
                else:
                    previousClose = float(row['previousClose'])
                #openning price
                if row['open'] is None or row['open'] == "":
                    openPrice = 0
                else:
                    openPrice = float(row['open'])
                #daily high
                if row['high'] is None or row['high'] == "":
                    high = 0
                else:
                    high = float(row['high'])
                #daily low
                if row['low'] is None or row['low'] == "":
                    low = 0
                else:
                    low = float(row['low'])
                #1 year high
                if row['fiftyTwoWkHigh'] is None or row['fiftyTwoWkHigh'] == "":
                    yearHigh = 0
                else:
                    yearHigh = float(row['fiftyTwoWkHigh']) 
                #1 year low
                if row['fiftyTwoWkLow'] is None or row['fiftyTwoWkLow'] == "":
                    yearLow = 0
                else:
                    yearLow = float(row['fiftyTwoWkLow'])
                #twenty Days Avarage Volume
                if row['twentyDayAvgVol'] is None or row['twentyDayAvgVol'] == "":
                    twentyDayAvgVol = 0
                else:
                    twentyDayAvgVol = float(row['twentyDayAvgVol'])
                #year Avarage Volume
                if row['avgVolume'] is None or row['avgVolume'] == "":
                    yearAvgVolume = 0
                else:
                    yearAvgVolume = float(row['avgVolume'])
                #sharesOutstanding
                if row['sharesOutstanding'] is None or row['sharesOutstanding'] == "":
                    sharesOutstanding = 0
                else:
                    sharesOutstanding = float(row['sharesOutstanding'])    
                #dividendYieldAnnual
                if row['dividendYieldAnnual'] is None or row['dividendYieldAnnual'] == "":
                    dividendYieldAnnual = 0
                else:
                    dividendYieldAnnual = float(row['dividendYieldAnnual'])
                #dividendRateAnnual
                if row['dividendRateAnnual'] is None or row['dividendRateAnnual'] == "":
                    dividendRateAnnual = 0
                else:
                    dividendRateAnnual = float(row['dividendRateAnnual'])
            sampleVolume = sum(tradeSize)
            sampleTo20DaysVolume = sampleVolume/twentyDayAvgVol
            sampleToYearVolume = sampleVolume/yearAvgVolume
            priceAvg = numpy.mean(lastPrice)
            bidAvg = numpy.mean(bid)
            askAvg = numpy.mean(ask)
            tradeSizeAvg = numpy.mean(tradeSize)  
            tradeSizeAvgDollars = tradeSizeAvg*priceAvg
            bidSizeAvg = numpy.mean(bidSize)
            bidSizeAvgDollars = bidSizeAvg*bidAvg
            askSizeAvg = numpy.mean(askSize)
            askSizeAvgDollars = askSizeAvg*askAvg
            maxTradeSize = max(tradeSize) 
            maxAskSize = max(askSize)
            maxBidSize = max(bidSize)
            maxTradeSizeDollars = maxTradeSize*priceAvg
            maxAskSizeDollars = maxAskSize*askAvg
            maxBidSizeDollars = maxBidSize*bidAvg
            var = numpy.var(lastPrice)
            bidVar = numpy.var(bid)
            askVar = numpy.var(ask)
            volatility = numpy.std(lastPrice)
            bidVolatility = numpy.std(bid)
            askVolatility = numpy.std(ask)
            priceChange, priceChangePrecentage = get_priceChange(lastPrice[0])
            bidChange, bidChangePrecentage = get_bidChange(bid[0])
            askChange, askChangePrecentage = get_askChange(ask[0])
            previousCloseChange, previousCloseChangePrecentage = get_priceChange(previousClose)
            openChange, openChangePrecentage = get_priceChange(openPrice)
            highChange, highChangePrecentage = get_priceChange(high)
            lowChange, lowChangePrecentage = get_priceChange(low)
            yearHighChange, yearHighChangePrecentage = get_priceChange(yearHigh)
            yearLowChange, yearLowChangePrecentage = get_priceChange(yearLow)
            matchedYearHigh = int(lastPrice.__contains__(yearHigh))
            matchedYearLow = int(lastPrice.__contains__(yearLow))
            matchedDayHigh = int(lastPrice.__contains__(high))
            matchedDayLow = int(lastPrice.__contains__(low))
            Consumer_Discretionary = int(fieldOfBusiness[i] == 'Consumer Discretionary')
            Consumer_Staples = int(fieldOfBusiness[i] == 'Consumer Staples')
            Energy = int(fieldOfBusiness[i] == 'Energy')
            Financials = int(fieldOfBusiness[i] == 'Financials')
            Health_Care = int(fieldOfBusiness[i] == 'Health Care')
            Industrials = int(fieldOfBusiness[i] == 'Industrials')
            Information_Technology = int(fieldOfBusiness[i] == 'Information Technology')
            Materials = int(fieldOfBusiness[i] == 'Materials')
            Real_Estate = int(fieldOfBusiness[i] == 'Real Estate')
            Telecommunications_Services = int(fieldOfBusiness[i] == 'Telecommunications Services')
            Utilities = int(fieldOfBusiness[i] == 'Utilities')
            maxTradeSizeToSharesOutstanding = maxTradeSize/sharesOutstanding
            newRows.append([symbolList[i], priceChange, priceChangePrecentage, priceAvg, var, volatility, previousCloseChange, previousCloseChangePrecentage, openChange, openChangePrecentage, highChange, highChangePrecentage, lowChange, lowChangePrecentage, yearHighChange, yearHighChangePrecentage, yearLowChange, yearLowChangePrecentage, matchedYearHigh, matchedYearLow, bidAvg, bidVar, bidVolatility, bidChange, bidChangePrecentage, askAvg, askVar, askVolatility, askChange, askChangePrecentage, tradeSizeAvg, tradeSizeAvgDollars, bidSizeAvg, bidSizeAvgDollars, askSizeAvg, askSizeAvgDollars,maxTradeSize, maxAskSize, maxBidSize, maxTradeSizeDollars, maxAskSizeDollars, maxBidSizeDollars, Consumer_Discretionary, Consumer_Staples, Energy, Financials, Health_Care, Industrials, Information_Technology, Materials, Real_Estate, Telecommunications_Services, Utilities, matchedDayHigh, matchedDayLow, sampleTo20DaysVolume, sampleToYearVolume, sharesOutstanding, maxTradeSizeToSharesOutstanding, dividendYieldAnnual, dividendRateAnnual])
    print (combined_file_name)
    with open(combined_file_name, 'wb') as f:
         writer = csv.writer(f)
         writer.writerow(headers)
         for i in range (0,len(symbolList)):
             writer.writerow(newRows[i])
    mydb = Database()
    csvfile = open(combined_file_name, 'r')
    jsonfile = open(json_combined_file_name, 'w')
    reader = csv.DictReader(csvfile, headers)
    jsonresult = json.dumps( [ row for row in reader ] )
    jsonfile.write(jsonresult)
    mydb.insert_results(jsonfile)
    print "Done"
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
    except getopth.GetoptError, err:
        print (str(err))
        sys.exit(2)
    get_info()
    create_combined_file()
    add_headers()
    add_info()
    #define_url()
    
if __name__ == "__main__":
    main()
    print ('done')

