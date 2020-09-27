import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from Modules import Module


class Interact(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def v_operator(self):
        print("interact started")
        stop = False
        accumlative = 0
        t = 0
        while self.p["play"] <= 90:
            t += 0  # このtでランダムな移動を作る
            print("\033[" + str(24) + ";2H\033[2K" + "playing score: " + str(accumlative), end="")

            # self.p["play"] = self.p["play"] + 0.06
            self.p["play"] = self.p["play"] + 0.01
            accumlative = self.play_update()
            if accumlative >= 20:
                accumlative = 0
                self.p["play"] = self.p["play"] + 20
                # @喜びの舞

            time.sleep(0.1)
            if self.stopper:
                self.stopper = False
                stop = True
                print("play cancelled")
                break

        if not stop:
            print("play finished")
            self.finisher()

        print("\033[" + str(24) + ";2H\033[2K" + "", end="")
        return

    def is_active(self, physio):
        if physio["play"] <= 30:
            return True
        elif physio["play"] <= 70 and  random.random() <= 1 / 40000 * (physio["play"] - 70)*(physio["play"] - 70):
            return True
        else:
            return False

    def play_touch(self):
        return False

    def play_torque(self):
        return False

    def play_update(self):
        return 0
