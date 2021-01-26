output = False
check_how_many_trades = 100
main_hour   = 6
support_dir = 1
callbackRate = 1.5

while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    print("3. LTC-USDT")
    print("4. BCH-USDT")
    print("5. LINK-USDT")
    print("6. SUSHI-USDT")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001 # 1.29 USDT @ 32000
        leverage        = 25
        round_decimal   = 2
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.02  # 1.24 USDT @ 12XX
        leverage        = 20
        round_decimal   = 2
        break

    elif (input_pair == '3') or (input_pair == 'LTC'):
        coin            = "LTC"
        quantity        = 0.15  # 1.40 USDT @ 140      
        leverage        = 15
        round_decimal   = 2
        break

    elif (input_pair == '4') or (input_pair == 'BCH'):
        coin            = "BCH"
        quantity        = 0.05  # 1.44 USDT @ 430
        leverage        = 15
        round_decimal   = 2
        break

    elif (input_pair == '5') or (input_pair == 'LINK'):
        coin            = "LINK"
        quantity        = 1     # 1.62 USDT @ 24.XX
        leverage        = 15
        round_decimal   = 3
        break

    elif (input_pair == '6') or (input_pair == 'SUSHI'):
        coin            = "SUSHI"
        quantity        = 2     # 1.42 USDT @ 7.XX
        leverage        = 10
        round_decimal   = 4
        break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Leverage         :   " + str(leverage) + "x")
