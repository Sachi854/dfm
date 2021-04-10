from unittest import TestCase
from aem import AndroidEmuMacro
import dfm.echelon as ec


class Test(TestCase):
    def setUp(self) -> None:
        self._aem = AndroidEmuMacro()
        self._aem.connect(device_port=63543)

    def tearDown(self) -> None:
        self._aem.disconnect()

    def test_select(self):
        ec.select(aem=self._aem, echelon=2)
        ec.select(aem=self._aem, echelon=1)

    def test_select_figurine(self):
        self.assertTrue(ec.swap_figurine(aem=self._aem, figurine1=1, figurine2=5))

    def test_swap(self):
        self.assertTrue(ec.swap(aem=self._aem, echelon1=2, echelon2=2))

    def test_load_formation(self):
        ec.load_formation(aem=self._aem, formation_num=2)
