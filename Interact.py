import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from Modules import Module
import numpy as np
from pykeigan import utils
from pykeigan import usbcontroller


class Interact(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def v_operator(self):
        # print("interact started")
        stop = False
        accumulative = 0
        t = 0
        temp = 0
        def_pos = 0
        while self.p["play"] <= 90:
            t += 1  # このtでランダムな移動を作る


            if t >= temp:
                t = 0
                temp = random.randint(20, 60)

                if self.p["sleep"] <= 50:
                    def_pos = random.randint(35, 55)
                else:
                    def_pos = random.randint(45, 65)

                # self.dev.set_speed(utils.rpm2rad_per_sec(30))
                self.dev.set_speed(utils.deg2rad(40))
                self.dev.move_to_pos(utils.deg2rad(-def_pos))


            # 報酬の処理
            self.p["play"] = self.p["play"] + 0.01  # 0.06
            if np.var(np.array(self.s["touch"])[:, 0]) + np.var(np.array(self.s["touch"])[:, 1]) + np.var(np.array(self.s["touch"])[:, 2]) >= 2000:
                accumulative += 1
            else:
                accumulative -= 0.1
                if accumulative <= 0:
                    accumulative = 0
            if accumulative >= 22:
                accumulative = 0
                self.p["play"] = self.p["play"] + 15
                self.dev.set_speed(utils.deg2rad(640))
                for i in range(5):
                    self.dev.move_to_pos(utils.deg2rad(-def_pos))
                    time.sleep(0.18)
                    self.dev.move_to_pos(utils.deg2rad(-def_pos + 20))
                    time.sleep(0.18)

            print(
                "\033[" + str(39) + ";2H\033[2K" + "=================== touch " + str(accumulative) +  "====" +str(
                    np.var(np.array(self.s["touch"])[:, 0])) + "|" + str(np.var(np.array(self.s["touch"])[:, 1])) +
                "|" + str(np.var(np.array(self.s["touch"])[:, 2])), end = "")

            # 中断の処理
            time.sleep(0.1)
            if self.stopper:
                self.stopper = False
                stop = True
                print("play cancelled")
                break

            print("\033[" + str(24) + ";2H\033[2K" + "playing score: " + str(accumulative), end="")

        if not stop:
            print("play finished")
            self.finisher()

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

