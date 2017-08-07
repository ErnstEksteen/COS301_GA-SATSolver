import atexit
from time import time
from datetime import timedelta


def seconds_to_str(t):
    return str(timedelta(seconds=t))

line = "="*70


def log(s, divisor=None):
    print(line)
    print(seconds_to_str((time()-init)/divisor) if divisor else print(seconds_to_str(time() - init), '-', s), '-', s)
    print(line)
    print()


def endlog():
    global init
    end = time()
    init = programStartTime
    log("End Program")


def now():
    return seconds_to_str(time())


def start():
    global init
    init = time()

init = time()
programStartTime = time()
atexit.register(endlog)
log("Start Program")
