import config
import os, time
from datetime import datetime
from termcolor import colored
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def lets_make_some_money():
    position_info = get_position_info()
    direction = current_candle(KLINE_INTERVAL_12HOUR())
    if direction == "GREEN": print(colored("CURRENT 12 HOUR  :   " + direction, "green"))
    elif direction == "RED": print(colored("CURRENT 12 HOUR  :   " + direction, "red"))
    else: print(colored("CURRENT 12 HOUR  :   " + direction, "yellow"))

    if position_info == "LONGING":
        if direction == "RED" and volume_confirmation(previous_volume(), current_volume()):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            if config.live_trade: close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if direction == "GREEN" and volume_confirmation(previous_volume(), current_volume()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            if config.live_trade: close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    else:
        if direction == "GREEN" and volume_confirmation(previous_volume(), current_volume()):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if config.live_trade: open_position("LONG")

        elif direction == "RED" and volume_confirmation(previous_volume(), current_volume()):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if config.live_trade: open_position("SHORT")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def get_timestamp()             : return int(time.time() * 1000)
def position_information()      : return client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())
def KLINE_INTERVAL_12HOUR()     : return client.get_klines(symbol=config.coin + "USDT", limit=4, interval=Client.KLINE_INTERVAL_12HOUR)
def change_leverage(leverage)   : return client.futures_change_leverage(symbol=config.pair, leverage=leverage, timestamp=get_timestamp())
def change_margin_to_ISOLATED() : return client.futures_change_margin_type(symbol=config.pair, marginType="ISOLATED", timestamp=get_timestamp())

def get_position_info(): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = "CURRENT POSITION :   "
    response = position_information()[0]
    positionAmt = float(response.get('positionAmt'))
    unRealizedProfit = round(float(response.get('unRealizedProfit')), 2)
    if (positionAmt > 0):
        position = "LONGING"
        print(colored(title + position, "green"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))
    elif (positionAmt < 0):
        position = "SHORTING"
        print(colored(title + position, "red"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))
    else:
        position = "NO_POSITION"
        print(title + position)
    return position

def open_position(position):
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())
    if position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())

def close_position(position):
    positionAmt = float(position_information()[0].get('positionAmt'))
    if position == "LONG":
        client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())
    if position == "SHORT":
        client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())

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
def first_run_volume()    : return float(KLINE_INTERVAL_12HOUR()[-3][5]) 
def previous_volume()     : return float(KLINE_INTERVAL_12HOUR()[-2][5]) 
def current_volume()      : return float(KLINE_INTERVAL_12HOUR()[-1][5]) 
def volume_confirmation(previous_volume, current_volume): return current_volume > (previous_volume / 5)

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

def pattern_broken(): # return "BROKEN" // "NOT_BROKEN"
    klines = KLINE_INTERVAL_12HOUR()

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
       ((current == "RED")      and (first_Low(klines) < previous_Low(klines))   and (previous_Low(klines) > current_Close(klines))) or \
       ((current == "GREEN")    and (current_Close(klines) < previous_Close(klines))) or \
       ((current == "RED")      and (current_Close(klines) > previous_Close(klines))): return "BROKEN"
    else: return "NOT_BROKEN"
