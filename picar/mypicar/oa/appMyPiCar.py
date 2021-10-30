#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 方向及车速控制
#
#

import os
from time import sleep
from flask import Flask, render_template, request, Response

import RPi.GPIO as GPIO
import time
import stateCtrl as SC

app = Flask(__name__)

global speed
speed = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#######PWM车速控制###########
ENA = 33  # //L298使能A
ENB = 35  # //L298使能B

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
leftpwm = GPIO.PWM(ENA, 1000)
rightpwm = GPIO.PWM(ENB, 1000)
leftpwm.start(100)
rightpwm.start(100)
print('pwm start')
#######PWM车速控制###########


@app.route('/')
def index():
	"""Video streaming home page."""

	return render_template('index.html')

@app.route("/ctrl/<state>")
def ctrl(state):
		car = SC.stateCtrl()
		if state == "t_up":
			car.t_up()
		elif state == "t_down":
			car.t_down()
		elif state == "t_left":
			car.t_left()
		elif state == "t_right":
			car.t_right()
		elif state == 't_stop':
			car.t_stop()
		return render_template('index.html')


@app.route("/speed/<state>")
def speedChange(state):
		global speed
		car = SC.stateCtrl()
		if state == 'acc':
			speed = speed + 10
			if int(speed) >= 100:
				speed = 100
			# car.changeSpeed(int(speed))
			leftpwm.ChangeDutyCycle(int(speed))
			rightpwm.ChangeDutyCycle(int(speed))
		elif state == 'dec':
			speed = speed - 10
			if int(speed) <= 0:
				speed = 0
			leftpwm.ChangeDutyCycle(int(speed))
			rightpwm.ChangeDutyCycle(int(speed))
		else:
			speed == 60   #复位到60
			leftpwm.ChangeDutyCycle(int(speed))
			rightpwm.ChangeDutyCycle(int(speed))

		return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port =8000)

