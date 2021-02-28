live_trade  = True
leverage    = 5
qty_in_USDT = 200

print("Which coin do you want to trade?")
print("1. BNB")
print("2. TRX")
user_input = input("Enter a number   :   ") or '1'
print()

# Asset Configuration
if user_input == '2':
    coin = "TRX"
    trade_amount = 200
else:
    coin = "BNB"
    trade_amount = 0.05

print("Which mode do you want to enable?")
print("1. Futures")
print("2. Binance Leverage Token")
user_input = input("Enter a number   :   ") or '1'
print()

if user_input == '2': mode = "BLVT"
else: mode = "FUTURES"

pair = coin + "USDT"
print("Coin Name        :   " + str(coin))
if mode == "BLVT": print("Trade Quantity   :   " + str(qty_in_USDT) + " USDT")
if mode == "FUTURES": print("Trade Quantity   :   " + str(trade_amount) + " " + coin)
print("Trading Mode     :   " + mode)
print()
