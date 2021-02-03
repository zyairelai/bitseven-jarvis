output = True
callbackRate = 3
check_how_many_trades = 5

while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    print("3. BNB-USDT")
    print("4. BCH-USDT")
    print("5. LTC-USDT")
    print("6. LINK-USDT")
    print("7. SUSHI-USDT")
    print("8. TRX-USDT")
    print("9. XRP-USDT")


    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001 # 1.04 USDT @ 30XXX
        leverage        = 20
        round_decimal   = 2
        callbackRate    = 3
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.01  # 0.65 USDT @ 12XX
        leverage        = 15
        round_decimal   = 2
        break

    elif (input_pair == '3') or (input_pair == 'BNB'):
        coin            = "BNB"
        quantity        = 0.5   # 1.38 USDT @ 41.XX
        leverage        = 10
        round_decimal   = 3
        break

    elif (input_pair == '4') or (input_pair == 'BCH'):
        coin            = "BCH"
        quantity        = 0.05  # 1.44 USDT @ 430
        leverage        = 10
        round_decimal   = 2
        break

    elif (input_pair == '5') or (input_pair == 'LTC'):
        coin            = "LTC"
        quantity        = 0.15  # 1.40 USDT @ 140      
        leverage        = 10
        round_decimal   = 2
        break

    elif (input_pair == '6') or (input_pair == 'LINK'):
        coin            = "LINK"
        quantity        = 1     # 1.62 USDT @ 24.XX
        leverage        = 10
        round_decimal   = 3
        break

    elif (input_pair == '7') or (input_pair == 'SUSHI'):
        coin            = "SUSHI"
        quantity        = 2     # 1.42 USDT @ 7.XX
        leverage        = 5
        round_decimal   = 4
        callbackRate    = 5
        break

    elif (input_pair == '8') or (input_pair == 'TRX'):
        coin            = "TRX"
        quantity        = 500   # 0.96 USDT @ 0.028XX
        leverage        = 10
        round_decimal   = 5
        break

    elif (input_pair == '9') or (input_pair == 'XRP'):
        coin            = "XRP"
        quantity        = 50     # 0.9 USDT @ 0.26XX
        leverage        = 10
        round_decimal   = 4
        break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Leverage         :   " + str(leverage) + "x")
