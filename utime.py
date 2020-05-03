import math
import time

def ticks_ms():
    return math.floor(time.time() * 1000)

def ticks_diff(a, b):
    return a - b

def sleep_ms(ms):
    time.sleep(ms / 1000)
