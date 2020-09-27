import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from Modules import Module
from pykeigan import utils
from pykeigan import usbcontroller


class Observe(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def is_active(self, physio):
        if physio["obs"] <= 30:
            return True
        else:
            return False

    def v_operator(self):
        print("observation started")

        stop = False

        self.dev.set_max_torque(0.03)
        self.dev.move_to_pos(utils.deg2rad(-30), (utils.deg2rad(90) / 3))
        t = 0
        while t <= 30:
            t += 1
            time.sleep(0.1)
            if self.stopper:
                self.stopper = False
                stop = True
                print("observation cancelled")
                break

        self.dev.move_to_pos(0.01)

        t = 0
        while t <= 20:
            t += 1
            time.sleep(0.1)
            if self.stopper:
                self.stopper = False
                stop = True
                print("observation cancelled")
                break

        if not stop:
            # self.p["obs"] = 100
            print("observation finished")
            self.finisher()