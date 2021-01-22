import config
import binance_futures
from termcolor import colored

def heikin_ashi(hour): # >>> "UP" // "DOWN" // "INDECISIVE"
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
    price_movement = (current_High - current_Low) / current_Open * 100
    threshold = config.threshold

    if (current_Open == current_Low):
        if (price_movement >= threshold):
            trend = "UP_TREND"
            print(colored(title + trend, "green"))
        else:
            trend = "NO_TRADE_ZONE" # "WEAK_RED"
            print(colored(title + trend, "green"))

    elif (current_Open == current_High):
        if (price_movement >= threshold):
            trend = "DOWN_TREND"
            print(colored(title + trend, "red"))
        else:
            trend = "NO_TRADE_ZONE" # "WEAK_GREEN"
            print(colored(title + trend, "red"))
            
    else:
        trend = "NO_TRADE_ZONE"
        print(colored(title + trend, "yellow"))

    return trend