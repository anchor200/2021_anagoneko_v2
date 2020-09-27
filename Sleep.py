import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from Modules import Module


class Sleep(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def is_active(self, physio):
        if physio["sleep"] <= 30:
            return True
        else:
            return False

    def v_operator(self):
        print("sleep started")
        stop = False
        while self.p["sleep"] <= 90:
            # @お家に変える
            print("\033[" + str(24) + ";2H\033[2K" + "sleeping", end="")
            # print("sleeping")
            self.p["sleep"] = self.p["sleep"] + 0.1
            time.sleep(0.1)
            if self.stopper:
                self.stopper = False
                stop = True
                print("sleep cancelled")
                break

        if not stop:
            print("sleep finished")
            self.finisher()

        print("\033[" + str(24) + ";2H\033[2K" + "", end="")

        return