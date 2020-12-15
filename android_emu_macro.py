from adb_wrapper import AdbWrapper
from object_detection import ObjectDetection

import os
import time
import numpy as np


class AndroidEmuMacro:
    def __init__(self, adb_path="adb.exe", save_img_path="./imgs"):
        self.__od = ObjectDetection()
        self.__aw = AdbWrapper(adb_path)
        self.__device_address = None
        self.__device_port = None
        self.__save_img_path = save_img_path
        os.makedirs(self.__save_img_path, exist_ok=True)

    def connect(self, device_address="localhost", device_port=5555) -> None:
        self.__device_address = device_address
        self.__device_port = device_port
        self.__aw.connect(self.__device_address, self.__device_port)

    def disconnect(self) -> None:
        self.__aw.disconnect(self.__device_address, self.__device_port)

    def restart(self) -> None:
        self.__aw.restart()

    # 特徴量でマッチング
    def __match_feature(self, train_img_path: str):
        self.screenshot(0)
        obj = self.__od.__match_img_akaze(self.__save_img_path + "/screenshot0.png", train_img_path)
        return obj

    # テンプレートマッチング
    def __match_template(self, train_img_path: str):
        self.screenshot(0)
        obj = []
        return obj

    # このメソッドをテンプレートマッチングと, 特徴量検知で分ける
    def get_img_coordinate(self, train_img_path: str, threshold=4, sample_num=20) -> list or None:
        result = None
        mr = self.__match_feature(train_img_path)[:sample_num]

        # 高精度でマッチングした点が4以上であれば処理をする
        if len(mr) >= threshold:
            r_std = np.std(np.array(mr), axis=0)
            r_average = np.average(np.array(mr), axis=0)

            # 標準偏差以上に差がある座標を削除
            result = list(
                filter(lambda x: np.abs(r_average[0] - x[0]) < r_std[0] and np.abs(r_average[1] - x[1]) < r_std[1], mr))

            return np.average(np.array(result), axis=0)
        else:
            return result

    def is_there_img(self, train_img_path: str, threshold=4, sample_num=20) -> bool:
        return not (self.get_img_coordinate(train_img_path, threshold, sample_num) is None)

    # 精度あやしい
    def tap_img(self, train_img_path: str, threshold=4, sample_num=20) -> bool:
        coordinate = self.get_img_coordinate(train_img_path, threshold, sample_num)
        if coordinate is None:
            return False
        else:
            self.tap(int(coordinate[0]), int(coordinate[1]))
            return True

    def tap(self, x: int, y: int) -> None:
        self.__aw.tap(x, y)

    def long_tap_img(self, train_img_path: str, m_sec=500, threshold=4, sample_num=20) -> bool:
        coordinate = self.get_img_coordinate(train_img_path, threshold, sample_num)
        if coordinate is None:
            return False
        else:
            self.long_tap(int(coordinate[0]), int(coordinate[1]), m_sec)
            return True

    def long_tap(self, x: int, y: int, m_sec=500) -> None:
        self.__aw.long_tap(x, y, m_sec)

    def swipe_img(self, train_img_path: str, x2: int, y2: int, m_sec=500, threshold=4, sample_num=20) -> bool:
        coordinate = self.get_img_coordinate(train_img_path, threshold, sample_num)
        if coordinate is None:
            return False
        else:
            self.swipe(int(coordinate[0]), int(coordinate[1]), x2, y2, m_sec)
            return True

    def swipe(self, x1: int, y1: int, x2: int, y2: int, m_sec=500) -> None:
        self.__aw.swipe(x1, y1, x2, y2, m_sec)

    @staticmethod
    def sleep(sec: float) -> None:
        time.sleep(sec)

    @staticmethod
    def sleep_ms(m_sec: float) -> None:
        time.sleep(m_sec / 1000.0)

    def screenshot(self, offset=1) -> None:
        while os.path.isfile(self.__save_img_path + "/screenshot" + str(offset) + ".png") and (offset != 0):
            offset = offset + 1

        self.__aw.screenshot(self.__save_img_path, "/screenshot" + str(offset) + ".png")


# add df test
# 特徴抽出は使える場合と死ぬ場合が極端だからパターンマッチングも実装しとく
if __name__ == '__main__':
    aem = AndroidEmuMacro()
    aem.connect()

    # macro
    aem.tap_img("df/sento.png")
    aem.sleep_ms(5000)

    aem.tap_img("df/mogi.png")
    aem.sleep_ms(5000)

    aem.tap_img("df/mogi_t.png")
    aem.sleep_ms(5000)

    c = aem.get_img_coordinate("df/mogi_ct_y_900.png")
    if c is None:
        print("ken ti de kizu")
        exit()
    aem.tap(c[0], 900)
    aem.sleep_ms(5000)

    aem.tap_img("df/tyosen.png")
    aem.save_recognition_range("img/d5.png")
    aem.sleep(10)

    # aem.tap_img("df/modoru.png")
    aem.tap_img("df/modoru.png")
    aem.sleep_ms(5000)

    aem.tap_img("df/modoru_2.png")
    aem.sleep_ms(5000)
    # end macro

    aem.disconnect()
