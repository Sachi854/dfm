from unittest import TestCase
from aem import AndroidEmuMacro
import dfm.base as bs


class Test(TestCase):
    def setUp(self) -> None:
        self._aem = AndroidEmuMacro()
        self._aem.connect(device_port=63543)

    def tearDown(self) -> None:
        self._aem.disconnect()

    # debug ha 30min go
    def test_check_logistic_support(self):
        bs.check_logistic_support(self._aem)

    def test_is_here_base(self):
        self.assertTrue((bs.is_here_base(self._aem)))

    def test_enter_factory(self):
        self.assertTrue((bs.mv_to_echelon(self._aem)))
