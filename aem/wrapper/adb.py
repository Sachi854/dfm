import subprocess


class AdbWrapper:
    def __init__(self, adb_path="adb.exe"):
        self.__adb_path = adb_path
        self.__device_serial = ""

    def restart(self) -> None:
        subprocess.check_output([self.__adb_path, "kill-server"])
        subprocess.check_output([self.__adb_path, "start-server"])

    def connect(self, device_ip_address="localhost", device_port=5555) -> None:
        subprocess.check_output([self.__adb_path, "connect", (device_ip_address + ":" + str(device_port))])
        self.__device_serial = self.get_serials()[0]

    def disconnect(self, device_ip_address="localhost", device_port=5555) -> None:
        subprocess.check_output([self.__adb_path, "disconnect", (device_ip_address + ":" + str(device_port))])

    def get_serials(self) -> list:
        result = []
        adb_result = subprocess.check_output([self.__adb_path, "devices"])
        for i, elem in enumerate(adb_result.decode().splitlines()):
            if elem == "" or i == 0:
                continue

            result.append(elem.split()[0])

        return result

    def tap(self, x: int, y: int) -> None:
        subprocess.check_output(
            [self.__adb_path, "-s", self.__device_serial, "shell", "input", "touchscreen", "tap", str(x), str(y)])

    def long_tap(self, x: int, y: int, m_sec=500) -> None:
        self.swipe(x, y, x, y, m_sec)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, m_sec=500) -> None:
        subprocess.check_output(
            [self.__adb_path, "-s", self.__device_serial, "shell", "input", "touchscreen", "swipe", str(x1), str(y1),
             str(x2),
             str(y2), str(m_sec)])

    def screenshot(self, save_dir="./", file_name="screenshot.png") -> None:
        subprocess.check_output(
            [self.__adb_path, "-s", self.__device_serial, "shell", "screencap", "-p", "/sdcard/" + file_name])

        subprocess.check_output(
            [self.__adb_path, "-s", self.__device_serial, "pull", ("/sdcard/" + file_name), save_dir])

        subprocess.check_output(
            [self.__adb_path, "-s", self.__device_serial, "shell", "rm", ("/sdcard/" + file_name)])


# debug
if __name__ == '__main__':
    aw = AdbWrapper()
