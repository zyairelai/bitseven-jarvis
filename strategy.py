import os
import config
import entry_exit
import heikin_ashi
from datetime import datetime
from termcolor import colored
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def KLINE_INTERVAL_12HOUR(): return client.get_klines(symbol=config.coin + "USDT", limit=4, interval=Client.KLINE_INTERVAL_12HOUR)
def first_run_volume(): return float(KLINE_INTERVAL_12HOUR()[-3][5]) 
def previous_volume(): return float(KLINE_INTERVAL_12HOUR()[-2][5]) 
def current_volume(): return float(KLINE_INTERVAL_12HOUR()[-1][5]) 


def lets_make_some_money():
    direction = KLINE_INTERVAL_12HOUR()

    if direction == "GREEN" and ((previous_volume() / 5) < current_volume()):
        if quote_asset_balance("UP") < config.qty_in_USDT:
            trade_amount = config.qty_in_USDT - quote_asset_balance("UP")
            if trade_amount >= 10:
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: open_position("UP", trade_amount)

    elif direction == "RED" and ((previous_volume() / 5) < current_volume()):
        if quote_asset_balance("DOWN") < config.qty_in_USDT:
            trade_amount = config.qty_in_USDT - quote_asset_balance("DOWN")
            if trade_amount >= 10:
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: open_position("DOWN", trade_amount)

    elif direction == "GREEN_INDECISIVE":
        if quote_asset_balance("DOWN") > config.qty_in_USDT * 1.05:
            if config.live_trade: close_position("UP")

    elif direction == "RED_INDECISIVE":
        if quote_asset_balance("DOWN") > config.qty_in_USDT * 1.05:
            if config.live_trade: close_position("DOWN")

    else: print("ACTION           :   🐺 WAIT 🐺")


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
