import time
from collections import OrderedDict
import math
import asyncio
import functools
import time
import threading
import random
import sys
import argparse
import os
import numpy as np
os.system('clear')
from Eat import Eat
from Sleep import Sleep
from Observe import Observe
from Reflect import Reflect
from Interact import Interact
from Sensor import Sensor
from collections import deque
from pykeigan import utils
from pykeigan import usbcontroller


class Body:
    def __init__(self):
        self.physio = dict(
            {"eat": 100.0, "sleep": 10.0, "play": 100.0, "obs": 0.0, "stan": 0.0, "warn": 0.0})  # すべて0-1
        self.p_decay = dict(
            {"sleep": 2.0, "eat": 6.0, "play": 3.0, "obs": 20.0, "stan": 0.0, "warn": 0.0})
        self.modules = {"reflector": Reflect(), "sleeper": Sleep(), "eater": Eat(), "observer": Observe(), "player": Interact()}  # [0]が一番優先度高い

        self.belief = {"food": 0}
        print("======= installed modules")
        for i in range(len(self.modules)):
            print("•" + str(list(self.modules.keys())[len(self.modules) - i - 1]))
        print("\n\n======= it got birth\n\n")

        self.max_pos = 87.0
        self.border_pos = 25.0
        self.sensor = Sensor(self.max_pos, self.border_pos)

        self.sensor_info = {"food": 0, "sound": deque([0], maxlen=30), "touch": deque([0, 0, 0], maxlen=100),
                            "torque": deque([0], maxlen=100), "pos": 0, "pos_log": deque([0], maxlen=50)}  # 外からはreadonly

        for k in self.modules.keys():
            self.modules[k].s = self.sensor_info
            self.modules[k].p = self.physio
            self.modules[k].b = self.belief

        #self.food = 0  # binary
        #self.touch = [0,0,0] # 頭,胸,腹 だいたいで正規化して1-10にする
        #self.torque = 0 # だいたいで正規化して1-10にする

        self.action_log = {"none": 0, "sleeper": 0, "eater": 0, "player": 0}
        self.motor_init()


    def motor_init(self):
        parser = argparse.ArgumentParser(description='モーターに接続し、各種情報の取得')
        parser.add_argument('port', metavar='PORT', default='/dev/ttyUSB1', nargs='?',
                            help='モーターのデバイスファイル指定 (default:/dev/ttyUSB1)')
        args = parser.parse_args()
        self.dev = usbcontroller.USBController(args.port, False, baud=1000000)  # モーターのアドレス 参照 usb-simple-connection.py
        print("tsunagatta")
        self.dev.disable_action()
        self.dev.set_max_speed(utils.deg2rad(1000))
        time.sleep(2)
        self.dev.enable_action()
        self.dev.preset_position(0.0)
        self.dev.set_curve_type(1)
        self.dev.set_acc(100)
        self.dev.set_led(2, 0, 255, 255)
        self.dev.set_speed(utils.deg2rad(180))
        for m in self.modules.values():
            m.dev = self.dev
        self.sensor.dev = self.dev
        self.dev.set_max_torque(0.03)
        self.dev.move_to_pos(utils.deg2rad(-40), (utils.deg2rad(90) / 3))
        time.sleep(3)
        self.dev.move_to_pos(0.01)



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
            self.sense()# active_layer, temp_active_layer)  # 感覚入力を更新

            # 活性化しているモジュールを取得 (活性化はこの処理で、非活性化はもモジュールごとのv_operatorで行う(非可逆な基準))
            for i in range(len(self.modules)):
                if active_layer[0] >= 0 and i >= active_layer[0]:
                    break  # 自分より下位のレイヤーしか見ない(下位のレイヤーがアクティブになった場合はそちらが優先権を取る)
                temp_key = list(self.modules.keys())[i]
                # self.print_status(19, temp_key + " lookat | " + str(active_layer[0]) + "\n")

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
                    self.modules[temp_active_layer[1]].stopper = True
                self.print_status(10, '\033[30m' + "active module : " + '\033[0m' + active_layer[1] + "\n")

                # print("module start : " + active_layer[1])
                self.modules[active_layer[1]].s = self.sensor_info
                self.modules[active_layer[1]].p = self.physio
                self.modules[active_layer[1]].b = self.belief
                self.modules[active_layer[1]].waiting = True

            if temp_active_layer[0] >= 0:
                # モジュールを終了させる
                if self.modules[active_layer[1]].finished:
                    self.print_status(40, "module kill" + "\n")
                    self.modules[active_layer[1]].finished = False
                    active_layer = [-1, "none"]

                    # @noneになったらとりあえず巣に帰らせる
                    self.dev.set_speed(utils.rpm2rad_per_sec(10))
                    self.dev.move_to_pos(0.0)
                    self.print_status(10, '\033[30m' + "active module : " + '\033[0m' + active_layer[1] + "\n")

            self.physio_sim()  # 生理状態のシミュレーション
            self.show_physio()
            self.print_status(30, str(active_layer) + "\n")
            try:
                self.action_log[active_layer[1]] += 0.05
            except KeyError:
                pass


            try:
                time.sleep(0.05)
            except KeyboardInterrupt:
                self.dev.disable_action()
                self.dev.disconnect()

    def updater(self):
        pass

    def physio_sim(self):
        dt = 0.0001
        for k in self.physio.keys():
            self.physio[k] = self.physio[k] - (max(self.physio[k], 0.0)) * dt * self.p_decay[k]
        if self.is_sound():  # 直近に音がなっていた
            self.physio["obs"] = max(self.physio["obs"] - 5, 0)
        if self.sensor_info["pos"] >= self.border_pos:  # 外にいる間は観察できる
            self.physio["obs"] = 100
            if not self.belief["food"] and self.sensor_info["food"] and self.physio["eat"] - 20 > 0:  # 目の前でスイッチが押されるのを見ると食欲が湧く
                self.physio["eat"] = self.physio["eat"] - 20
            self.belief["food"] = self.sensor_info["food"]


    def sense(self):
        """if temp_active_layer[0] >= 0:
            self.modules[active_layer[1]].s = self.sensor()"""
        temp_sensor = self.sensor.sensor()

        # @自分の動きでセンサーに入力が入っていないように、チェックする
        self.sensor_info["food"] = temp_sensor["food"]
        self.sensor_info["pos"] = temp_sensor["pos"]
        self.sensor_info["pos_log"].append(temp_sensor["pos"])
        self.sensor_info["sound"].append(temp_sensor["sound"])
        self.sensor_info["touch"].append(temp_sensor["touch"])
        self.sensor_info["torque"].append(temp_sensor["torque"])

        # self.sensor_info
        # print("\033[" + str(40) + ";2H\033[2K" + str(self.sensor_info), end="")

    def print_status(self, n, s):
        print("\033["+ str(n) + ";2H\033[2K" + s, end="")
        # print(s)

    def show_physio(self):
        tt = 12
        self.print_status(tt,'\033[30m' + "======desire parameters: " + '\033[0m')
        for k in self.physio.keys():
            tt += 1
            if int(self.physio[k]) <= 30:
                s = '\033[31m' + k + "\t"
            else:
                s = '\033[36m' + k + "\t"
            for i in range(int(self.physio[k])):
                s += "|"
            s += '\033[39m'
            self.print_status(tt, s)
        print("\n")

        temp = {"none": 0, "sleeper": 0, "eater": 0, "player": 0}
        for k in self.action_log.keys():
            temp[k] = int(self.action_log[k])
        print("\033[" + str(20) + ";2H\033[2K" + str(temp), end="")
        print("\033[" + str(21) + ";2H\033[2K" + str(self.belief), end="")

    def is_sound(self):
        if np.var(np.array(self.sensor_info["sound"])) >= 200:
            return True  # 過去の値から、最新の値においておとがなる判定が下るか
        return False






robot = Body()
robot.life()
