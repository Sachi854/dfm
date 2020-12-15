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

    # エラー処理が必要
    def connect(self, device_address="localhost", device_port=5555) -> None:
        self.__device_address = device_address
        self.__device_port = device_port
        self.__aw.connect(self.__device_address, self.__device_port)

    # エラー処理が必要
    def disconnect(self) -> None:
        self.__aw.disconnect(self.__device_address, self.__device_port)

    def restart(self) -> None:
        self.__aw.restart()

    # 全引数を有効にすべきかそうでないか
    # 特徴量でマッチング
    def match_feature(self, train_img_path: str, threshold=4, sample_num=20, ratio=0.5, save_img=False) -> list:
        self.screenshot(0)
        return self.__od.match_img_feature(self.__save_img_path + "/screenshot0.png", train_img_path,
                                           threshold, sample_num, ratio, [save_img, self.__save_img_path + "/mf.png"])

    # テンプレートマッチング
    def match_template(self, train_img_path: str, threshold=0.8, save_img=False) -> list:
        self.screenshot(0)
        return self.__od.match_img_template(self.__save_img_path + "/screenshot0.png", train_img_path,
                                            threshold, [save_img, self.__save_img_path + "/mt.png"])

    # mode 0 : template and feature
    # mode 1 : template only
    # mode 2 : feature only
    def is_there_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
        flag = False
        if mode in {0, 1}:
            flag = flag or self.match_template(train_img_path, save_img=save_img)[0]
        if mode in {0, 2}:
            flag = flag or self.match_feature(train_img_path, save_img=save_img)[0]
        return flag

    # mode 0 : template and feature
    # mode 1 : template only
    # mode 2 : feature only
    def tap_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
        if mode in {0, 1}:
            flag, pos = self.match_template(train_img_path, save_img=save_img)
            if flag:
                self.tap(pos[0], pos[1])
                return flag
        if mode in {0, 2}:
            flag, pos = self.match_feature(train_img_path, save_img=save_img)
            if flag:
                self.tap(pos[0], pos[1])
                return flag
        return False

    # mode 0 : template and feature
    # mode 1 : template only
    # mode 2 : feature only
    def long_tap_img(self, train_img_path: str, m_sec=500, mode=0, save_img=False) -> bool:
        if mode in {0, 1}:
            flag, pos = self.match_template(train_img_path, save_img=save_img)
            if flag:
                self.long_tap(pos[0], pos[1], m_sec)
                return flag
        if mode in {0, 2}:
            flag, pos = self.match_feature(train_img_path, save_img=save_img)
            if flag:
                self.long_tap(pos[0], pos[1], m_sec)
                return flag
        return False

    # mode 0 : template and feature
    # mode 1 : template only
    # mode 2 : feature only
    def swipe_img(self, train_img_path: str, x2: int, y2: int, m_sec=500, mode=0, save_img=False) -> bool:
        if mode in {0, 1}:
            flag, pos = self.match_template(train_img_path, save_img=save_img)
            if flag:
                self.swipe(pos[0], pos[1], x2, y2, m_sec)
                return flag
        if mode in {0, 2}:
            flag, pos = self.match_feature(train_img_path, save_img=save_img)
            if flag:
                self.swipe(pos[0], pos[1], x2, y2, m_sec)
                return flag
        return False

    def tap(self, x: int, y: int) -> None:
        self.__aw.tap(x, y)

    def long_tap(self, x: int, y: int, m_sec=500) -> None:
        self.__aw.long_tap(x, y, m_sec)

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

    # 遠征後, クリック回数2 (1111,745->でうまくっぽい)

    # macro
    aem.screenshot()
    #print(aem.is_there_img("img/screenshot3.png"))
    # end macro
    aem.disconnect()
