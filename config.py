live_trade = False

coin = "BNB"
quantity = 0.001

if   coin == "BTC": leverage = 125
elif coin == "ETH": leverage = 100
else: leverage = 75

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Set Levarage     :   " + str(leverage))
print()
