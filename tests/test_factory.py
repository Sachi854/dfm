from unittest import TestCase
from aem import AndroidEmuMacro
import dfm.factory as ft


class Test(TestCase):
    def setUp(self) -> None:
        self._aem = AndroidEmuMacro()
        self._aem.connect(device_port=63543)

    def tearDown(self) -> None:
        self._aem.disconnect()

    def test_disassemble_all_char(self):
        ft.disassemble_all_char(self._aem)

    def test_disassemble_auto_char(self):
        ft.disassemble_auto_char(self._aem)

    def test_disassemble_all_equipment(self):
        ft.disassemble_all_equipment(self._aem)

    def test_disassemble_auto_equipment(self):
        ft.disassemble_auto_equipment(self._aem)
