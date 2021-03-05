try:
    import time
    import jarvis

    while True:
        jarvis.go()
        time.sleep(2)
except KeyboardInterrupt: print("\n\nAborted.\n")
