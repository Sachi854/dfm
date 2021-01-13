from unittest import TestCase
import aem


class TestAndroidEmuMacro(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._aem = aem.AndroidEmuMacro()
        cls._aem.connect()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._aem.disconnect()

    @classmethod
    def test_screenshot(cls):
        cls._aem.screenshot()
