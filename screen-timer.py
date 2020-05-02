# Add your Python code here. E.g.
import time
from microbit import *

def get_time_image(mins):
    if mins <= 9:
        return mins
    image = ""
    for i in range(29):
        if i % 6 == 5:
            image += ":"
        elif mins > 0:
            image += "9"
            mins -= 3
        else:
            image += "0"
    return Image(image)

class Timer():
    def __init__(self):
        self.last_update_ticks = None
        self.mins_left = None
        self.alarm = False

    def _draw(self):
        display.show(get_time_image(self.mins_left))

    def start(self, mins):
        self.mins_left = mins
        self.last_update_ticks = time.ticks_ms()
        self.alarm = False
        self._draw()

    def update(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_update_ticks) >= 60000:
            if self.mins_left > 0:
                self.mins_left -= 1
                if self.mins_left == 0:
                    self.alarm = True
            self._draw()
            self.last_update_ticks = now

    def incr(self):
        fill_up = 15 - self.mins_left % 15
        if fill_up > 0:
            self.mins_left += fill_up
        else:
            self.mins_left += 15
        self.start(self.mins_left)

    def decr(self):
        if self.mins_left > 0:
            fill_down = self.mins_left % 15
            if fill_down > 0:
                self.mins_left -= fill_down
            else:
                self.mins_left -= 15
            self.start(self.mins_left)
    
    def check_alarm(self):
        alarm = self.alarm
        self.alarm = False
        return alarm

def beep():
    for i in range(1, 7):
        pin0.write_digital(i % 2)
        time.sleep_ms(500)

timer = Timer()
timer.start(30)
while True:
    if button_a.was_pressed():
        timer.incr()
    if button_b.was_pressed():
        timer.decr()
    timer.update()
    if timer.check_alarm():
        beep()
