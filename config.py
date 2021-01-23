while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    print("3. LTC-USDT")
    print("4. BCH-USDT")
    print("5. LINK-USDT")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001
        leverage        = 15
        threshold       = 1.5
        round_decimal   = 2
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.01
        leverage        = 10
        threshold       = 1.5
        round_decimal   = 2
        break

    elif (input_pair == '3') or (input_pair == 'LTC'):
        coin            = "LTC"
        quantity        = 0.1
        leverage        = 10
        threshold       = 1.5
        round_decimal   = 2
        break

    elif (input_pair == '4') or (input_pair == 'BCH'):
        coin            = "BCH"
        quantity        = 0.05
        leverage        = 15
        threshold       = 1.5
        round_decimal   = 2
        break

    elif (input_pair == '5') or (input_pair == 'LINK'):
        coin            = "LINK"
        quantity        = 1
        leverage        = 15
        threshold       = 1.5
        round_decimal   = 3
        break

    elif (input_pair == '6') or (input_pair == 'SUSHI'):
        coin            = "SUSHI"
        quantity        = 2
        leverage        = 10
        threshold       = 1.5
        round_decimal   = 4
        break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Leverage         :   " + str(leverage) + "x")
print("Entry Threshold  :   " + str(threshold) + " %\n")
