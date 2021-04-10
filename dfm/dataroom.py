import random

from aem import AndroidEmuMacro
from dfm.tools import here

OVERVIEW_DELAY = 1.0


def make_fd(aem: AndroidEmuMacro) -> bool:
    result = False
    if aem.tap_img(here("df_img/dr_dk.png")):
        aem.sleep(OVERVIEW_DELAY)
        aem.tap_img(here("df_img/dr_dk_start.png"))
        aem.sleep(OVERVIEW_DELAY)
        if aem.tap_img(here("df_img/dr_dk_apply.png")):
            result = True
            if aem.is_there_img(here("df_img/dr_dk_apply.png")):
                aem.sleep(OVERVIEW_DELAY)
                aem.tap_img(here("df_img/dr_dk_cancel.png"))
                result = False

        if not result:
            aem.sleep(OVERVIEW_DELAY)
            aem.tap_img(here("df_img/dr_dk_bk.png"))

    aem.sleep(OVERVIEW_DELAY)
    return result
