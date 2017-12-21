#from marketHack import get_data
from marketHack import define_url
from marketHack import create_files
from joinedStockData import get_info
from joinedStockData import create_combined_file
#from joinedStockData import add_headers
from joinedStockData import add_info
import getopt
import sys


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
    except getopth.GetoptError, err:
        print (str(err))
        sys.exit(2)
    for i in range(0,3):
        urls, symbolList = define_url()
        time_stamp, run_time, stock_data_db = create_files(urls, symbolList)
        symbolList, fieldOfBusiness = get_info(run_time)
        #get_info(time_stamp, run_time)
        combined_file_name = create_combined_file(run_time)
        #create_combined_file()
        #add_headers()
        add_info(symbolList, fieldOfBusiness, combined_file_name, run_time, stock_data_db)
        #add_info()
        # define_url()


if __name__ == "__main__":
    main()
    print ('done')