import time
from collections import OrderedDict
import math
import asyncio
import functools
import time
import threading
import random
import sys
import os
os.system('clear')

class Body:
    def __init__(self):
        self.physio = dict(
            {"eat": 100.0, "sleep": 100.0, "play": 100.0, "obs": 0.0, "stan": 0.0, "warn": 0.0})  # すべて0-1
        self.p_decay = dict(
            {"eat": 10.0, "sleep": 3.0, "play": 3.0, "obs": 20.0, "stan": 0.0, "warn": 0.0})
        self.modules = {"reflector": Reflect(), "eater": Eat(), "sleeper": Sleep(), "interacter": Interact(), "observer": Observe()}  # [0]が一番優先度高い
        print("======= installed modules")
        for i in range(len(self.modules)):
            print("•" + str(list(self.modules.keys())[len(self.modules) - i - 1]))
        print("\n\n======= it got birth\n\n")

        self.max_pos = 70.0

        self.food = 0  # binary
        self.sound = 0  # binary
        self.touch = [0,0,0] # 頭,胸,腹 だいたいで正規化して1-10にする
        self.torque = 0 # だいたいで正規化して1-10にする


    def life(self):
        t = []
        for k in self.modules.keys():
            t.append(threading.Thread(target=self.modules[k].module_loop))
        for tt in t:
            tt.start()
        self.runner()


    def runner(self):
        active_layer = [-1, "none"]
        loop = asyncio.get_event_loop()
        while True:
            # print("working")
            temp_active_layer = active_layer
            self.sense(active_layer, temp_active_layer)  # 感覚入力を更新

            # 活性化しているモジュールを取得 (活性化はこの処理で、非活性化はもモジュールごとのv_operatorで行う(非可逆な基準))
            for i in range(len(self.modules)):
                if active_layer[0] >= 0 and i >= active_layer[0]:
                    break  # 自分より下位のレイヤーしか見ない(下位のレイヤーがアクティブになった場合はそちらが優先権を取る)
                temp_key = list(self.modules.keys())[i]

                if self.modules[temp_key].is_active(self.physio):
                    self.print_status(10, temp_key + " activated" + "\n")
                    # print(temp_key + " activated")
                    active_layer = [i, temp_key]
                    break

            if active_layer != temp_active_layer:
                # モジュールをスタートさせる
                # print("kill working module : " + temp_active_layer[1])
                self.print_status(10, "subsuming working module : " + temp_active_layer[1] + ", ")
                if temp_active_layer[0] >= 0:
                    self.modules[active_layer[1]].stopper = True
                self.print_status(10, '\033[30m' + "active module : " + '\033[0m' + active_layer[1] + "\n")
                # print("module start : " + active_layer[1])
                self.modules[active_layer[1]].p = self.physio
                self.modules[active_layer[1]].waiting = True

            if temp_active_layer[0] >= 0:
                # モジュールを終了させる
                if self.modules[active_layer[1]].finished:
                    active_layer = [-1, "none"]

            # 生理状態のシミュレーション
            self.physio_sim()
            self.show_physio()

            time.sleep(0.5)

    def updater(self):
        pass

    def physio_sim(self):
        dt = 0.01
        for k in self.physio.keys():
            self.physio[k] = self.physio[k] - math.sqrt(max(self.physio[k], 0.0)) * dt * self.p_decay[k]
        if self.sound:
            self.physio["obs"] = max(self.physio["obs"] - 50, 0)

    def sense(self, active_layer, temp_active_layer):
        if temp_active_layer[0] >= 0:
            self.modules[active_layer[1]].s = self.sensor()

    def sensor(self):  # 接続しているセンサーから入力を受け取る
        return {}

    def print_status(self, n, s):
        print("\033["+ str(n) + ";2H\033[2K" + s, end="")

    def show_physio(self):
        tt = 12
        self.print_status(tt,'\033[30m' + "======desire parameters: " + '\033[0m')
        for k in self.physio.keys():
            tt += 1
            s = k + "\t"
            for i in range(int(self.physio[k])):
                s += "|"
            self.print_status(tt, s)
        print("\n")


class Module:
    def __init__(self):
        self.param = {}
        self.waiting = False
        self.stopper = False
        self.finished = False
        self.p = {}  # physio
        self.s = {}  # sensor

    def is_active(self, physio):
        if random.random() <= 0.1:
            return True
        else:
            return False

    def v_operator(self):
        print("something started")
        t = 0
        while t <= 100:
            t += 1
            time.sleep(0.1)
            if self.stopper:
                print("cancelled")
                break

        print("waited or cancelled")

        self.finisher()

        return True

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

class Eat(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def v_operator(self):
        print("eat started")
        t = 0
        while t <= 100:
            t += 1
            time.sleep(0.1)
            if self.stopper:
                print("cancelled")
                break

        print("eat waited or cancelled")
        self.finisher()

class Sleep(Module):
    def __init__(self):
        super().__init__()
        self.param = {}


class Interact(Module):
    def __init__(self):
        super().__init__()
        self.param = {}


class Reflect(Module):
    def __init__(self):
        super().__init__()
        self.param = {}


class Observe(Module):
    def __init__(self):
        super().__init__()
        self.param = {"obs_angle": 15}



robot = Body()
robot.life()
