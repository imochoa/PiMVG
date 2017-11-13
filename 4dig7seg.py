#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################
# Starting the internet part
from core import MVGTracker, mvg_pars_factory
import RPi.GPIO as GPIO
import time
import os

# Using BCM pin numbering
GPIO.setmode(GPIO.BCM)
segments = (21, 16, 19, 6, 5, 20, 26, 13)  # 7seg_segment_pins +  100R inline
digits = (2, 3, 4, 14)  # digit select pins

# Set as outputs
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

# what 7segments to light up for each number
num = {' ':  (0, 0, 0, 0, 0, 0, 0),
       '0':  (1, 1, 1, 1, 1, 1, 0),
       '1':  (0, 1, 1, 0, 0, 0, 0),
       '2':  (1, 1, 0, 1, 1, 0, 1),
       '3':  (1, 1, 1, 1, 0, 0, 1),
       '4':  (0, 1, 1, 0, 0, 1, 1),
       '5':  (1, 0, 1, 1, 0, 1, 1),
       '6':  (1, 0, 1, 1, 1, 1, 1),
       '7':  (1, 1, 1, 0, 0, 0, 0),
       '8':  (1, 1, 1, 1, 1, 1, 1),
       '9':  (1, 1, 1, 1, 0, 1, 1),
       's:': (1, 0, 1, 1, 0, 1, 1),
       '-:': (0, 0, 0, 1, 0, 0, 0),  # Might also be the last one...
       }


class FourDigSevSeg(MVGTracker):
    def __init__(self, mvg_pars, screen_timeout=None, update_interval=30):

        if screen_timeout > 0:
            self.screen_timeout = screen_timeout
        else:
            screen_timeout = None

        super(FourDigSevSeg, self).__init__(mvg_pars=mvg_pars, update_interval=update_interval)

    @staticmethod
    def factory(station,
                line=[],
                destination=[],
                max_time=None,
                min_time=None,
                screen_timeout=None,
                update_interval=30):
        mvg_pars = mvg_pars_factory(
                station, line=line, destination=destination, max_time=max_time, min_time=min_time)
        return FourDigSevSeg(mvg_pars=mvg_pars, screen_timeout=screen_timeout, update_interval=update_interval)

    @property
    def display_string(self):
        """
        Specially formatted display string for this type of display, the 4d7s display
        :return:
        """

        name, dep_time = self.return_next_departure()

        return '{0:>4}'.format(dep_time)

    def track(self):

        if self.screen_timeout > 0:  # display for an unlimited ammount of time?
            on_flag = False
            OFF_time = time.time() + self.screen_timeout * 60  # Time when the screen will turn off
        else:
            on_flag = True
            OFF_time = time.time()  # value will be ignored

	super(FourDigSevSeg, self).track() # Call the parent track method which actually starts the tracking
        try:
            while on_flag or (time.time() < OFF_time):
                # os.system('sudo shutdown -h now')

                s = self.display_string

                for digit in range(4):
                    for loop in range(0, 7):
                        # print("s[dtig] is "+str(s))
                        GPIO.output(segments[loop], num.get(s[digit], (0, 0, 0, 0, 0, 0, 0, 0))[loop])
                    GPIO.output(digits[digit], 0)
                    time.sleep(0.001)
                    GPIO.output(digits[digit], 1)
        finally:
            self.stop_tracking()
            GPIO.cleanup()


if __name__ == "__main__":

    pi_mvg = FourDigSevSeg.factory(station='Olympiazentrum',
                                   line=['u'],
                                   destination=['Fürstenried West'],
                                   screen_timeout=3,
                                   update_interval=5)

    pi_mvg.track()
