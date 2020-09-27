import time
from collections import OrderedDict


class Body:
    def __init__(self):
        self.physio = dict({"eat": 0, "sleep": 0, "interact": 0, "stamina": 0})
        self.modules = {"eater": Eat(), "sleeper": Sleep(), "interacter": Interact()}  # [0]が一番優先度高い
        print("active modules")
        for i in range(len(self.modules)):
            print(list(self.modules.keys())[i])
        print("\n\nit got birth\n\n")

    def runner(self):

        while True:
            active_layer = [-1, "none"]

            # 活性化しているモジュールを取得
            for i in range(len(self.modules)):
                temp_key = list(self.modules.keys())[i]
                print([temp_key, self.modules[temp_key].is_active(self.physio)])
                if self.modules[temp_key].is_active(self.physio):
                    active_layer = [i, temp_key]
                    break

            #モジュールを走らせる
            self.modules[active_layer[1]].v_operator(self.physio)

            # モジュールを更新
            # self.modules.items()[active_layer].learner()

            time.sleep(0.5)

    def updater(self):
        pass


class Eat:
    def __init__(self):
        self.param = dict({"mov1": 0})

    def is_active(self, physio):
        return True

    def v_operator(self, physio):
        pass

    def learner(self):
        pass


class Sleep:
    def __init__(self):
        self.param = dict({"test": 0})

    def is_active(self):
        pass

    def v_operator(self):
        pass

    def learner(self):
        pass


class Interact:
    def __init__(self):
        self.param = dict({"test": 0})

    def is_active(self):
        pass

    def v_operator(self):
        pass

    def learner(self):
        pass


robot = Body()
robot.runner()
