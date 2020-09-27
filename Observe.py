import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from Modules import Module


class Observe(Module):
    def __init__(self):
        super().__init__()
        self.param = {"obs_angle": 15}

    def is_active(self, physio):
        if physio["obs"] <= 30:
            return True
        else:
            return False

    def v_operator(self):
        print("observation started")
        t = 0
        stop = False
        # @様子を見る動きを作る
        while t <= 10:
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