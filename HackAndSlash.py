from marketHack import define_url
from marketHack import create_files
from joinedStockData import get_info
from joinedStockData import add_info
import getopt
import sys


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
    except getopth.GetoptError, err:
        print (str(err))
        sys.exit(2)

    for i in range(0,5):
        urls, symbolList = define_url()
        time_stamp, run_time, stock_data_db = create_files(urls, symbolList)
        symbolList, fieldOfBusiness = get_info()
        add_info(symbolList, fieldOfBusiness, run_time, stock_data_db)


if __name__ == "__main__":
    main()
    print ('done')