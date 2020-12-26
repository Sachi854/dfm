from android_emu_macro import AndroidEmuMacro
import random


###################################################
# 使うならこのレベルのAPIがいいとおもう
###################################################

# ベースを基準に動かそうとおもう
# まるちめにゅーっぽいやつは保留

# うごく
# 後方支援処理
def check_logistic_support(aem: AndroidEmuMacro) -> bool:
    result = False
    while aem.is_there_img("df_img/b_ls.png"):
        result = True
        aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
        aem.sleep(1)
        aem.tap_img("df_img/b_ls_apply.png")
        aem.sleep(10)
    return result


# 未検証
# 獲得キャラをすべて分解
def disassemble_all_char(aem: AndroidEmuMacro) -> bool:
    if __go_b2factory(aem):
        __go_ft2retire(aem)
        while __enter_select_char(aem):
            __select_char(aem)
            aem.sleep(0.2)
            __disassemble(aem)
            aem.sleep(1.0)
        __return_base(aem)
        return True
    return False


###################################################
# 以下下層の実装
###################################################

# いちおううごく
# まるちめにゅー？からベースに移動
def __return_base(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img("df_img/multi_menu.png"):
        aem.sleep(5)
        if aem.tap_img("df_img/return_base.png"):
            aem.sleep(10)
            return True
    return False


# うごく
# ベースから工廠へ移動
def __go_b2factory(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img("df_img/b_ft.png"):
        aem.sleep(10)
        return True
    return False


# うごく
# 工廠から回収分解に移動
def __go_ft2retire(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img("df_img/ft_da.png"):
        aem.sleep(5)
        return True
    return False


# うごく
# 人形を上一列選択
def __select_char(aem: AndroidEmuMacro) -> bool:
    aem.tap(random.randrange(80, 230, 1), random.randrange(230, 460, 1))
    aem.sleep(0.1)
    aem.tap(random.randrange(350, 500, 1), random.randrange(230, 460, 1))
    aem.sleep(0.1)
    aem.tap(random.randrange(600, 750, 1), random.randrange(230, 460, 1))
    aem.sleep(0.1)
    aem.tap(random.randrange(850, 1000, 1), random.randrange(230, 460, 1))
    aem.sleep(0.1)
    aem.tap(random.randrange(1130, 1280, 1), random.randrange(230, 460, 1))
    aem.sleep(0.1)
    aem.tap(random.randrange(1400, 1550, 1), random.randrange(230, 460, 1))
    aem.sleep(0.1)
    return aem.tap_img("df_img/sc_apply.png")


# うごく
# 分解の解体ボタンをおす
def __disassemble(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img("df_img/da_apply.png"):
        aem.sleep(0.5)
        while aem.tap_img("df_img/da_e_apply.png"):
            aem.sleep(0.5)
        return True
    return False


def __enter_select_char(aem: AndroidEmuMacro) -> bool:
    aem.tap_img("df_img/da_select_char.png")
    aem.sleep(1.0)
    if aem.is_there_img("df_img/da_.png"):
        return False
    return True


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
        print(disassemble_all_char(aem))
        pass
    except KeyboardInterrupt:
        aem.disconnect()
        print("周回を終了")

    # デバッグ用に用意, リリース時は削除するように
    aem.disconnect()
    print("周回を終了")
