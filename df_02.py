from android_emu_macro import AndroidEmuMacro
import random

###################################################
# 使うならこのレベルのAPIがいいとおもう
###################################################

# 待機時間を一応書いておく
load_maximum = 8.0
load_medium = 2.0
load_minimum = 0.4


# ベースを基準に動かそうとおもう
# まるちめにゅーっぽいやつは保留

# うごく
# 後方支援処理
def check_logistic_support(aem: AndroidEmuMacro) -> bool:
    result = False
    while aem.is_there_img("df_img/b_ls.png"):
        result = True
        aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
        aem.sleep(load_medium)
        aem.tap_img("df_img/b_ls_apply.png")
        aem.sleep(load_maximum)
    return result


# うごく
# 獲得キャラをすべて分解
def disassemble_all_char(aem: AndroidEmuMacro) -> bool:
    if __go_b2factory(aem):
        aem.sleep(load_maximum)
        __go_ft2retire(aem)
        aem.sleep(load_medium)
        while __enter_select_char(aem):
            __select_char(aem)
            aem.sleep(load_minimum)
            __disassemble(aem)
            aem.sleep(load_medium)
        __return_base(aem)
        aem.sleep(load_maximum)
        return True
    return False


# うごく
# 作戦報告書を作る
def make_fd(aem: AndroidEmuMacro) -> bool:
    __go_b2factory(aem)
    aem.sleep(load_maximum)
    __open_multi_menu(aem)
    aem.sleep(load_medium)
    __go_m2dataroom(aem)
    aem.sleep(load_maximum)

    # ここに報告書作るコードいれろ
    if __make_fd(aem):
        __return_base(aem)
        aem.sleep(load_maximum)
        return True
    else:
        __return_base(aem)
        aem.sleep(load_maximum)
        return False


# TODO 戦闘に飛ぶ可能性があるっぽいから検証しとけ
# あやしいけどうごく
# アタッカーの入れ替え
def change_attacker(aem: AndroidEmuMacro, is_formation_1: bool) -> bool:
    result = False
    if __go_b2ef(aem):
        aem.sleep(load_maximum)
        __go_ef2form(aem)
        aem.sleep(load_medium)
        __go_form2cfm(aem)
        aem.sleep(load_medium)

        if is_formation_1:
            result = __select_formation(aem, "df_img/ef2.png")
        else:
            result = __select_formation(aem, "df_img/ef1.png")

        aem.sleep(load_medium)
        __go_form2ef(aem)
        aem.sleep(load_medium)
        __return_base(aem)
        aem.sleep(load_maximum)

    return result


# 0-2に侵入するコード
def go_02(aem: AndroidEmuMacro) -> bool:
    result = False
    if __go_b2combat(aem):
        aem.sleep(load_maximum)
        if __select_02(aem):
            aem.sleep(load_medium)
            result = aem.tap_img("df_img/cbt_apply.png")
            aem.sleep(load_maximum)

    return result


###################################################
# 以下下層の実装
###################################################

# たぶんうごく
# マルチメニューをひらく
def __open_multi_menu(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/multi_menu.png")


# うごく
# マルチメニューからデータルームに飛ぶ
def __go_m2dataroom(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/mm_dr.png")


# いちおううごく
# まるちめにゅー？からベースに移動
def __return_base(aem: AndroidEmuMacro) -> bool:
    if __open_multi_menu(aem):
        aem.sleep(load_medium)
        return aem.tap_img("df_img/return_base.png")
    return False


# ベースto戦闘
def __go_b2combat(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/b_cbt.png")


# うごく
# ベースから工廠へ移動
def __go_b2factory(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/b_ft.png")


# うごく
# ベースto部隊編成
def __go_b2ef(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/b_ef.png")


# 部隊編成to陣形編成
def __go_ef2form(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/ef_f.png")


# 陣形編成to陣形プリセット
def __go_form2cfm(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/f_fc.png")


# 陣形プリセット選択
def __select_formation(aem: AndroidEmuMacro, img_path: str) -> bool:
    result = False
    if aem.tap_img(img_path):
        aem.sleep(load_medium)
        result = aem.tap_img("df_img/fc_apply.png")
        aem.sleep(load_medium)
        if aem.tap_img("df_img/fc_x.png"):
            aem.sleep(load_minimum)
            aem.tap_img("df_img/fc_x_apply.png")
            aem.sleep(load_minimum)

    return result


# 部隊編成へ戻る
def __go_form2ef(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/f_apply.png")


# うごく
# 工廠から回収分解に移動
def __go_ft2retire(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/ft_da.png")


# うごく
# 人形を上一列選択
def __select_char(aem: AndroidEmuMacro) -> bool:
    aem.tap(random.randrange(80, 230, 1), random.randrange(230, 460, 1))
    aem.sleep(load_minimum)
    aem.tap(random.randrange(350, 500, 1), random.randrange(230, 460, 1))
    aem.sleep(load_minimum)
    aem.tap(random.randrange(600, 750, 1), random.randrange(230, 460, 1))
    aem.sleep(load_minimum)
    aem.tap(random.randrange(850, 1000, 1), random.randrange(230, 460, 1))
    aem.sleep(load_minimum)
    aem.tap(random.randrange(1130, 1280, 1), random.randrange(230, 460, 1))
    aem.sleep(load_minimum)
    aem.tap(random.randrange(1400, 1550, 1), random.randrange(230, 460, 1))
    aem.sleep(load_minimum)
    return aem.tap_img("df_img/sc_apply.png")


# TODO ずれてたときに修正するコード追加したほうがいいかも
def __select_02(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/cbt_02.png")


# うごく
# 分解の解体ボタンをおす
def __disassemble(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img("df_img/da_apply.png"):
        aem.sleep(load_minimum)
        while aem.tap_img("df_img/da_e_apply.png"):
            aem.sleep(load_minimum)
        return True
    return False


# うごく
# キャラ選択画面へ移行
def __enter_select_char(aem: AndroidEmuMacro) -> bool:
    aem.tap_img("df_img/da_select_char.png")
    aem.sleep(load_medium)
    if aem.is_there_img("df_img/da_.png"):
        return False
    return True


# うごく
# データルーム内からフロッピーディスクを作る
def __make_fd(aem: AndroidEmuMacro) -> bool:
    result = False
    if aem.tap_img("df_img/dr_dk.png"):
        aem.sleep(load_minimum)
        aem.tap_img("df_img/dr_dk_start.png")
        aem.sleep(load_minimum)
        if aem.tap_img("df_img/dr_dk_apply.png"):
            result = True
            if aem.is_there_img("df_img/dr_dk_apply.png"):
                aem.sleep(load_minimum)
                aem.tap_img("df_img/dr_dk_cancel.png")
                result = False

        if not result:
            aem.sleep(load_minimum)
            aem.tap_img("df_img/dr_dk_bk.png")

    return result


if __name__ == '__main__':
    aem = AndroidEmuMacro()
    aem.connect()
    aem.sleep(2)
    print("周回を開始 : 停止 -> ctrl^c")
    print("==========================")

    # macro code
    try:
        # check_logistic_support(aem)
        # go_h2factory(aem)
        # go_ft2retire(aem)
        # return_base(aem)
        # __select_char(aem)
        # __select_disassemble(aem)
        # print(disassemble_all_char(aem))
        # print(make_fd(aem))
        # print(change_attacker(aem, True))
        # print(change_attacker(aem, False))
        go_02(aem)
        pass
    except KeyboardInterrupt:
        aem.disconnect()
        print("周回を終了")

    # デバッグ用に用意, リリース時は削除するように
    aem.disconnect()
    print("==========================")
    print("周回を終了")
    print("==========================")
