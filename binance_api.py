import os
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

pair = "BTCUSDT"

def KLINE_INTERVAL_1MINUTE()    : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_1MINUTE)
def KLINE_INTERVAL_3MINUTE()    : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_3MINUTE)
def KLINE_INTERVAL_5MINUTE()    : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_5MINUTE)
def KLINE_INTERVAL_15MINUTE()   : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_15MINUTE)
def KLINE_INTERVAL_30MINUTE()   : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_30MINUTE)
def KLINE_INTERVAL_1HOUR()      : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_1HOUR)
def KLINE_INTERVAL_2HOUR()      : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_2HOUR)
def KLINE_INTERVAL_4HOUR()      : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_4HOUR)
def KLINE_INTERVAL_6HOUR()      : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_6HOUR)
def KLINE_INTERVAL_12HOUR()     : return client.get_klines(symbol=pair, limit=4, interval=Client.KLINE_INTERVAL_12HOUR)

def get_volume(TIME_TRAVEL, INTERVAL):
    if   TIME_TRAVEL == "FIRSTRUN" : which = -3
    elif TIME_TRAVEL == "PREVIOUS" : which = -2
    elif TIME_TRAVEL == "CURRENT"  : which = -1
    if   INTERVAL == "1MINUTE"  : volume = KLINE_INTERVAL_1MINUTE()[which][5]
    elif INTERVAL == "3MINUTE"  : volume = KLINE_INTERVAL_3MINUTE()[which][5]
    elif INTERVAL == "5MINUTE"  : volume = KLINE_INTERVAL_5MINUTE()[which][5]
    elif INTERVAL == "15MINUTE" : volume = KLINE_INTERVAL_15MINUTE()[which][5]
    elif INTERVAL == "30MINUTE" : volume = KLINE_INTERVAL_30MINUTE()[which][5]
    elif INTERVAL == "1HOUR"    : volume = KLINE_INTERVAL_1HOUR()[which][5]
    elif INTERVAL == "2HOUR"    : volume = KLINE_INTERVAL_2HOUR()[which][5]
    elif INTERVAL == "4HOUR"    : volume = KLINE_INTERVAL_4HOUR()[which][5]
    elif INTERVAL == "6HOUR"    : volume = KLINE_INTERVAL_6HOUR()[which][5]
    return float(volume)

