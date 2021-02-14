live_trade      = True      # False to see the output & verify your API key is working
clear_direction = True      # True to minimize lose, False to maximize profit

# Asset Configuration
coin            = "ETH"
quantity        = 0.01
leverage        = 40
round_decimal   = 2

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Set Levarage     :   " + str(leverage))
print()
