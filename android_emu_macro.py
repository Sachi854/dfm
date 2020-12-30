from adb_wrapper import AdbWrapper
from object_detection import ObjectDetection

import os
import time


class AndroidEmuMacro:
    def __init__(self, adb_path="adb.exe", save_img_path="./imgs"):
        """
        Constructor.

        Parameters:
        ----------
        adb_path : str
            Path of adb.
        save_img_path : str
            Path of save img.
        """
        self.__od = ObjectDetection()
        self.__aw = AdbWrapper(adb_path)
        self.__device_address = None
        self.__device_port = None
        self.__save_img_path = save_img_path
        os.makedirs(self.__save_img_path, exist_ok=True)

    # エラー処理が必要
    def connect(self, device_address="localhost", device_port=5555) -> None:
        """
        Connect adb server of emulator.

        Parameters:
        ----------
        device_address : str
            IP address that can be checked in the settings of emulator.
        device_port : str
            Port that can be checked in the settings of emulator.
        """
        self.__device_address = device_address
        self.__device_port = device_port
        self.__aw.connect(self.__device_address, self.__device_port)

    # エラー処理が必要
    def disconnect(self) -> None:
        """
        Disconnect adb server of emulator.
        """
        self.__aw.disconnect(self.__device_address, self.__device_port)

    def restart(self) -> None:
        """
        Restart adb server
        """
        self.__aw.restart()

    # 特徴量でマッチング
    def match_feature(self, train_img_path: str, threshold=4, sample_num=20, ratio=0.5, save_img=False) -> list:
        """
        Returns the coordinates of the image match.
        Algorithm is object detection.
        Match for slightly obscure images.

        Parameters:
        ----------
        train_img_path : str
            Path of input image.
        threshold : int
            Minimum number of matches.
        sample_num : int
            Number of use mathe sample.
        ratio : float
            Parameter of ration test.
        save_img : bool
            Save match img diff flag.

        Returns:
        ----------
        list
            [is_match: Bool, [x: int, y: int]]
        """
        self.screenshot(0)
        return self.__od.match_img_feature(self.__save_img_path + "/screenshot0.png", train_img_path,
                                           threshold, sample_num, ratio, [save_img, self.__save_img_path + "/mf.png"])

    # テンプレートマッチング
    def match_template(self, train_img_path: str, threshold=0.8, save_img=False) -> list:
        """
        Returns the coordinates of the image match.
        Algorithm is template matching.
        Match for per-pixel.

        Parameters:
        ----------
        train_img_path : str
            Path of input image.
        threshold : float
            Accuracy of match for per-pixel.
        save_img : bool
            Save match img diff flag.

        Returns:
        ----------
        list
            [is_match: Bool, [x: int, y: int]]
        """
        self.screenshot(0)
        return self.__od.match_img_template(self.__save_img_path + "/screenshot0.png", train_img_path,
                                            threshold, [save_img, self.__save_img_path + "/mt.png"])

    # テンプレートマッチングを優先でマッチングその後特徴量でマッチング
    def match(self, train_img_path: str, save_img=False) -> list:
        """
        Returns the coordinates of the image match.
        Match for template or feature.

        Parameters:
        ----------
        train_img_path : str
            Path of input image.
        save_img : bool
            Save match img diff flag.

        Returns:
        ----------
        list
            [is_match: Bool, [x: int, y: int]]
        """
        result = self.match_template(train_img_path, save_img=save_img)
        if result[0]:
            return result
        else:
            return self.match_feature(train_img_path, save_img=save_img)

    # mode 0 : template and feature
    # mode 1 : template only
    # mode 2 : feature only
    def is_there_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
        """
        Judge is there this image.

        Parameters:
        ----------
        train_img_path : str
            Path of input image.
        mode : int
            0 -> Template and feature, 1 -> Template only,2 -> Feature only
        save_img : bool
            Save match img diff flag.

        Returns:
        ----------
        bool
        """
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
        """
        Tap input image.

        Parameters:
        ----------
        train_img_path : str
            Path of input image.
        mode : int
            0 -> Template and feature, 1 -> template only,2 -> feature only
        save_img : bool
            Save match img diff flag.

        Returns:
        ----------
        bool
        """
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
        """
        Long tap input image.

        Parameters:
        ----------
        train_img_path : str
            Path of input image.
        mode : int
            0 -> Template and feature, 1 -> template only,2 -> feature only
        save_img : bool
            Save match img diff flag.

        Returns:
        ----------
        bool
        """
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
        """
        Swipe input image.

        Parameters:
        ----------
        train_img_path : int
            Path of input image.
        x2 : int
            target coordinate of x.
        y2 : int
            target coordinate of y.
        m_sec : int
            Time of start between end.
        mode : int
            0 -> Template and feature, 1 -> Template only,2 -> Feature only
        save_img : bool
            Save match img diff flag.

        Returns:
        ----------
        bool
        """
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
        """
        Tap input coordinates.

        Parameters:
        ----------
        x : int
            target coordinate of x.
        y : int
            target coordinate of y.
        save_img : str
            Save match img diff flag.
        """
        self.__aw.tap(x, y)

    def long_tap(self, x: int, y: int, m_sec=500) -> None:
        """
        Long tap input coordinates.

        Parameters:
        ----------
        x : int
            target coordinate of x.
        y : int
            target coordinate of y.
        save_img : str
            Save match img diff flag.
        """
        self.__aw.long_tap(x, y, m_sec)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, m_sec=500) -> None:
        """
        Swipe input coordinates to target coordinates.

        Parameters:
        ----------
        x1 : int
            Current coordinate of x.
        y1 : int
            Current coordinate of y.
        x2 : int
            target coordinate of x.
        y2 : int
            target coordinate of y.
        m_sec : int
            Time of start between end.
        """
        self.__aw.swipe(x1, y1, x2, y2, m_sec)

    @staticmethod
    def sleep(sec: float) -> None:
        """
        Sleep sec.

        Parameters:
        ----------
        sec : float
            sec.
        """
        time.sleep(sec)

    @staticmethod
    def sleep_ms(m_sec: float) -> None:
        """
        Sleep micro sec.

        Parameters:
        ----------
        m_sec : float
            micro sec.
        """
        time.sleep(m_sec / 1000.0)

    def screenshot(self, offset=1) -> None:
        """
        Take screen shot.

        Parameters:
        ----------
        offset : int
            Number of saving
        """
        while os.path.isfile(self.__save_img_path + "/screenshot" + str(offset) + ".png") and (offset != 0):
            offset = offset + 1
        self.__aw.screenshot(self.__save_img_path, "/screenshot" + str(offset) + ".png")


if __name__ == '__main__':
    aem = AndroidEmuMacro()
    aem.connect()
    # スクショとるコード
    aem.screenshot()
    aem.disconnect()
