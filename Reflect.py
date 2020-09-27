import time
from collections import OrderedDict
import math
import time
import random
import sys
import os
from Modules import Module


class Reflect(Module):
    def __init__(self):
        super().__init__()
        self.param = {}

    def is_active(self, physio):  # pとsで決まるようにする
        if random.random() <= 0.001 or self.ref_sound() or self.ref_touch() or self.ref_torque():
            return True
        else:
            return False

    def ref_touch(self):  # 強いものが来ると反応
        return False

    def ref_torque(self):  # 強いものが来ると反応
        return False

    def ref_sound(self):
        # deque内の累計値で、sleepの深さによって反応性が違うようにする
        return False

    def fight_flight(self):
        if self.p["eat"] + self.p["sleep"] <= 60 and self.s["pos"] <= 40:  # 自分の位置も視野に入れる(間違えてライトをつけないように)
            return "fight"
        else:
            return "flight"

    def v_operator(self):
        print("reflection started")
        if self.fight_flight() == "fight":
            time.sleep(1)
            # @暴れる
        else:
            time.sleep(1)
            # @逃げる

        print("finished")
        self.finisher()