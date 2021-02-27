try:
    import os, time, requests, socket, urllib3
    import config, heikin_ashi
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    def lets_make_some_money():
        heikin_ashi.lets_make_some_money()

    while True:
        try:
            scheduler = BlockingScheduler()
            scheduler.add_job(lets_make_some_money, 'cron', minute='30')
            scheduler.start()

        except (KeyError,
                socket.timeout,
                BinanceAPIException,
                ConnectionResetError,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout) as e:

            if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
            with open((os.path.join("Error_Message", config.coin + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.coin + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")
