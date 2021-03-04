live_trade = False

coin = "BTC"
quantity = 0.001

if   coin == "BTC": leverage = 50
elif coin == "ETH": leverage = 40
else: leverage = 30

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Set Levarage     :   " + str(leverage))
print()
