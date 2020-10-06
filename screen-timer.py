"""This is a screen timer I wrote for the BBC microbit, because I was tired of telling
them when to stop playing on their phones. Connect a buzzer between pin 0 and ground.
Copy and paste the source code into https://python.microbit.org/v/2.0 then download the
hex. Press the A/B buttons to increase/decrease the interval in units of 15 minutes.
The remaining time is shown by the LEDs: each LED represents 5 minutes. When there is
less than 10 minutes left, the display shows the remaining minutes as a digit. The
buzzer sounds at half-time, on every minute for the last five minutes, and then
continuously when the time is up."""

import utime
from microbit import *

class Schedule:
    """Run some code with the given interval (in ms)"""
    def __init__(self, interval=1000):
        self.interval = interval
        self.last_update_ticks = utime.ticks_ms()

    def reset(self):
        self.last_update_ticks = utime.ticks_ms()

    def tick(self):
        """Call me in the event loop"""
        now = utime.ticks_ms()
        while utime.ticks_diff(now, self.last_update_ticks) >= self.interval:
            self._fire()
            self.last_update_ticks += self.interval

    def _fire(self):
        """Override me"""
        pass

class Alarm(Schedule):
    """Sends a repeating pattern of 1s and 0s to pin 0"""
    def __init__(self, pattern, repeat=False, interval=100):
        super().__init__(interval)
        self.pattern = pattern
        self.repeat = repeat
        self.active = None

    def set(self):
        self.active = self.pattern

    def reset(self):
        super().reset()
        self.active = None

    def _fire(self):
        if self.active is None:
            return
        pin0.write_digital(int(self.active[0]))
        self.active = self.active[1:]
        if len(self.active) == 0:
            if self.repeat:
                self.active = self.pattern
            else:
                self.active = None

class Timer(Schedule):
    """The main countdown timer"""
    def __init__(self):
        super().__init__(60000)
        self.mins_left = None
        self.button_alarm = Alarm("110")        # Sounds when a button is pressed
        self.half_time_alarm = Alarm("111000111000111000")  # Sounds at half time
        self.countdown_alarm = Alarm("1010")    # Sounds in the last 5 minutes
        self.final_alarm = Alarm("111000", True)    # Sounds when the timer ends
        self.half_time = None

    def _draw(self):
        mins = self.mins_left
        if mins <= 9:
            display.show(str(mins))
        else:
            image = ""
            for i in range(29):
                if i % 6 == 5:
                    image += ":"
                elif mins > 0:
                    image += "9"
                    mins -= 3
                else:
                    image += "0"
            display.show(Image(image))

    def start(self, mins):
        self.mins_left = mins
        self.button_alarm.set()
        self.half_time_alarm.reset()
        self.countdown_alarm.reset()
        self.final_alarm.reset()
        if mins >= 30:
            self.half_time = mins // 2
        else:
            self.half_time = None
        self.reset()
        self._draw()

    def tick(self):
        super().tick()
        self.button_alarm.tick()
        self.half_time_alarm.tick()
        self.countdown_alarm.tick()
        self.final_alarm.tick()

    def _fire(self):
        if self.mins_left > 0:
            self.mins_left -= 1
            if self.mins_left == 0:
                self.final_alarm.set()
            elif self.mins_left == self.half_time:
                self.half_time_alarm.set()
            elif self.mins_left <= 5:
                self.countdown_alarm.set()
        self._draw()

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

timer = Timer()
timer.start(60)
while True:
    if button_a.was_pressed():
        timer.incr()
    if button_b.was_pressed():
        timer.decr()
    timer.tick()
