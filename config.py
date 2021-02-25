live_trade      = False     # False to see the output & verify your API key is working

# print("Which coin do you want to trade?")
# print("1. BTC")
# print("2. ETH")
# user_input = input("\nEnter a number   :   ") or '1'

# Asset Configuration
user_input = 1
if user_input == '2': coin = "ETH"
else: coin = "BTC"

qty_in_USDT = 200

print("Coin Name        :   " + str(coin))
print("Trade Quantity   :   " + str(qty_in_USDT) + " " + " USDT")
print()
