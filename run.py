try:
    live_trade = True
    trailing_stop = False

    import os
    import time
    import requests
    import socket
    import urllib3
    import config
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from position import position_info
    from heikin_ashi import heikin_ashi
    from pencil_wick import pencil_wick_test
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    def trade_action():
        title          = "ACTION           :   "
        check_position = position_info()
        main_direction = heikin_ashi(6)
        mini_direction = heikin_ashi(1)
        entry_confirmation = heikin_ashi(30)

        if check_position == "LONGING":
            if (main_direction != "GREEN") or (pencil_wick_test(6, "GREEN") == "FAIL"):
                print(title + "💰 CLOSE_LONG 💰")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored(title + "HOLDING_LONG", "green"))

        elif check_position == "SHORTING":
            if (main_direction != "RED") or (pencil_wick_test(6, "RED") == "FAIL"):
                print(title + "💰 CLOSE_SHORT 💰")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored(title + "HOLDING_SHORT", "red"))

        else:
            if (main_direction == "GREEN") and (mini_direction == "GREEN") and (entry_confirmation == "GREEN") and (pencil_wick_test(6, "GREEN") == "PASS"):
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
                if live_trade: 
                    binance_futures.open_position("LONG")
                    if trailing_stop: binance_futures.set_trailing_stop("LONG")

            elif (main_direction == "RED") and (mini_direction == "RED") and (entry_confirmation == "RED") and (pencil_wick_test(6, "RED") == "PASS"):
                print(colored(title + "💥 GO_SHORT 💥", "red"))
                if live_trade: 
                    binance_futures.open_position("SHORT")
                    if trailing_stop: binance_futures.set_trailing_stop("SHORT")

            else: print(title + "🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

    # Initialize SETUP
    if live_trade:
        if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
        if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
            binance_futures.change_leverage()
            print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    while True:
        try:
            if live_trade:
                scheduler = BlockingScheduler()
                scheduler.add_job(trade_action, 'cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
                scheduler.start()
            else:
                trade_action()
                time.sleep(3)

        except Exception as e:
        # except (BinanceAPIException,
                # ConnectionResetError,
                # socket.timeout,
                # urllib3.exceptions.ProtocolError,
                # urllib3.exceptions.ReadTimeoutError,
                # requests.exceptions.ConnectionError,
                # requests.exceptions.ConnectTimeout,
                # requests.exceptions.ReadTimeout) as e:

            if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
            with open((os.path.join("Error_Message", config.pair + ".txt")), "a") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")
            continue

except KeyboardInterrupt: print("\n\nAborted.\n")
