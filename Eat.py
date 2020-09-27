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


class Eat(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def v_operator(self):
        # print("\033[" + str(50) + ";2H\033[2K" + "eat module in action", end="")
        stop = False
        t = 0
        def_pos = 10
        self.dev.set_max_torque(0.03)

        while self.p["eat"] <= 80:
            if self.p["sleep"] <= 50:
                def_pos = random.randint(0, 10)
            else:
                def_pos = random.randint(35, 55)

            # self.dev.set_speed(utils.rpm2rad_per_sec(30))
            self.dev.set_speed(utils.deg2rad(180))
            self.dev.move_to_pos(utils.deg2rad(-def_pos))

            temp = random.randint(30, 60)
            t = 0
            while t <= temp:
                t += 1
                time.sleep(0.1)
                if self.stopper:
                    self.stopper = False
                    stop = True
                    break
            if stop:
                print("eat cancelled on waiting")
                break

            if random.choice([False, False, True]):
                def_pos = 0
                self.dev.move_to_pos(utils.deg2rad(-def_pos))

                temp = random.randint(10, 40)
                t = 0
                while t <= temp:
                    t += 1
                    time.sleep(0.1)
                    if self.stopper:
                        self.stopper = False
                        stop = True
                        break
                if stop:
                    print("eat cancelled on waiting")
                    break


            is_flying = False
            if self.b["food"]:
                if self.p["sleep"] <= 50:
                    self.dev.set_speed(utils.deg2rad(random.randint(20,50)))
                else:
                    self.dev.set_speed(utils.deg2rad(840))
                    self.dev.set_curve_type(2)
                    self.dev.set_acc(200)
                self.dev.set_max_torque(0.4)
                self.dev.move_to_pos(utils.deg2rad(-130))  # 押しに行く
                is_flying = True

            if is_flying:
                while True:
                    if self.stopper:
                        self.stopper = False
                        stop = True
                        break

                    if not self.s["food"]:
                        if self.s["pos"] >= 85:
                            self.p["eat"] = self.p["eat"] + 30
                        break



            if self.stopper or stop:  # 食事を邪魔された場合はループから抜ける
                self.stopper = False
                stop = True
                print("eat cancelled on flight")
                self.dev.set_max_torque(0.03)
                self.dev.set_speed(utils.deg2rad(180))
                self.dev.set_curve_type(1)
                self.dev.set_acc(100)
                return

            if is_flying:  # 食った後は戻る
                self.dev.move_to_pos(utils.deg2rad(-def_pos))

            temp = random.randint(30, 60)
            t = 0
            while t <= temp:
                t += 1
                time.sleep(0.1)
                if self.stopper:
                    self.stopper = False
                    stop = True
                    break
            if stop:
                print("eat cancelled on waiting")
                break

            time.sleep(0.1)
            if self.stopper or stop:
                self.stopper = False
                stop = True
                print("eat cancelled on back")


        if not stop:
            print("eat finished")
            self.finisher()

        # print("\033[" + str(50) + ";2H\033[2K" + "snapped", end="")

        self.dev.set_max_torque(0.03)
        self.dev.set_speed(utils.deg2rad(180))
        self.dev.set_curve_type(1)
        self.dev.set_acc(100)

    def is_active(self, physio):
        if physio["eat"] <= 30:
            return True
        elif physio["eat"] <= 70 and random.random() <= 1 / 50000 * (physio["eat"] - 70)*(physio["eat"] - 70) and self.b["food"]:
            return True
        else:
            return False