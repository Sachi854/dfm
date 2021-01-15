from unittest import TestCase
from aem import AndroidEmuMacro
import dfm.overview as ov


class Test(TestCase):
    def setUp(self) -> None:
        self._aem = AndroidEmuMacro()
        self._aem.connect()

    def tearDown(self) -> None:
        self._aem.disconnect()

    def test_is_overview_available(self):
        self.assertTrue(ov.is_overview_available(self._aem))

    def test_open_overview(self):
        self.assertTrue(ov.open_overview(self._aem))

    def test_mv_to_base(self):
        self.assertTrue(ov.mv_to_base(self._aem))

    def test_mv_to_factory(self):
        self.assertTrue(ov.mv_to_factory(self._aem))

    def test_mv_to_xxx(self):
        self.assertTrue(ov.mv_to_combat(self._aem))
        self.assertTrue(ov.mv_to_echelon(self._aem))
        self.assertTrue(ov.mv_to_factory(self._aem))
        self.assertTrue(ov.mv_to_develop(self._aem))
        self.assertTrue(ov.mv_to_cic(self._aem))
        self.assertTrue(ov.mv_to_base(self._aem))
