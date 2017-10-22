#!/usr/bin/env python
#-*- coding: utf-8 -*-

#update interval
t_step = 30
OFF_time = 1200

#######################################################
# Starting the internet part
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import threading

import time
import re

url = r'http://www.mvg-live.de/MvgLive/MvgLive.jsp#haltestelle=Olympiazentrum&gehweg=0&zeilen=7&ubahn=true&bus=false&tram=false&sbahn=false'
phantomjs_path = r'/usr/bin/phantomjs'
# driver = webdriver.PhantomJS()  # or add to your PATH

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
dcap = DesiredCapabilities.PHANTOMJS

driver = webdriver.PhantomJS(executable_path=phantomjs_path,
				desired_capabilities=dcap,
				service_args=['--ignore-ssl-errors=true',
				 '--ssl-protocol=any',
				 '--web-security=false'])

# driver = webdriver.PhantomJS(executable_path=phantomjs_path)



# driver.set_window_size(1024, 768)  # optional
driver.get(url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.ID,'mvgDepartureView')))
# wait.until(EC.presence_of_element_located((By.ID, 'mvgDepartureView')))

str_to_show = '    '
driver.save_screenshot('/home/pi/Desktop/MVG/loaded.png')


# driver.save_screenshot('screen.png') # save a screenshot to disk

def get_mvg_display():

	global element, wait, str_to_show

	print("in mvg_display func!")
	times = [int(uStr) for uStr in re.findall(r'F\xfcrstenried West Abfahrt in Minuten (\d+)', element.text)]

	print(times)
	if len(times) == 0:
		driver.save_screenshot('/home/pi/Desktop/MVG/No_times.png')
		str_to_show = '    '
		driver.get(url)
                element = wait.until(EC.visibility_of_element_located((By.ID,'mvgDepartureView')))
		# wait.until(EC.presence_of_element_located((By.ID, 'mvgDepartureView')))
		threading.Timer(t_step, get_mvg_display).start()
		return None
	elif len(times) == 1:
                driver.save_screenshot('/home/pi/Desktop/MVG/times.png')
		str_to_show = str(times[0]).ljust(4)
		threading.Timer(t_step, get_mvg_display).start()
		return None
	else:
                driver.save_screenshot('/home/pi/Desktop/MVG/times.png')
		str_to_show = str(times[0]).ljust(2) + str(times[1]).rjust(2)
		threading.Timer(t_step, get_mvg_display).start()
		return None






#############################################################################################################
# Starting the display part
# code modified, tweaked and tailored from code by bertwert
# http://raspi.tv/2015/how-to-drive-a-7-segment-display-directly-on-raspberry-pi-in-python

# on RPi forum thread topic 91796
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

# GPIO ports for the 7seg pins

# segments = (11, 4, 23, 8, 7, 10, 18, 25)#Original from the internet

#segments = (40, 36, 35, 31, 29, 38, 37, 33)
segments =  (21, 16, 19,  6,  5, 20, 26, 13)

# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

for segment in segments:
	GPIO.setup(segment, GPIO.OUT)
	GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins

# digits = (22, 27, 17, 24)#Original from the website

#digits = (3, 5, 7, 8)
digits =  (2, 3, 4, 14)

# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively

for digit in digits:
	GPIO.setup(digit, GPIO.OUT)
	GPIO.output(digit, 1)

num = {' ': (0, 0, 0, 0, 0, 0, 0),
       '0': (1, 1, 1, 1, 1, 1, 0),
       '1': (0, 1, 1, 0, 0, 0, 0),
       '2': (1, 1, 0, 1, 1, 0, 1),
       '3': (1, 1, 1, 1, 0, 0, 1),
       '4': (0, 1, 1, 0, 0, 1, 1),
       '5': (1, 0, 1, 1, 0, 1, 1),
       '6': (1, 0, 1, 1, 1, 1, 1),
       '7': (1, 1, 1, 0, 0, 0, 0),
       '8': (1, 1, 1, 1, 1, 1, 1),
       '9': (1, 1, 1, 1, 0, 1, 1)}


ON_time = time.time()
get_mvg_display()

try:
	s = str_to_show
	start_time = time.time()

	while (True):
		if time.time() - ON_time > OFF_time:
			os.system('sudo shutdown -h now')

		s = str_to_show
		
		for digit in range(4):
			for loop in range(0, 7):
				GPIO.output(segments[loop], num[s[digit]][loop])
                                
				'''
				if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
					GPIO.output(25, 1)
				else:
					GPIO.output(25, 0)
					'''
			GPIO.output(digits[digit], 0)
			time.sleep(0.001)
			GPIO.output(digits[digit], 1)
finally:
	GPIO.cleanup()
