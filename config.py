live_trade      = True      # False to see the output & verify your API key is working
clear_direction = True      # True to minimize lose, False to maximize profit

# Asset Configuration
coin            = "ETH"
quantity        = 0.01      # Minimum 0.001, if good trending it will raise up to 3x of this amount
leverage        = 40        # Maximum 125 // Recommended 30-40
round_decimal   = 2         # Some crypto pairs like chainlink read up to 3 decimal place of USDT

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Set Levarage     :   " + str(leverage))
print()
