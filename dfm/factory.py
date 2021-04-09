import random

from aem import AndroidEmuMacro
from dfm.tools import here

OVERVIEW_DELAY = 1.0


def __is_here_retire(aem: AndroidEmuMacro) -> bool:
    return aem.is_there_img(here("df_img/da_.png"))


def __go_ft2retire(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img(here("df_img/ft_da.png")):
        while True:
            aem.sleep(OVERVIEW_DELAY)
            if __is_here_retire(aem):
                return True
    return False


def __enter_select_char(aem: AndroidEmuMacro) -> bool:
    aem.tap_img(here("df_img/da_select_char.png"))
    aem.sleep(OVERVIEW_DELAY * 2)
    if __is_here_retire(aem):
        return False
    return True


def __enter_select_eq(aem: AndroidEmuMacro) -> bool:
    aem.tap_img(here("df_img/da_select_eq.png"))
    aem.sleep(OVERVIEW_DELAY * 2)
    if __is_here_retire(aem):
        return False
    return True


def __select_6_char(aem: AndroidEmuMacro) -> bool:
    aem.tap(random.randrange(80, 230, 1), random.randrange(230, 460, 1))
    aem.sleep(OVERVIEW_DELAY)
    aem.tap(random.randrange(350, 500, 1), random.randrange(230, 460, 1))
    aem.sleep(OVERVIEW_DELAY)
    aem.tap(random.randrange(600, 750, 1), random.randrange(230, 460, 1))
    aem.sleep(OVERVIEW_DELAY)
    aem.tap(random.randrange(850, 1000, 1), random.randrange(230, 460, 1))
    aem.sleep(OVERVIEW_DELAY)
    aem.tap(random.randrange(1130, 1280, 1), random.randrange(230, 460, 1))
    aem.sleep(OVERVIEW_DELAY)
    aem.tap(random.randrange(1400, 1550, 1), random.randrange(230, 460, 1))
    aem.sleep(OVERVIEW_DELAY)
    flg = aem.tap_img(here("df_img/sc_apply.png"))
    aem.sleep(OVERVIEW_DELAY)
    return flg


def __select_auto(aem: AndroidEmuMacro) -> bool:
    aem.tap_img(here("df_img/sc_auto.png"))
    aem.sleep(OVERVIEW_DELAY)
    flg = aem.tap_img(here("df_img/sc_apply.png"))
    aem.sleep(OVERVIEW_DELAY)
    return flg


def __disassemble(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img(here("df_img/da_apply.png")):
        aem.sleep(OVERVIEW_DELAY)
        while aem.tap_img(here("df_img/da_e_apply.png")):
            aem.sleep(OVERVIEW_DELAY)
        return True
    return False


def disassemble_all_char(aem: AndroidEmuMacro) -> bool:
    __go_ft2retire(aem)
    while __enter_select_char(aem):
        if not __select_6_char(aem):
            break
        __disassemble(aem)
    return True


def disassemble_auto_char(aem: AndroidEmuMacro) -> bool:
    __go_ft2retire(aem)
    while __enter_select_char(aem):
        if not __select_auto(aem):
            break
        __disassemble(aem)
    return True


def disassemble_all_equipment(aem: AndroidEmuMacro) -> bool:
    __go_ft2retire(aem)
    while __enter_select_eq(aem):
        if not __select_6_char(aem):
            break
        __disassemble(aem)
    return True


def disassemble_auto_equipment(aem: AndroidEmuMacro) -> bool:
    __go_ft2retire(aem)
    while __enter_select_eq(aem):
        if not __select_auto(aem):
            break
        __disassemble(aem)
    return True
