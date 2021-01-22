try:
    live_trade = False

    import os
    import time
    import requests
    import socket
    import urllib3
    import config
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from heikin_ashi import heikin_ashi
    from get_position import get_position_info
    from binance.exceptions import BinanceAPIException

    def trade_action():
        title           = "ACTION           :   "
        position_info   = get_position_info()
        main_direction  = heikin_ashi(6)
        entry_direction = heikin_ashi(1)

        if position_info == "LONGING":
            if (entry_direction == "DOWN_TREND"):
                print(title + "💰 CLOSE_LONG 💰")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored(title + "HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            if (entry_direction == "UP_TREND"):
                print(title + "💰 CLOSE_SHORT 💰")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored(title + "HOLDING_SHORT", "red"))

        else:
            if main_direction == "UP_TREND" and (entry_direction == "UP_TREND"):
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
                if live_trade: binance_futures.open_position("LONG")

            elif main_direction == "DOWN_TREND" and (entry_direction == "DOWN_TREND"):
                print(colored(title + "💥 GO_SHORT 💥", "red"))
                if live_trade: binance_futures.open_position("SHORT")

            else: print(title + "🐺 WAIT 🐺")

    # Initialize SETUP
    binance_futures.change_leverage()
    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()

    while True:
        try:    trade_action()
        except (BinanceAPIException,
                ConnectionResetError,
                socket.timeout,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout) as e:

            if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
            with open((os.path.join("Error_Message", config.pair + ".txt")), "a") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")
            continue

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
        time.sleep(10)

except KeyboardInterrupt: print("\n\nAborted.\n")
