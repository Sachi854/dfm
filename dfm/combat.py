import random

from aem import AndroidEmuMacro
from dfm.tools import here

OVERVIEW_DELAY = 1.0


def select_row(aem: AndroidEmuMacro, pos: int) -> bool:
    pos = abs(pos)
    if pos == 1:
        aem.tap(random.randrange(900, 1600, 1), random.randrange(400, 480, 1))
    elif pos == 2:
        aem.tap(random.randrange(900, 1600, 1), random.randrange(580, 660, 1))
    elif pos == 3:
        aem.tap(random.randrange(900, 1600, 1), random.randrange(760, 820, 1))
    elif pos == 4:
        aem.tap(random.randrange(900, 1600, 1), random.randrange(920, 1000, 1))
    else:
        return False
    aem.sleep(OVERVIEW_DELAY)
    aem.tap(random.randrange(1400, 1600, 1), random.randrange(870, 920, 1))
    aem.sleep(OVERVIEW_DELAY * 6)

    while not aem.is_there_img(here("df_img/c02_apply.png")):
        aem.sleep(OVERVIEW_DELAY * 2)
    return True


# 戦役選択アルゴリズム考えておく
# なんか
# つよいコード
# をコイツラに追加する
def select_n02(aem: AndroidEmuMacro) -> bool:
    return select_row(aem, 2)


def select_m81(aem: AndroidEmuMacro) -> bool:
    return select_row(aem, 1)


def select_e104(aem: AndroidEmuMacro) -> bool:
    return select_row(aem, 4)
