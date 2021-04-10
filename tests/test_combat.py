from unittest import TestCase
from aem import AndroidEmuMacro
import dfm.combat as cb


class Test(TestCase):
    def setUp(self) -> None:
        self._aem = AndroidEmuMacro()
        self._aem.connect(device_port=63543)

    def tearDown(self) -> None:
        self._aem.disconnect()

    def test_select_row(self):
        self.fail()

    def test_select_n02(self):
        cb.select_n02(aem=self._aem)

    def test_select_m81(self):
        cb.select_m81(aem=self._aem)

    def test_select_e104(self):
        cb.select_e104(aem=self._aem)
