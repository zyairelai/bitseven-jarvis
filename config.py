live_trade      = True
clear_direction = True      # True to minimize lose, False to maximize profit

# Asset Configuration
coin            = "ETH"
quantity        = 0.009     # Minimum 0.001
leverage        = 20
round_decimal   = 2

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()
