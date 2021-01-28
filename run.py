try:
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

    print()

    prompt_LIVE = input("Enable Live Trade? [Y/n] ")
    if prompt_LIVE == 'Y': 
        live_trade = True
        print(colored("Live Trade Enabled", "green"))
    else: live_trade = False

    prompt_TSL = input("Enable Trailing Stop? [Y/n] ")
    if prompt_TSL == 'Y': 
        trailing_stop = True
        print(colored("Trailing Stop Enabled", "green"))
    else: trailing_stop = False

    print()

    def trade_action():
        main_hour = 6
        mini_hour = 4

        title          = "ACTION           :   "
        check_position = position_info()
        
        main_direction = heikin_ashi(main_hour)
        mini_direction = heikin_ashi(mini_hour)
        entry_confirmation = heikin_ashi(1)

        if check_position == "LONGING":
            if (main_direction != "GREEN") or (mini_direction != "GREEN") or ((pencil_wick_test(main_hour, "GREEN") == "FAIL") or (pencil_wick_test(mini_hour, "GREEN") == "FAIL")):
                print(title + "💰 CLOSE_LONG 💰")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored(title + "HOLDING_LONG", "green"))

        elif check_position == "SHORTING":
            if (main_direction != "RED") or (mini_direction != "RED") or ((pencil_wick_test(main_hour, "RED") == "FAIL") or (pencil_wick_test(mini_hour, "RED") == "FAIL")):
                print(title + "💰 CLOSE_SHORT 💰")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored(title + "HOLDING_SHORT", "red"))

        else:
            binance_futures.cancel_all_open_orders()
            if (main_direction == "GREEN") and (mini_direction == "GREEN") and (entry_confirmation == "GREEN") and ((pencil_wick_test(main_hour, "GREEN") == "PASS") or (pencil_wick_test(mini_hour, "GREEN") == "PASS")):
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
                if live_trade: 
                    binance_futures.open_position("LONG")
                    if trailing_stop: binance_futures.set_trailing_stop("LONG")

            elif (main_direction == "RED") and (mini_direction == "RED") and (entry_confirmation == "RED") and ((pencil_wick_test(main_hour, "RED") == "PASS") or (pencil_wick_test(mini_hour, "RED") == "PASS")):
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
                # scheduler.add_job(trade_action, 'interval', minute='3')
                scheduler.add_job(trade_action, 'cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
                scheduler.start()
            else:
                trade_action()
                time.sleep(3)

        # except Exception as e:
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

except KeyboardInterrupt: print("\n\nAborted.\n")
