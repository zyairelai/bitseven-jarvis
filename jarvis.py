import os, time
import heikin_ashi
import binance_api
from datetime import datetime
from termcolor import colored

def go():
    six_hour      = heikin_ashi.get_hour(6)
    four_hour     = heikin_ashi.get_hour(4)
    one_hour      = heikin_ashi.get_hour(1)
    five_minute   = heikin_ashi.get_current_minute(5)
    one_minute    = heikin_ashi.get_current_minute(1)
    previous_volume = binance_api.get_volume("PREVIOUS", "1HOUR")
    current_volume  = binance_api.get_volume("CURRENT", "1HOUR")

    if (six_hour == "GREEN" or four_hour == "GREEN") and volume_confirmation(previous_volume, current_volume):
        if GO_LONG(one_minute, five_minute, one_hour):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
        else: print("ACTION           :   🐺 WAIT 🐺")

    elif (six_hour == "RED" or four_hour == "RED") and volume_confirmation(previous_volume, current_volume):
        if GO_SHORT(one_minute, five_minute, one_hour):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
        else: print("ACTION           :   🐺 WAIT 🐺")

    else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

from heikin_ashi import pattern_broken
from heikin_ashi import pencil_wick_test

def GO_LONG(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "GREEN") and (pencil_wick_test("GREEN", "1MINUTE") == "PASS")) and \
       (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (pencil_wick_test("GREEN", "5MINUTE") == "PASS")) and \
       ((one_hour == "GREEN") and (pencil_wick_test("RED", "1HOUR") == "FAIL")): return True

def GO_SHORT(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "RED") and (pencil_wick_test("RED", "1MINUTE") == "PASS")) and \
       (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (pencil_wick_test("RED", "5MINUTE") == "PASS")) and \
       ((one_hour == "RED") and (pencil_wick_test("GREEN", "1HOUR") == "FAIL")): return True

def volume_confirmation(previous_volume, current_volume):
    return (current_volume > (previous_volume / 5))

while True:
    go()
    time.sleep(1)