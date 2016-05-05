# code from runciter in #python
import os
import sys
import time
import signal
import threading


class PleaseRestart(Exception):
    pass


MAIN_THREAD_ID = threading.main_thread().ident


def restart(*args, **kwargs):
    raise PleaseRestart


signal.signal(signal.SIGUSR2, restart)
signal.siginterrupt(signal.SIGUSR2, True)


def btn_cb(channel):
    time.sleep(1)
    signal.pthread_kill(MAIN_THREAD_ID, signal.SIGUSR2)


def main():
    print("\nLoader Controller")
    try:
        wo_scan = input("Scan Work Order: ")
    except PleaseRestart:
        return
    print("\nWork Order #" + wo_scan)
    print()


def run():
    thread = threading.Thread(target=btn_cb, args=(None,))
    thread.start()

    while True:
        try:
            main()
        except:
            sys.exit()

if __name__ == '__main__':
    run()
