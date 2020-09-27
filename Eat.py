import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from Modules import Module


class Eat(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def v_operator(self):
        print("eat started")
        stop = False
        t = 0
        while self.p["eat"] <= 90:
            if t % 80 == 30:
                self.p["eat"] = self.p["eat"] + 30

            t += 1
            time.sleep(0.1)
            if self.stopper:
                self.stopper = False
                stop = True
                print("eat cancelled")
                break

        if not stop:
            print("eat finished")
            self.finisher()


    def is_active(self, physio):
        if physio["eat"] <= 30:
            return True
        elif physio["eat"] <= 70 and random.random() <= 1 / 50000 * (physio["eat"] - 70)*(physio["eat"] - 70):
            return True
        else:
            return False