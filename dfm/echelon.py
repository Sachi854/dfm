import random

from aem import AndroidEmuMacro
from dfm.tools import here

OVERVIEW_DELAY = 1.0


def __is_here_ef(aem: AndroidEmuMacro) -> bool:
    return aem.is_there_img(here("df_img/ef_f.png"))


def __is_here_form(aem: AndroidEmuMacro) -> bool:
    return aem.is_there_img(here("df_img/f_fc.png"))


def __is_here_cfm(aem: AndroidEmuMacro) -> bool:
    return aem.is_there_img(here("df_img/ef1.png"))


def __go_ef2form(aem: AndroidEmuMacro) -> bool:
    flg = aem.tap_img(here("df_img/ef_f.png"))
    aem.sleep(OVERVIEW_DELAY)
    if flg:
        while not __is_here_form(aem):
            aem.sleep(OVERVIEW_DELAY)
    return flg


def __go_form2cfm(aem: AndroidEmuMacro) -> bool:
    flg = aem.tap_img(here("df_img/f_fc.png"))
    aem.sleep(OVERVIEW_DELAY)
    if flg:
        while not __is_here_cfm(aem):
            aem.sleep(OVERVIEW_DELAY)
    return flg


def __go_form2ef(aem: AndroidEmuMacro) -> bool:
    flg = aem.tap_img(here("df_img/f_apply.png"))
    aem.sleep(OVERVIEW_DELAY)
    if flg:
        while not __is_here_ef(aem):
            aem.sleep(OVERVIEW_DELAY)
    return flg


# 手を抜いたから必要に応じて部隊の設定を追加すること
def __get_pos(aem: AndroidEmuMacro, e: int) -> list:
    e = abs(e)
    if e == 1:
        flg, pos = aem.match(here("df_img/e1_active_fix.png"))
        if flg:
            return pos
        flg, pos = aem.match(here("df_img/e1_fix.png"))
        if flg:
            return pos
    elif e == 2:
        flg, pos = aem.match(here("df_img/e2_active_fix.png"))
        if flg:
            return pos
        flg, pos = aem.match(here("df_img/e2_fix.png"))
        if flg:
            return pos
    return None


def __get_fig_pos(aem: AndroidEmuMacro, f: int):
    f = abs(f)
    return [304 + 277 * (f - 1), 424]


def select(aem: AndroidEmuMacro, echelon: int) -> bool:
    echelon = abs(echelon)
    if echelon <= 2:
        if echelon == 1:
            aem.tap_img(here("df_img/e1_fix.png"))
        elif echelon == 2:
            aem.tap_img(here("df_img/e2_fix.png"))
        aem.sleep(OVERVIEW_DELAY)
        while not __is_here_ef(aem):
            aem.sleep(OVERVIEW_DELAY)
        return True
    return False


# めんどいので手抜きしてる
def swap(aem: AndroidEmuMacro, echelon1: int, echelon2: int) -> bool:
    flg = select(aem, echelon1)
    if flg:
        t = abs(echelon1) + abs(echelon2)
        echelon1 = __get_pos(aem, abs(echelon1))
        echelon2 = __get_pos(aem, abs(echelon2))
        if None not in [echelon1, echelon2]:
            aem.swipe(int(echelon1[0]), int(echelon1[1]), int(echelon2[0]), int(echelon2[1]), 1000 * t)
            aem.sleep(t + OVERVIEW_DELAY / 2)
            aem.tap_img(here("df_img/e_apply.png"))
            aem.sleep(OVERVIEW_DELAY / 2)
            return not aem.is_there_img(here("df_img/e_apply.png"))
    return False


# 絶対座標で指定してあるので暇なら相対座標に対応させる
def swap_figurine(aem: AndroidEmuMacro, figurine1: int, figurine2: int):
    if max([abs(figurine1), abs(figurine2)]) <= 5 and figurine1 != figurine2:
        t = abs(figurine1) + abs(figurine2)
        figurine1 = __get_fig_pos(aem, figurine1)
        figurine2 = __get_fig_pos(aem, figurine2)
        aem.swipe(figurine1[0], figurine1[1], figurine2[0], figurine2[1], 1000 * t)
        aem.sleep(OVERVIEW_DELAY / 2)
        return True
    return False


def load_formation(aem: AndroidEmuMacro, formation_num: int) -> bool:
    formation_num = abs(formation_num)
    if formation_num <= 2:
        __go_ef2form(aem)
        __go_form2cfm(aem)

        # 陣形編集
        if formation_num == 1 and aem.tap_img(here("df_img/ef1.png")):
            pass
        elif formation_num == 2 and aem.tap_img(here("df_img/ef2.png")):
            pass
        aem.sleep(OVERVIEW_DELAY)
        result = aem.tap_img(here("df_img/fc_apply.png"))
        aem.sleep(OVERVIEW_DELAY)
        if aem.tap_img(here("df_img/fc_x.png")) or aem.is_there_img(here("df_img/fc_v.png")):
            aem.sleep(OVERVIEW_DELAY)
            aem.tap_img(here("df_img/fc_x_apply.png"))
            aem.sleep(OVERVIEW_DELAY)
        while not __is_here_form(aem):
            aem.sleep(OVERVIEW_DELAY)

        # 部隊編集へ
        __go_form2ef(aem)

        return result
    return False
