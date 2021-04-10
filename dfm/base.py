from aem import AndroidEmuMacro
from dfm.tools import here
import random

BASE_DELAY = 1.0


def is_here_base(aem: AndroidEmuMacro) -> bool:
    return aem.is_there_img(here("df_img/b_d.png")) and aem.is_there_img(here("df_img/b_cam.png"))


def check_logistic_support(aem: AndroidEmuMacro) -> bool:
    # 後方支援が帰ってるか判定 440 330
    while True:
        aem.tap(random.randrange(430, 440, 1), random.randrange(330, 340, 1))
        aem.sleep(BASE_DELAY / 8)
        aem.tap(random.randrange(430, 440, 1), random.randrange(330, 340, 1))
        aem.sleep(BASE_DELAY / 4)
        if not aem.match(here("df_img/b_cbt.png"))[0]:
            aem.tap_img(here("df_img/b_ls_apply.png"))
        else:
            break


def mv_to_factory(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img(here("df_img/b_ft.png")):
        while True:
            aem.sleep(BASE_DELAY * 5)
            if aem.is_there_img(here("df_img/ov.png")) or aem.is_there_img(here("df_img/ov_enable.png")):
                return True
    return False


def mv_to_combat(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img(here("df_img/b_cbt.png")):
        while True:
            aem.sleep(BASE_DELAY * 5)
            if aem.is_there_img(here("df_img/ov.png")) or aem.is_there_img(here("df_img/ov_enable.png")):
                return True
    return False


def mv_to_echelon(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img(here("df_img/b_ef.png")):
        while True:
            aem.sleep(BASE_DELAY * 5)
            if aem.is_there_img(here("df_img/ov.png")) or aem.is_there_img(here("df_img/ov_enable.png")):
                return True
    return False
