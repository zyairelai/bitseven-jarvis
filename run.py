try:
    import os, time, requests, socket, urllib3
    import config, strategy
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    if strategy.position_information()[0].get('marginType') != "cross": strategy.change_margin_to_CROSSED()
    if int(strategy.position_information()[0].get("leverage")) != config.leverage:
        strategy.change_leverage(config.leverage)
        print(colored("CHANGED LEVERAGE :   " + strategy.position_information()[0].get("leverage") + "x\n", "red"))

    def lets_make_some_money():
        strategy.play_with_fire()

    while True:
        try:
            scheduler = BlockingScheduler()
            scheduler.add_job(lets_make_some_money, 'cron', second='0,20,40')
            scheduler.start()

        except (OSError, KeyError,
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
