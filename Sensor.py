import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from pykeigan import utils
from pykeigan import usbcontroller
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1015()
GAIN = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class Sensor:
    def __init__(self, max_pos=70, border_pos=15):
        self.dev = None

    def sensor(self):

        measurement = self.dev.read_motor_measurement()
        pos = abs(measurement["position"] * 180 / math.pi)
        torque =  - measurement["torque"]
        food = GPIO.input(37)

        head = adc.read_adc(1, gain=GAIN)
        body = adc.read_adc(0, gain=GAIN)
        tail = adc.read_adc(2, gain=GAIN)
        sound = adc.read_adc(3, gain=1)

        sens = {"food": food, "sound": sound, "touch": [head,body,tail], "torque": torque, "pos": pos}
        print("\033[" + str(44) + ";2H\033[2K" + str(sens), end="")
        return sens

