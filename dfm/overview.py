from aem import AndroidEmuMacro
from dfm.tools import here

OVERVIEW_DELAY = 1.0
X_LEFT = 200
X_RIGHT = 1700
Y = 350


def is_overview_available(aem: AndroidEmuMacro) -> bool:
    # ベースにいるか？
    if aem.is_there_img(here("df_img/b_st.png")):
        return False
    # ベースではないならovがあるか？
    return aem.is_there_img(here("df_img/ov.png")) or aem.is_there_img(here("df_img/ov_enable.png"))


def open_overview(aem: AndroidEmuMacro) -> bool:
    if is_overview_available(aem):
        # ovがすでに開かれているか？
        if aem.is_there_img(here("df_img/ov_wt.png")):
            return True

        # ovを開く
        if aem.tap_img(here("df_img/ov.png")):
            while True:
                aem.sleep(OVERVIEW_DELAY)
                # ランドマークを確認したら開かれていることにする
                if aem.is_there_img(here("df_img/ov_base.png")):
                    return True

    return False


def _swipe_wt(aem: AndroidEmuMacro, x: int, y: int):
    aem.swipe_img(here("df_img/ov_wt.png"), x, y)
    aem.sleep(OVERVIEW_DELAY)


def mv_to_base(aem: AndroidEmuMacro) -> bool:
    if open_overview(aem):
        # ret baseをタップ
        if aem.tap_img(here("df_img/ov_base.png")):
            # ロード中の待機
            while True:
                aem.sleep(OVERVIEW_DELAY * 4)
                # 戦闘か後方支援が帰ってるならそこはベースだ
                if aem.is_there_img(here("df_img/b_cbt.png")) or aem.is_there_img(here("df_img/b_ls.png")):
                    return True
    # そもそもベースにいるならTを返す
    return aem.is_there_img(here("df_img/b_st.png"))


def _mv_to_xx(aem: AndroidEmuMacro, img_path: str) -> bool:
    if aem.tap_img(img_path):
        # ロード待機
        while True:
            aem.sleep(OVERVIEW_DELAY * 4)
            # ovが消えている and ov呼び出し可なら正常終了
            if (not aem.is_there_img(here("df_img/ov_base.png"), mode=1)) and is_overview_available(aem):
                return True
            # そもそも目的地にいるならovを閉じる
            elif aem.is_there_img(here("df_img/ov_base.png")):
                aem.tap_img(here("df_img/ov_enable.png"))
    return False


def mv_to_combat(aem: AndroidEmuMacro) -> bool:
    # ov開く
    if open_overview(aem):
        # 工廠の項目がないならずらず
        while not aem.is_there_img(here("df_img/ov_cbt.png")):
            _swipe_wt(aem, X_RIGHT, Y)

        # 画像指定で移動させる
        return _mv_to_xx(aem, here("df_img/ov_cbt.png"))
    return False


def mv_to_echelon(aem: AndroidEmuMacro) -> bool:
    # ov開く
    if open_overview(aem):
        # 工廠の項目がないならずらず
        while not aem.is_there_img(here("df_img/ov_ef.png")):
            _swipe_wt(aem, X_RIGHT, Y)

        # 画像指定で移動させる
        return _mv_to_xx(aem, here("df_img/ov_ef.png"))
    return False


def mv_to_factory(aem: AndroidEmuMacro) -> bool:
    # ov開く
    if open_overview(aem):
        # 工廠の項目がないならずらず
        while not aem.is_there_img(here("df_img/ov_ft.png")):
            _swipe_wt(aem, X_RIGHT, Y)

        # 画像指定で移動させる
        return _mv_to_xx(aem, here("df_img/ov_ft.png"))
    return False


def mv_to_develop(aem: AndroidEmuMacro) -> bool:
    # ov開く
    if open_overview(aem):
        # 工廠の項目がないならずらず
        while not aem.is_there_img(here("df_img/ov_dev.png")):
            _swipe_wt(aem, X_RIGHT, Y)

        # 画像指定で移動させる
        return _mv_to_xx(aem, here("df_img/ov_dev.png"))
    return False


def mv_to_cic(aem: AndroidEmuMacro) -> bool:
    # ov開く
    if open_overview(aem):
        # 工廠の項目がないならずらず
        while not aem.is_there_img(here("df_img/ov_cic.png")):
            _swipe_wt(aem, X_RIGHT, Y)

        # 画像指定で移動させる
        return _mv_to_xx(aem, here("df_img/ov_cic.png"))
    return False
