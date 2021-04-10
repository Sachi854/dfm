from unittest import TestCase
from aem import AndroidEmuMacro
import dfm.dataroom as dr


class Test(TestCase):
    def setUp(self) -> None:
        self._aem = AndroidEmuMacro()
        self._aem.connect(device_port=63543)

    def tearDown(self) -> None:
        self._aem.disconnect()

    def test_make_fd(self):
        dr.make_fd(aem=self._aem)
