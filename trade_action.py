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

title          = "ACTION           :   "
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

def pencil_6entry_4exit():
    main_hour = 6
    mini_hour = 4

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

def standard_6entry_1exit():
    main_hour = 6
    mini_hour = 1

    check_position = position_info()
    main_direction = heikin_ashi(main_hour)
    mini_direction = heikin_ashi(mini_hour)

    if check_position == "LONGING":
        if (main_direction != "GREEN") or (mini_direction != "GREEN"):
            print(title + "💰 CLOSE_LONG 💰")
            if live_trade: binance_futures.close_position("LONG")
        else: print(colored(title + "HOLDING_LONG", "green"))

    elif check_position == "SHORTING":
        if (main_direction != "RED") or (mini_direction != "RED"):
            print(title + "💰 CLOSE_SHORT 💰")
            if live_trade: binance_futures.close_position("SHORT")
        else: print(colored(title + "HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if (main_direction == "GREEN") and (mini_direction == "GREEN"):
            print(colored(title + "🚀 GO_LONG 🚀", "green"))
            if live_trade: 
                binance_futures.open_position("LONG")
                if trailing_stop: binance_futures.set_trailing_stop("LONG")

        elif (main_direction == "RED") and (mini_direction == "RED"):
            print(colored(title + "💥 GO_SHORT 💥", "red"))
            if live_trade: 
                binance_futures.open_position("SHORT")
                if trailing_stop: binance_futures.set_trailing_stop("SHORT")

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def pure_6_hour():
    check_position = position_info()
    if check_position == "LONGING":
        if (heikin_ashi(6) != "GREEN"):
            print(title + "💰 CLOSE_LONG 💰")
            if live_trade: binance_futures.close_position("LONG")
        else: print(colored(title + "HOLDING_LONG", "green"))

    elif check_position == "SHORTING":
        if (heikin_ashi(6) != "RED"):
            print(title + "💰 CLOSE_SHORT 💰")
            if live_trade: binance_futures.close_position("SHORT")
        else: print(colored(title + "HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if (heikin_ashi(6) == "GREEN"):
            print(colored(title + "🚀 GO_LONG 🚀", "green"))
            if live_trade: 
                binance_futures.open_position("LONG")
                if trailing_stop: binance_futures.set_trailing_stop("LONG")

        elif (heikin_ashi(6) == "RED"):
            print(colored(title + "💥 GO_SHORT 💥", "red"))
            if live_trade: 
                binance_futures.open_position("SHORT")
                if trailing_stop: binance_futures.set_trailing_stop("SHORT")

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")