import config
import entry_exit
import heikin_ashi
import pencil_wick
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored

def dead_or_alive():
    position_info = get_position.get_position_info()
    if config.clear_direction: direction = heikin_ashi.get_clear_direction()
    else: direction = heikin_ashi.get_hour(6)
    five_minute   = heikin_ashi.get_current_minute(5)
    one_minute    = heikin_ashi.get_current_minute(1)
    # exit_minute   = heikin_ashi.exit_minute()

    if position_info == "LONGING":
        # if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or entry_exit.EMERGENCY_EXIT_LONG(five_minute):
        # if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or entry_exit.EMERGENCY_EXIT("LONG"):
        if entry_exit.EMERGENCY_EXIT("LONG"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        # if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or entry_exit.EMERGENCY_EXIT_SHORT(five_minute):
        # if ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(exit_minute)) or entry_exit.EMERGENCY_EXIT("SHORT"):
        if entry_exit.EMERGENCY_EXIT("SHORT"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()

        if direction == "UP_TREND":
            if entry_exit.GO_LONG(one_minute, five_minute):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "DOWN_TREND":
            if entry_exit.GO_SHORT(one_minute, five_minute):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
