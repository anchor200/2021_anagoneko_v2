import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from pykeigan import utils
from pykeigan import usbcontroller


class Module:
    def __init__(self):
        self.param = {}
        self.waiting = False
        self.stopper = False
        self.finished = False
        self.module_working = False
        self.p = {}  # physio
        self.s = {}  # sensor
        self.dev = None
        self.b = {}  # belief

    def is_active(self, physio):
        if random.random() <= 0.001:
            return True
        else:
            return False

    def v_operator(self):
        print("something started")
        t = 0
        stop = False
        while t <= 100:
            t += 1
            time.sleep(0.1)
            if self.stopper:
                self.stopper = False
                stop = True
                print("cancelled")
                break

        if not stop:
            print("finished")
            self.finisher()

        return

    def finisher(self):
        self.finished = True

    def module_loop(self):

        while True:
            # この中からoperatorを起動させる
            if self.waiting:
                self.waiting = False
                self.v_operator()

            time.sleep(0.01)

    def learner(self):
        pass
