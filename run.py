try:
    import os
    import time
    import requests
    import socket
    import urllib3
    import config
    import heikin_ashi
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from position import position_info
    from pencil_wick import pencil_wick_test
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    print()

    prompt_LIVE = input("Enable Live Trade? [Y/n] ")
    if prompt_LIVE == 'Y': 
        live_trade = True
        print(colored("Live Trade Enabled", "green"))
    else: live_trade = False

    print()

    def trade_action():
        main_hour = 6
        mini_hour = 1

        title          = "ACTION           :   "
        check_position = position_info()
        
        main_direction = heikin_ashi.get_clear_direction(main_hour)
        mini_direction = heikin_ashi.get_clear_direction(mini_hour)

        if check_position == "LONGING":
            if (main_direction != "UP_TREND") or (mini_direction != "UP_TREND"):
                print(title + "💰 CLOSE_LONG 💰")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored(title + "HOLDING_LONG", "green"))

        elif check_position == "SHORTING":
            if (main_direction != "DOWN_TREND") or (mini_direction != "DOWN_TREND"):
                print(title + "💰 CLOSE_SHORT 💰")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored(title + "HOLDING_SHORT", "red"))

        else:
            binance_futures.cancel_all_open_orders()
            if (main_direction == "UP_TREND") and (mini_direction == "UP_TREND"):
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
                if live_trade: 
                    binance_futures.open_position("LONG")

            elif (main_direction == "DOWN_TREND") and (mini_direction == "DOWN_TREND"):
                print(colored(title + "💥 GO_SHORT 💥", "red"))
                if live_trade: 
                    binance_futures.open_position("SHORT")

            else: print(title + "🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

    def add_to_job():
        try: trade_action()
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

    if live_trade:
        # Initialize SETUP
        if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
        if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
            binance_futures.change_leverage()
            print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))
        
        scheduler = BlockingScheduler()
        scheduler.add_job(trade_action, 'interval', minute='10')
        # scheduler.add_job(add_to_job, 'cron', minute='0,5,10,15,20,25,30,35,40,45,50,55')
        scheduler.start()

    else:
        while True:
            try: 
                trade_action()
                time.sleep(10*60)

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
