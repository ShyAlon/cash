#import urllib2
#import time
import getopt
import sys
import csv
import os
#import math
import numpy
from db import Database
#import json
#import datetime

SAMPLE_COUNT = 2
FIELD_COUNT = 46
SYMBOL_COUNT = 500


def get_info(time_tag):
    #global time_tag
    #time_tag = "20171113-201721"
    #global sampleCount
    #sampleCount = 60
    #global fieldCount
    #fieldCount = 46
    #global symbolCount
    #symbolCount = 500
    #global symbol_list
    #global symbols
    symbol_list = []
    #global field_of_business
    field_of_business = []
    #os.chdir("..")
    #os.chdir("..")

    with open('resources/snp_constituents.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            symbol_list.append(row[0])
            field_of_business.append(row[2])

    symbols = ['']
    for i in range(0, len(symbol_list)):
        symbols = [symbols[0]+symbol_list[i]+',']

    #print (time_tag)

    return symbol_list, field_of_business


def create_combined_file(time_tag):
    #os.chdir("stockdata")
    #os.chdir(time_tag)
    j = 0
    while os.path.exists("stockdata/" + time_tag + "/%s_combined_data_try_%s.csv" % (time_tag, j)):
        j += 1
    #global combined_file_name
    #global json_combined_file_name
    combined_file_name = "stockdata/" + time_tag + '/%s_combined_data_try_%s.csv' % (time_tag, j)
    #json_combined_file_name = '%s_combined_data_try_%s.json' %(time_tag ,j)
    with open(combined_file_name, 'wb') as f:
        reader = csv.reader(f)

    return combined_file_name
    #return json_combined_file_name


# def add_headers():
#     headers = ['priceAvg']
#     with open(combined_file_name, 'wb') as f:
#         writer = csv.DictWriter(f, headers)
#         writer.writeheader()


def get_price_change(compared_price):
    price_change = last_price[SAMPLE_COUNT-1]-compared_price
    if compared_price == 0:
        price_change_percentage = 0
    else:
        price_change_percentage = price_change/compared_price
    return price_change, price_change_percentage


def get_bidChange(comparedBid):
    bidChange = bid[SAMPLE_COUNT-1]-comparedBid
    if comparedBid == 0:
        bidChangePrecentage = 0
    else:
        bidChangePrecentage = bidChange/comparedBid
    return bidChange, bidChangePrecentage


def get_askChange(comparedAsk):
    askChange = ask[SAMPLE_COUNT-1]-comparedAsk
    if comparedAsk == 0:
        askChangePrecentage = 0
    else:
        askChangePrecentage = askChange/comparedAsk
    return askChange, askChangePrecentage


def add_info(symbol_list, field_of_business, combined_file_name, time_tag, stock_data_db):
    #fileName = 'A20170929-180854.csv'
    #global headers
    combined_stock_data = []
    headers = ['Symbol', 'price_change', 'price_change%', 'priceAvg', 'variance', 'volatility','previousCloseChange', 'previousCloseChange%', 'openChange', 'openChange%', 'highChange', 'highChange%', 'lowChange', 'lowChange%', 'yearHighChange', 'yearHighChange%', 'yearLowChange', 'yearLowChange%', 'matchedYearHigh', 'matchedYearLow', 'bidAvg', 'bidVar', 'bidVolatility', 'bidChange', 'bidChange%', 'askAvg', 'askVar', 'askVolatility', 'askChange', 'askChange%', 'tradeSizeAvg', 'tradeSizeAvg$', 'bidSizeAvg', 'bidSizeAvg$', 'askSizeAvg', 'askSizeAvg$', 'maxTradeSize', 'maxAskSize', 'maxBidSize', 'maxTradeSize$', 'maxAskSize$', 'maxBidSize$', 'Consumer_Discretionary', 'Consumer_Staples', 'Energy', 'Financials', 'Health_Care', 'Industrials', 'Information Technology', 'Materials', 'Real_Estate', 'Telecommunications_Services', 'Utilities', 'matchedDayHigh', 'matchedDayLow', 'sampleTo20DaysVolume', 'sampleToYearVolume', 'sharesOutstanding', 'maxTradeSizeToSharesOutstanding', 'dividendYieldAnnual', 'dividendRateAnnual']
    combined_stock_data["headers"] = headers
    newRows = []
    for i in range(0,len(symbol_list)):
        with open("stockdata/" + time_tag + "/" + symbol_list[i]+time_tag+'.csv', 'rb') as f:
            reader = csv.DictReader(f)
            #priceSum = 0
            #var = 0
            #bidVar = 0
            #askVar = 0
            #volatility = 0
            #bidVolatility = 0
            #askVolatility = 0
            #relativeRate = 1.06 #3month US Gov bonds rate
            global last_price
            last_price = []
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
                    last_price.append(0)
                else:
                    last_price.append(float(row['lastPrice']))
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
            if (twentyDayAvgVol>0):
                sampleTo20DaysVolume = sampleVolume/twentyDayAvgVol
            else:
                sampleTo20DaysVolume = 0
            if (yearAvgVolume>0):
                sampleToYearVolume = sampleVolume/yearAvgVolume
            else:
                sampleToYearVolume = 0
            priceAvg = numpy.mean(last_price)
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
            var = numpy.var(last_price)
            bidVar = numpy.var(bid)
            askVar = numpy.var(ask)
            volatility = numpy.std(last_price)
            bidVolatility = numpy.std(bid)
            askVolatility = numpy.std(ask)
            price_change, price_change_percentage = get_price_change(last_price[0])
            bidChange, bidChangePrecentage = get_bidChange(bid[0])
            askChange, askChangePrecentage = get_askChange(ask[0])
            previousCloseChange, previousCloseChangePrecentage = get_price_change(previousClose)
            openChange, openChangePrecentage = get_price_change(openPrice)
            highChange, highChangePrecentage = get_price_change(high)
            lowChange, lowChangePrecentage = get_price_change(low)
            yearHighChange, yearHighChangePrecentage = get_price_change(yearHigh)
            yearLowChange, yearLowChangePrecentage = get_price_change(yearLow)
            matchedYearHigh = int(last_price.__contains__(yearHigh))
            matchedYearLow = int(last_price.__contains__(yearLow))
            matchedDayHigh = int(last_price.__contains__(high))
            matchedDayLow = int(last_price.__contains__(low))
            Consumer_Discretionary = int(field_of_business[i] == 'Consumer Discretionary')
            Consumer_Staples = int(field_of_business[i] == 'Consumer Staples')
            Energy = int(field_of_business[i] == 'Energy')
            Financials = int(field_of_business[i] == 'Financials')
            Health_Care = int(field_of_business[i] == 'Health Care')
            Industrials = int(field_of_business[i] == 'Industrials')
            Information_Technology = int(field_of_business[i] == 'Information Technology')
            Materials = int(field_of_business[i] == 'Materials')
            Real_Estate = int(field_of_business[i] == 'Real Estate')
            Telecommunications_Services = int(field_of_business[i] == 'Telecommunications Services')
            Utilities = int(field_of_business[i] == 'Utilities')
            maxTradeSizeToSharesOutstanding = maxTradeSize/sharesOutstanding
            newRows.append([symbol_list[i], price_change, price_change_percentage, priceAvg, var, volatility, previousCloseChange, previousCloseChangePrecentage, openChange, openChangePrecentage, highChange, highChangePrecentage, lowChange, lowChangePrecentage, yearHighChange, yearHighChangePrecentage, yearLowChange, yearLowChangePrecentage, matchedYearHigh, matchedYearLow, bidAvg, bidVar, bidVolatility, bidChange, bidChangePrecentage, askAvg, askVar, askVolatility, askChange, askChangePrecentage, tradeSizeAvg, tradeSizeAvgDollars, bidSizeAvg, bidSizeAvgDollars, askSizeAvg, askSizeAvgDollars,maxTradeSize, maxAskSize, maxBidSize, maxTradeSizeDollars, maxAskSizeDollars, maxBidSizeDollars, Consumer_Discretionary, Consumer_Staples, Energy, Financials, Health_Care, Industrials, Information_Technology, Materials, Real_Estate, Telecommunications_Services, Utilities, matchedDayHigh, matchedDayLow, sampleTo20DaysVolume, sampleToYearVolume, sharesOutstanding, maxTradeSizeToSharesOutstanding, dividendYieldAnnual, dividendRateAnnual])
    print (combined_file_name)
    with open(combined_file_name, 'wb') as f:
         writer = csv.writer(f)
         writer.writerow(headers)
         for i in range (0,len(symbol_list)):
             writer.writerow(newRows[i])
    mydb = Database()
    data_type = "Joined Stock Data"
    #time_stamp = time.mktime(int(time_tag).timetuple())
    mydb.insert_result({"Data Type":data_type, "Date and Time":time_tag, "Headers":headers, "rows":newRows})
    print "Done"
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
    except getopth.GetoptError, err:
        print (str(err))
        sys.exit(2)
    symbol_list, field_of_business = get_info(time_tag="20171218-140923")
    combined_file_name = create_combined_file(time_tag="20171218-140923")
    #add_headers()
    mydb = Database()
    stock_data_db = mydb.pull_last_result()
    add_info(symbol_list, field_of_business, combined_file_name, time_tag="20171218-140923", stock_data_db = stock_data_db)
    #define_url()
    
if __name__ == "__main__":
    main()
    print ('done')

