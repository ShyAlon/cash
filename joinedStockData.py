import getopt
import sys
import csv
import numpy
from db import Database

SAMPLE_COUNT = 98
FIELD_COUNT = 46
SYMBOL_COUNT = 500


def get_info():
    symbol_list = []
    field_of_business = []

    with open('resources/snp_constituents.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            symbol_list.append(row[0])
            field_of_business.append(row[2])

    symbols = ['']
    for i in range(0, len(symbol_list)):
        symbols = [symbols[0]+symbol_list[i]+',']

    return symbol_list, field_of_business


def get_price_change(compared_price, last_price):
    price_change = last_price[SAMPLE_COUNT-1]-compared_price
    if compared_price == 0:
        price_change_percentage = 0
    else:
        price_change_percentage = price_change/compared_price
    return price_change, price_change_percentage


def get_bidChange(comparedBid, bid):
    bidChange = bid[SAMPLE_COUNT-1]-comparedBid
    if comparedBid == 0:
        bidChangePrecentage = 0
    else:
        bidChangePrecentage = bidChange/comparedBid
    return bidChange, bidChangePrecentage


def get_askChange(comparedAsk, ask):
    askChange = ask[SAMPLE_COUNT-1]-comparedAsk
    if comparedAsk == 0:
        askChangePrecentage = 0
    else:
        askChangePrecentage = askChange/comparedAsk
    return askChange, askChangePrecentage


def find_key_index(key, stock_data):
    for i in range(0, FIELD_COUNT):
        if stock_data[0][i] == key:
            return i


def test_data_null(data):
    if data is None or data == "":
        return 0
    else:
        return data


def add_info(symbol_list, field_of_business, time_tag, stock_data_db):
    combined_stock_data = {}

    headers = ['Symbol', 'price_change', 'price_change%', 'priceAvg', 'variance', 'volatility', 'previousCloseChange',
               'previousCloseChange%', 'openChange', 'openChange%', 'highChange', 'highChange%', 'lowChange',
               'lowChange%', 'yearHighChange', 'yearHighChange%', 'yearLowChange', 'yearLowChange%', 'matchedYearHigh',
               'matchedYearLow', 'bidAvg', 'bidVar', 'bidVolatility', 'bidChange', 'bidChange%', 'askAvg', 'askVar',
               'askVolatility', 'askChange', 'askChange%', 'tradeSizeAvg', 'tradeSizeAvg$', 'bidSizeAvg', 'bidSizeAvg$',
               'askSizeAvg', 'askSizeAvg$', 'maxTradeSize', 'maxAskSize', 'maxBidSize', 'maxTradeSize$', 'maxAskSize$',
               'maxBidSize$', 'Consumer_Discretionary', 'Consumer_Staples', 'Energy', 'Financials', 'Health_Care',
               'Industrials', 'Information Technology', 'Materials', 'Real_Estate', 'Telecommunications_Services',
               'Utilities', 'matchedDayHigh', 'matchedDayLow', 'sampleTo20DaysVolume', 'sampleToYearVolume',
               'sharesOutstanding', 'maxTradeSizeToSharesOutstanding', 'dividendYieldAnnual', 'dividendRateAnnual']

    for key in stock_data_db["rows"].keys():
        last_price = []
        bid = []
        ask = []
        tradeSize = []
        bidSize = []
        askSize = []
        volume = []
        stock_data = numpy.array(stock_data_db["rows"][key])
        for i in range(1,SAMPLE_COUNT+1):
            last_price.append(test_data_null(stock_data[i][find_key_index('lastPrice',stock_data)]))
            bid.append(test_data_null(stock_data[i][find_key_index('bid',stock_data)]))
            ask.append(test_data_null(stock_data[i][find_key_index('ask',stock_data)]))
            tradeSize.append(test_data_null(stock_data[i][find_key_index('tradeSize',stock_data)]))
            bidSize.append(test_data_null(stock_data[i][find_key_index('bidSize',stock_data)]))
            askSize.append(test_data_null(stock_data[i][find_key_index('askSize',stock_data)]))
            volume.append(test_data_null(stock_data[i][find_key_index('volume',stock_data)]))
            previousClose = test_data_null(stock_data[i][find_key_index('previousClose',stock_data)])
            openPrice = test_data_null(stock_data[i][find_key_index('open',stock_data)])
            high = test_data_null(stock_data[i][find_key_index('high',stock_data)])
            low = test_data_null(stock_data[i][find_key_index('low',stock_data)])
            yearHigh = test_data_null(stock_data[i][find_key_index('fiftyTwoWkHigh',stock_data)])
            yearLow = test_data_null(stock_data[i][find_key_index('fiftyTwoWkLow',stock_data)])
            twentyDayAvgVol = test_data_null(stock_data[i][find_key_index('twentyDayAvgVol',stock_data)])
            yearAvgVolume = test_data_null(stock_data[i][find_key_index('avgVolume',stock_data)])
            sharesOutstanding = test_data_null(stock_data[i][find_key_index('sharesOutstanding',stock_data)])
            dividendYieldAnnual = test_data_null(stock_data[i][find_key_index('dividendYieldAnnual',stock_data)])
            dividendRateAnnual = test_data_null(stock_data[i][find_key_index('dividendRateAnnual',stock_data)])
        sampleVolume = sum(tradeSize)
        if (twentyDayAvgVol > 0):
            sampleTo20DaysVolume = sampleVolume / twentyDayAvgVol
        else:
            sampleTo20DaysVolume = 0
        if (yearAvgVolume > 0):
            sampleToYearVolume = sampleVolume / yearAvgVolume
        else:
            sampleToYearVolume = 0
        priceAvg = numpy.mean(last_price)
        bidAvg = numpy.mean(bid)
        askAvg = numpy.mean(ask)
        tradeSizeAvg = numpy.mean(tradeSize)
        tradeSizeAvgDollars = tradeSizeAvg * priceAvg
        bidSizeAvg = numpy.mean(bidSize)
        bidSizeAvgDollars = bidSizeAvg * bidAvg
        askSizeAvg = numpy.mean(askSize)
        askSizeAvgDollars = askSizeAvg * askAvg
        maxTradeSize = max(tradeSize)
        maxAskSize = max(askSize)
        maxBidSize = max(bidSize)
        maxTradeSizeDollars = maxTradeSize * priceAvg
        maxAskSizeDollars = maxAskSize * askAvg
        maxBidSizeDollars = maxBidSize * bidAvg
        var = numpy.var(last_price)
        bidVar = numpy.var(bid)
        askVar = numpy.var(ask)
        volatility = numpy.std(last_price)
        bidVolatility = numpy.std(bid)
        askVolatility = numpy.std(ask)
        price_change, price_change_percentage = get_price_change(last_price[0], last_price)
        bidChange, bidChangePrecentage = get_bidChange(bid[0], bid)
        askChange, askChangePrecentage = get_askChange(ask[0], ask)
        previousCloseChange, previousCloseChangePrecentage = get_price_change(previousClose, last_price)
        openChange, openChangePrecentage = get_price_change(openPrice, last_price)
        highChange, highChangePrecentage = get_price_change(high, last_price)
        lowChange, lowChangePrecentage = get_price_change(low, last_price)
        yearHighChange, yearHighChangePrecentage = get_price_change(yearHigh, last_price)
        yearLowChange, yearLowChangePrecentage = get_price_change(yearLow, last_price)
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
        maxTradeSizeToSharesOutstanding = maxTradeSize / sharesOutstanding
        combined_stock_data[key] = [key, price_change, price_change_percentage, priceAvg, var, volatility,
                                    previousCloseChange, previousCloseChangePrecentage, openChange, openChangePrecentage
                                    , highChange, highChangePrecentage, lowChange, lowChangePrecentage, yearHighChange,
                                    yearHighChangePrecentage, yearLowChange,yearLowChangePrecentage, matchedYearHigh,
                                    matchedYearLow, bidAvg, bidVar, bidVolatility, bidChange, bidChangePrecentage,
                                    askAvg, askVar, askVolatility, askChange, askChangePrecentage, tradeSizeAvg,
                                    tradeSizeAvgDollars, bidSizeAvg, bidSizeAvgDollars, askSizeAvg, askSizeAvgDollars,
                                    maxTradeSize, maxAskSize, maxBidSize, maxTradeSizeDollars, maxAskSizeDollars,
                                    maxBidSizeDollars, Consumer_Discretionary, Consumer_Staples, Energy, Financials,
                                    Health_Care, Industrials, Information_Technology, Materials, Real_Estate,
                                    Telecommunications_Services, Utilities, matchedDayHigh, matchedDayLow,
                                    sampleTo20DaysVolume, sampleToYearVolume, sharesOutstanding,
                                    maxTradeSizeToSharesOutstanding, dividendYieldAnnual, dividendRateAnnual]

    mydb = Database()
    data_type = "joined_stock_data"
    mydb.insert_result({"data_type": data_type, "date_and_time": time_tag, "rows": combined_stock_data,
                        "headers": headers, "samples": SAMPLE_COUNT})
    print "Done"


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
    except getopth.GetoptError, err:
        print (str(err))
        sys.exit(2)
    symbol_list, field_of_business = get_info()
    mydb = Database()
    stock_data_db = mydb.pull_last_result()
    add_info(symbol_list, field_of_business, time_tag="20171220-135509", stock_data_db=stock_data_db)


if __name__ == "__main__":
    main()
    print ('done')

