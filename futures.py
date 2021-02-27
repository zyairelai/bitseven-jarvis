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
            if config.live_trade: client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if direction == "GREEN" and volume_confirmation(previous_volume(), current_volume()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            if config.live_trade: client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    else:
        if direction == "GREEN" and volume_confirmation(previous_volume(), current_volume()):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if config.live_trade: client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.trade_amount, timestamp=get_timestamp())

        elif direction == "RED" and volume_confirmation(previous_volume(), current_volume()):
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
def first_run_volume()    : return float(KLINE_INTERVAL_12HOUR()[-3][5]) 
def previous_volume()     : return float(KLINE_INTERVAL_12HOUR()[-2][5]) 
def current_volume()      : return float(KLINE_INTERVAL_12HOUR()[-1][5]) 
def volume_confirmation(previous_volume, current_volume): return current_volume > (previous_volume / 5)

def get_timestamp()             : return int(time.time() * 1000)
def position_information()      : return client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())
def KLINE_INTERVAL_12HOUR()     : return client.get_klines(symbol=config.coin + "USDT", limit=4, interval=Client.KLINE_INTERVAL_12HOUR)
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