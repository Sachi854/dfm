from unittest import TestCase
from aem import AndroidEmuMacro


class TestAndroidEmuMacro(TestCase):
    def setUp(self) -> None:
        self._aem = AndroidEmuMacro()
        self._aem.connect()

    def tearDown(self) -> None:
        self._aem.disconnect()

    def test_screenshot(self):
        self._aem.screenshot()
