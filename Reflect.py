import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
import numpy as np
from Modules import Module
from pykeigan import utils
from pykeigan import usbcontroller


class Reflect(Module):
    def __init__(self):
        super().__init__()
        self.param = {}
        self.cum_sound = 0
        self.cum_torque = 0

    def is_active(self, physio):  # pとsで決まるようにする
        if random.random() <= 0.00 or self.ref_sound() or self.ref_touch() or self.ref_torque():
            return True
        else:
            return False

    def ref_touch(self):  # 強いものが来ると反応
        return False

    def ref_torque(self):  # 強いものが来ると反応

        if abs(self.s["torque"][-1]) >= 0.02:
            self.cum_torque += 1
        else:
            self.cum_torque -= 0.9
            if self.cum_torque < 0:
                self.cum_torque = 0
        if self.cum_torque >= 30 or (self.cum_torque >= 14 and np.var(np.array(self.s["pos_log"])) >= 40):
            self.cum_torque = 0
            return True

        print("\033[" + str(39) + ";2H\033[2K" + "=================== " + str(self.cum_torque) + "cum torque idouryo" + str(np.var(np.array(self.s["pos_log"]))), end="")

        if abs(self.s["torque"][-1]) >= 0.08 and self.s["pos"] <= 80:
            return True
        return False

    def ref_sound(self):
        # deque内の累計値で、sleepの深さによって反応性が違うようにする
        # とりあえず寝てるのを起こすだけにする0928
        ## print("\033[" + str(39) + ";2H\033[2K" + "=================== " + str(self.cum_sound) + "== sound var" + str(np.var(np.array(self.s["sound"]))), end="")
        if np.var(np.array(self.s["sound"])) >= 200:
            self.cum_sound += 1
        else:
            self.cum_sound -= 0.5
            if self.cum_sound < 0:
                self.cum_sound = 0

        if self.s["pos"] <= 20 and self.p["sleep"] >= 30:  # 隠れているときだけ、の意味
            if self.cum_sound >= 90 - self.p["sleep"]:
                self.cum_sound = 0
                return True

        return False

    def fight_flight(self):
        if self.p["eat"] + self.p["sleep"] <= 60 and False:
            return "fight"
        else:
            return "flight"

    def v_operator(self):
        print("reflection started")
        if self.fight_flight() == "fight":
            pass
            # @暴れる
        else:
            print("\033[" + str(39) + ";2H\033[2K" + "flight", end="")
            self.dev.set_speed(utils.deg2rad(840))
            self.dev.set_curve_type(2)
            self.dev.set_acc(200)
            self.dev.set_max_torque(0.5)
            self.dev.move_to_pos(utils.deg2rad(min(self.s["pos"] + 40, 0)))
            time.sleep(2)


        print("finished")
        self.finisher()
        self.dev.set_max_torque(0.03)
        self.dev.set_speed(utils.deg2rad(180))
        self.dev.set_curve_type(1)
        self.dev.set_acc(100)