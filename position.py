import time
import config
import binance_futures
from termcolor import colored

def position_info(): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = "CURRENT POSITION :   "
    positionAmt = float(binance_futures.position_information()[0].get('positionAmt'))
    unRealizedProfit = round(float(binance_futures.position_information()[0].get('unRealizedProfit')), 4)
    # print(binance_futures.position_information()[0])

    if (positionAmt > 0):
        position = "LONGING"
        print(colored(title + position, "green"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "red"))

    elif (positionAmt < 0):
        position = "SHORTING"
        print(colored(title + position, "red"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "red"))

    else:
        position = "NO_POSITION"
        print(title + position)

    return position
