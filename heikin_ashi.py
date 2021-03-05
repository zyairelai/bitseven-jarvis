import binance_api
from datetime import datetime
from termcolor import colored

def initial_Open(klines)  : return (float(klines[-4][1]) + float(klines[-4][4])) / 2
def initial_Close(klines) : return (float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4

def first_Open(klines)    : return (initial_Open(klines) + initial_Close(klines)) / 2
def first_Close(klines)   : return (float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4
def first_High(klines)    : return max(float(klines[-3][2]), first_Open(klines), first_Close(klines))
def first_Low(klines)     : return min(float(klines[-3][3]), first_Open(klines), first_Close(klines))

def previous_Open(klines) : return (first_Open(klines) + first_Close(klines)) / 2
def previous_Close(klines): return (float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4
def previous_High(klines) : return max(float(klines[-2][2]), previous_Open(klines), previous_Close(klines))
def previous_Low(klines)  : return min(float(klines[-2][3]), previous_Open(klines), previous_Close(klines))

def current_Open(klines)  : return (previous_Open(klines) + previous_Close(klines)) / 2
def current_Close(klines) : return (float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4
def current_High(klines)  : return max(float(klines[-1][2]), current_Open(klines), current_Close(klines))
def current_Low(klines)   : return min(float(klines[-1][3]), current_Open(klines), current_Close(klines))

def first_run_volume()    : return float(binance_api.KLINE_INTERVAL_1HOUR()[-3][5]) 
def previous_volume()     : return float(binance_api.KLINE_INTERVAL_1HOUR()[-2][5]) 
def current_volume()      : return float(binance_api.KLINE_INTERVAL_1HOUR()[-1][5]) 

def first_candle(klines):
    if   (first_Open(klines) == first_High(klines)): return "RED"
    elif (first_Open(klines) == first_Low(klines)) : return "GREEN"
    elif (first_Open(klines) > first_Close(klines)): return "RED_INDECISIVE"
    elif (first_Close(klines) > first_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def previous_candle(klines):
    if   (previous_Open(klines) == previous_High(klines)): return "RED"
    elif (previous_Open(klines) == previous_Low(klines)) : return "GREEN"
    elif (previous_Open(klines) > previous_Close(klines)): return "RED_INDECISIVE"
    elif (previous_Close(klines) > previous_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def current_candle(klines):
    if   (current_Open(klines) == current_High(klines)): return "RED"
    elif (current_Open(klines) == current_Low(klines)) : return "GREEN"
    elif (current_Open(klines) > current_Close(klines)): return "RED_INDECISIVE"
    elif (current_Close(klines) > current_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def volume_confirmation() : 
    confirmation = current_volume() > (previous_volume() / 5)
    if confirmation == True: print(colored("VOLUME ENTRY     :   YES", "green"))
    else: print(colored("VOLUME ENTRY     :   NO", "red"))
    return confirmation

def get_hour(hour): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    title = str(hour) + " HOUR DIRECTION :   "
    if   hour == 1: klines = binance_api.KLINE_INTERVAL_1HOUR()
    elif hour == 2: klines = binance_api.KLINE_INTERVAL_2HOUR()
    elif hour == 4: klines = binance_api.KLINE_INTERVAL_4HOUR()
    elif hour == 6: klines = binance_api.KLINE_INTERVAL_6HOUR()

    current = current_candle(klines)
    if   current == "GREEN"             : print(colored(title + current, "green"))
    elif current == "GREEN_INDECISIVE"  : print(colored(title + current, "green"))
    elif current == "RED"               : print(colored(title + current, "red"))
    elif current == "RED_INDECISIVE"    : print(colored(title + current, "red"))
    else                                : print(colored(title + current, "yellow"))
    return current

def get_current_minute(minute): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    title = "RECENT " + str(minute) + " MINUTE  :   "
    if   minute == 1: klines = binance_api.KLINE_INTERVAL_1MINUTE()
    elif minute == 3: klines  = binance_api.KLINE_INTERVAL_3MINUTE()
    elif minute == 5: klines  = binance_api.KLINE_INTERVAL_5MINUTE()
    elif minute == 15: klines = binance_api.KLINE_INTERVAL_15MINUTE()
    elif minute == 30: klines = binance_api.KLINE_INTERVAL_30MINUTE()

    minute_candle = current_candle(klines)
    if   minute_candle == "GREEN"            :   print(colored(title + minute_candle, "green"))
    elif minute_candle == "GREEN_INDECISIVE" :   print(colored(title + minute_candle, "green"))
    elif minute_candle == "RED"              :   print(colored(title + minute_candle, "red"))
    elif minute_candle == "RED_INDECISIVE"   :   print(colored(title + minute_candle, "red"))
    else                                     :   print(colored(title + minute_candle, "yellow"))
    return minute_candle

def pencil_wick_test(CANDLE, INTERVAL): # return "PASS" // "FAIL"
    if   INTERVAL == "1MINUTE" : klines = binance_api.KLINE_INTERVAL_1MINUTE()
    elif INTERVAL == "3MINUTE" : klines = binance_api.KLINE_INTERVAL_3MINUTE()
    elif INTERVAL == "5MINUTE" : klines = binance_api.KLINE_INTERVAL_5MINUTE()
    elif INTERVAL == "15MINUTE": klines = binance_api.KLINE_INTERVAL_15MINUTE()
    elif INTERVAL == "30MINUTE": klines = binance_api.KLINE_INTERVAL_30MINUTE()
    elif INTERVAL == "1HOUR"   : klines = binance_api.KLINE_INTERVAL_1HOUR()
    elif INTERVAL == "2HOUR"   : klines = binance_api.KLINE_INTERVAL_2HOUR()
    elif INTERVAL == "4HOUR"   : klines = binance_api.KLINE_INTERVAL_4HOUR()
    elif INTERVAL == "6HOUR"   : klines = binance_api.KLINE_INTERVAL_6HOUR()

    if CANDLE == "GREEN":
        # if (current_Close(klines) > previous_Close(klines)): return "PASS"
        if (current_Close(klines) > previous_High(klines)): return "PASS"
        else: return "FAIL"
    elif CANDLE == "RED":
        # if (current_Close(klines) < previous_Close(klines)): return "PASS"
        if (current_Low(klines) < previous_Low(klines)): return "PASS"
        else: return "FAIL"

def pattern_broken(INTERVAL): # return "BROKEN" // "NOT_BROKEN"
    if   INTERVAL == "1MINUTE" : klines = binance_api.KLINE_INTERVAL_1MINUTE()
    elif INTERVAL == "3MINUTE" : klines = binance_api.KLINE_INTERVAL_3MINUTE()
    elif INTERVAL == "5MINUTE" : klines = binance_api.KLINE_INTERVAL_5MINUTE()
    elif INTERVAL == "15MINUTE": klines = binance_api.KLINE_INTERVAL_15MINUTE()
    elif INTERVAL == "30MINUTE": klines = binance_api.KLINE_INTERVAL_30MINUTE()
    elif INTERVAL == "1HOUR"   : klines = binance_api.KLINE_INTERVAL_1HOUR()
    elif INTERVAL == "2HOUR"   : klines = binance_api.KLINE_INTERVAL_2HOUR()
    elif INTERVAL == "4HOUR"   : klines = binance_api.KLINE_INTERVAL_4HOUR()
    elif INTERVAL == "6HOUR"   : klines = binance_api.KLINE_INTERVAL_6HOUR()

    if   (first_Open(klines) == first_Low(klines)) : first = "GREEN"
    elif (first_Open(klines) == first_High(klines)): first = "RED"
    else: first = "INDECISIVE"

    if   (previous_Open(klines) == previous_Low(klines)) : previous = "GREEN"
    elif (previous_Open(klines) == previous_High(klines)): previous = "RED"
    else: previous = "INDECISIVE"

    if   (current_Open(klines) == current_Low(klines)) : current = "GREEN"
    elif (current_Open(klines) == current_High(klines)): current = "RED"
    else: current = "INDECISIVE"

    if ((first == "INDECISIVE") and (previous == "INDECISIVE") and (current == "INDECISIVE") and (current_Close(klines) >= previous_Low(klines))) or \
       ((first == "GREEN")      and (previous == "GREEN")      and (current == "INDECISIVE") and (current_Close(klines) <= previous_High(klines))) or \
       ((first == "RED")        and (previous == "RED")        and (current == "INDECISIVE")) or \
       ((current == "GREEN")    and (first_High(klines) > previous_High(klines)) and (previous_High(klines) < current_Close(klines))) or \
       ((current == "RED")      and (first_Low(klines) < previous_Low(klines))   and (previous_Low(klines) > current_Close(klines))) or \
       ((current == "GREEN")    and (current_Close(klines) < previous_Close(klines))) or \
       ((current == "RED")      and (current_Close(klines) > previous_Close(klines))): return "BROKEN"
    else: return "NOT_BROKEN"
