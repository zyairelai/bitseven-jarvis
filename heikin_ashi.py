output = False

import config
import binance_futures
from termcolor import colored

def heikin_ashi(hour, EXIT):
    if hour == 1: klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif hour == 6: klines = binance_futures.KLINE_INTERVAL_6HOUR()
    else: 
        hour = 6
        klines = binance_futures.KLINE_INTERVAL_6HOUR()
    title = str(hour) + " HOUR DIRECTION :   "

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    title = str(hour) + " HOUR DIRECTION :   "
    if EXIT == "EXIT": threshold = 0
    else: threshold = config.threshold
    price_movement = abs((current_Open - current_Close) / current_Open * 100)

    if output:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))
        print("The price_movement is:   " + str(price_movement))

    if (current_Open == current_Low):
        if (price_movement >= threshold):
            trend = "GREEN"
            print(colored(title + trend, "green"))
        else:
            trend = "WEAK_GREEN" # "WEAK_RED"
            print(colored(title + trend, "green"))

    elif (current_Open == current_High):
        if (price_movement >= threshold):
            trend = "RED"
            print(colored(title + trend, "red"))
        else:
            trend = "WEAK_RED" # "WEAK_GREEN"
            print(colored(title + trend, "red"))
            
    else:
        trend = "INDECISIVE"
        print(colored(title + trend, "yellow"))

    return trend