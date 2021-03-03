import os
import config
from datetime import datetime
from termcolor import colored
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def lets_make_some_money():
    direction = current_candle(KLINE_INTERVAL_6HOUR())
    if direction == "GREEN": print(colored("CURRENT 6 HOUR   :   " + direction, "green"))
    elif direction == "RED": print(colored("CURRENT 6 HOUR   :   " + direction, "red"))
    else: print(colored("CURRENT 6 HOUR   :   " + direction, "yellow"))

    one_hour  = current_candle(KLINE_INTERVAL_1HOUR())
    if one_hour == "GREEN": print(colored("CURRENT 1 HOUR   :   " + one_hour, "green"))
    elif one_hour == "RED": print(colored("CURRENT 1 HOUR   :   " + one_hour, "red"))
    else: print(colored("CURRENT 1 HOUR   :   " + one_hour, "yellow"))

    if direction == "GREEN" and one_hour == "GREEN" and volume_confirmation():
        if quote_asset_balance("UP") < config.qty_in_USDT:
            trade_amount = config.qty_in_USDT - quote_asset_balance("UP")
            if trade_amount >= 10:
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: open_position("UP", trade_amount)

    elif direction == "RED" and one_hour == "RED" and volume_confirmation():
        if quote_asset_balance("DOWN") < config.qty_in_USDT:
            trade_amount = config.qty_in_USDT - quote_asset_balance("DOWN")
            if trade_amount >= 10:
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: open_position("DOWN", trade_amount)

    elif (direction == "GREEN" or direction == "GREEN_INDECISIVE"):
        if quote_asset_balance("DOWN") > config.qty_in_USDT:
            if config.live_trade: close_position("UP")

    elif (direction == "RED" or direction == "RED_INDECISIVE"):
        if quote_asset_balance("DOWN") > config.qty_in_USDT:
            if config.live_trade: close_position("DOWN")
                
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def asset_info(SIDE):
    return client.get_symbol_ticker(symbol=config.coin + SIDE + "USDT")

def asset_balance(SIDE):
    return float(client.get_asset_balance(asset=config.coin + SIDE).get("free"))

def quote_asset_balance(SIDE):
    return round(float(client.get_symbol_ticker(symbol=config.coin + SIDE + "USDT").get("price")) * float(client.get_asset_balance(asset=config.coin).get("free")), 2)

def open_position(SIDE, trade_amount):
    client.order_market_buy(symbol=config.coin + SIDE + "USDT", quoteOrderQty=trade_amount)

def close_position(SIDE):
    asset_balance = float(client.get_asset_balance(asset=config.coin + SIDE).get("free"))
    client.order_market_sell(symbol=config.coin + SIDE + "USDT", quantity=asset_balance)

def volume_confirmation() : 
    confirmation = current_volume() > (previous_volume() / 5)
    if confirmation == True: print(colored("VOLUME ENTRY     :   YES", "green"))
    else: print(colored("VOLUME ENTRY     :   NO", "red"))
    return confirmation

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
def first_run_volume(): return float(KLINE_INTERVAL_1HOUR()[-3][5]) 
def previous_volume(): return float(KLINE_INTERVAL_1HOUR()[-2][5]) 
def current_volume(): return float(KLINE_INTERVAL_1HOUR()[-1][5]) 

def KLINE_INTERVAL_1HOUR(): return client.get_klines(symbol=config.coin + "USDT", limit=4, interval=Client.KLINE_INTERVAL_1HOUR)
def KLINE_INTERVAL_6HOUR(): return client.get_klines(symbol=config.coin + "USDT", limit=4, interval=Client.KLINE_INTERVAL_6HOUR)

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
