from datetime import datetime
from termcolor import colored

round_decimal = 6
def initial_Open(klines)  : return round(((float(klines[-4][1]) + float(klines[-4][4])) / 2), round_decimal)
def initial_Close(klines) : return round(((float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4), round_decimal)

def first_Open(klines)    : return round(((initial_Open(klines) + initial_Close(klines)) / 2), round_decimal)
def first_Close(klines)   : return round(((float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4), round_decimal)
def first_High(klines)    : return max(float(klines[-3][2]), first_Open(klines), first_Close(klines))
def first_Low(klines)     : return min(float(klines[-3][3]), first_Open(klines), first_Close(klines))

def previous_Open(klines) : return round(((first_Open(klines) + first_Close(klines)) / 2), round_decimal)
def previous_Close(klines): return round(((float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4), round_decimal)
def previous_High(klines) : return max(float(klines[-2][2]), previous_Open(klines), previous_Close(klines))
def previous_Low(klines)  : return min(float(klines[-2][3]), previous_Open(klines), previous_Close(klines))

def current_Open(klines)  : return round(((previous_Open(klines) + previous_Close(klines)) / 2), round_decimal)
def current_Close(klines) : return round(((float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4), round_decimal)
def current_High(klines)  : return max(float(klines[-1][2]), current_Open(klines), current_Close(klines))
def current_Low(klines)   : return min(float(klines[-1][3]), current_Open(klines), current_Close(klines))

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

def current_direction(): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    title = "CURRENT 12 HOUR  :   "
    klines = binance_spot.KLINE_INTERVAL_12HOUR()

    current = current_candle(klines)
    if   current == "GREEN"             : print(colored(title + current, "green"))
    elif current == "GREEN_INDECISIVE"  : print(colored(title + current, "green"))
    elif current == "RED"               : print(colored(title + current, "red"))
    elif current == "RED_INDECISIVE"    : print(colored(title + current, "red"))
    else                                : print(colored(title + current, "yellow"))
    return current

def pencil_wick_test(CANDLE, INTERVAL): # return "PASS" // "FAIL"
    klines = binance_spot.KLINE_INTERVAL_12HOUR()

    if CANDLE == "GREEN":
        if (current_High(klines) > previous_High(klines)): return "PASS"
        else: return "FAIL"
    elif CANDLE == "RED":
        if (current_Low(klines) < previous_Low(klines)): return "PASS"
        else: return "FAIL"

def one_minute_exit_test(CANDLE): # return "PASS" // "FAIL"
    klines = binance_spot.KLINE_INTERVAL_1MINUTE()
    threshold = abs((previous_Open(klines) - previous_Close(klines)) / 4)

    if CANDLE == "GREEN":
        if (previous_High(klines) > current_High(klines)) and (current_Low(klines) < (previous_Low(klines) + threshold)): return True
    elif CANDLE == "RED":
        if (current_Low(klines) > previous_Low(klines)) and (current_High(klines) > (previous_High(klines) - threshold)): return True

def pattern_broken(): # return "BROKEN" // "NOT_BROKEN"
    klines = binance_spot.KLINE_INTERVAL_12HOUR()

    if   (first_Open(klines) == first_Low(klines)) : first = "GREEN"
    elif (first_Open(klines) == first_High(klines)): first = "RED"
    else: first = "INDECISIVE"

    if   (previous_Open(klines) == previous_Low(klines)) : previous = "GREEN"
    elif (previous_Open(klines) == previous_High(klines)): previous = "RED"
    else: previous = "INDECISIVE"

    if   (current_Open(klines) == current_Low(klines)) : current = "GREEN"
    elif (current_Open(klines) == current_High(klines)): current = "RED"
    else: current = "INDECISIVE"

    if ((first == "INDECISIVE") and (previous == "INDECISIVE") and (current == "INDECISIVE")) or \
       ((first == "GREEN")      and (previous == "GREEN")      and (current == "INDECISIVE")) or \
       ((first == "RED")        and (previous == "RED")        and (current == "INDECISIVE")) or \
       ((current == "GREEN")    and (first_High(klines) > previous_High(klines)) and (previous_High(klines) < current_Close(klines))) or \
       ((current == "RED")      and (first_Low(klines) < previous_Low(klines))   and (previous_Low(klines) > current_Close(klines))): return "BROKEN"
    else: return "NOT_BROKEN"
