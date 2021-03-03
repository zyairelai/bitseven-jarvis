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
    direction = current_candle(KLINE_INTERVAL_6HOUR())
    if direction == "GREEN": print(colored("CURRENT 6 HOUR   :   " + direction, "green"))
    elif direction == "RED": print(colored("CURRENT 6 HOUR   :   " + direction, "red"))
    else: print(colored("CURRENT 6 HOUR   :   " + direction, "yellow"))

    one_hour  = current_candle(KLINE_INTERVAL_1HOUR())
    if one_hour == "GREEN": print(colored("CURRENT 1 HOUR   :   " + one_hour, "green"))
    elif one_hour == "RED": print(colored("CURRENT 1 HOUR   :   " + one_hour, "red"))
    else: print(colored("CURRENT 1 HOUR   :   " + one_hour, "yellow"))

    if position_info == "LONGING":
        if (one_hour == "RED" or one_hour == "RED_INDECISIVE") and volume_confirmation():
            print("ACTION           :   💰 CLOSE_LONG 💰")
            if config.live_trade: client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if (one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE") and volume_confirmation():
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            if config.live_trade: client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    else:
        if direction == "GREEN" and one_hour == "GREEN" and volume_confirmation():
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if config.live_trade: client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())

        elif direction == "RED" and one_hour == "RED" and volume_confirmation():
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if config.live_trade: client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

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
def first_run_volume()    : return float(KLINE_INTERVAL_1HOUR()[-3][5]) 
def previous_volume()     : return float(KLINE_INTERVAL_1HOUR()[-2][5]) 
def current_volume()      : return float(KLINE_INTERVAL_1HOUR()[-1][5]) 

def volume_confirmation() : 
    confirmation = current_volume() > (previous_volume() / 5)
    if confirmation == True: print(colored("VOLUME ENTRY     :   YES", "green"))
    else: print(colored("VOLUME ENTRY     :   NO", "red"))
    return confirmation

def get_timestamp()             : return int(time.time() * 1000)
def position_information()      : return client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())
def KLINE_INTERVAL_1HOUR()      : return client.get_klines(symbol=config.coin + "USDT", limit=4, interval=Client.KLINE_INTERVAL_1HOUR)
def KLINE_INTERVAL_6HOUR()      : return client.get_klines(symbol=config.coin + "USDT", limit=4, interval=Client.KLINE_INTERVAL_6HOUR)
def change_leverage(leverage)   : return client.futures_change_leverage(symbol=config.pair, leverage=leverage, timestamp=get_timestamp())
def change_margin_to_ISOLATED() : return client.futures_change_margin_type(symbol=config.pair, marginType="ISOLATED", timestamp=get_timestamp())

def current_candle(klines):
    if   (current_Open(klines) == current_High(klines)): return "RED"
    elif (current_Open(klines) == current_Low(klines)) : return "GREEN"
    elif (current_Open(klines) > current_Close(klines)): return "RED_INDECISIVE"
    elif (current_Close(klines) > current_Open(klines)): return "GREEN_INDECISIVE"

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