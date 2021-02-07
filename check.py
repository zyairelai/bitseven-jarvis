import time

def check():
    while True:
        print("What do you want to check? ")
        print("1. trend")
        print("2. position")
        print("3. realizedPNL")
        input_num = input("\nEnter a number   :   ") or '1'

        if (input_num == '1'):
            start = time.time()
            import heikin_ashi
            heikin_ashi.get_clear_direction(6)
            heikin_ashi.get_hour(4)
            heikin_ashi.get_hour(1)
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '2'):
            start = time.time()
            from position import position_info
            print("\nThe <position.py> return value is : " + position_info())
            print(f"Time Taken: {time.time() - start} seconds\n")
            break

        elif (input_num == '3'):
            import realizedPNL
            break

        else: print("❗Invalid Number❗Try again❗\n")

try: check()
except KeyboardInterrupt: print("\n\nAborted.\n")
