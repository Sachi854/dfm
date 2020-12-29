from android_emu_macro import AndroidEmuMacro
import random
import cv2
import numpy as np

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
    # 後方支援が帰ってるか判定
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
    # ベースから工廠へ
    if __go_b2factory(aem):
        aem.sleep(load_maximum)
        # 分解の画面へ
        __go_ft2retire(aem)
        aem.sleep(load_medium)
        # 分解できるキャラがいればキャラ選択へ
        while __enter_select_char(aem):
            # キャラ選択とばらすボタンオス処理
            __select_char(aem)
            aem.sleep(load_minimum)
            __disassemble(aem)
            aem.sleep(load_medium)

        # ベースへ
        __return_base(aem)
        aem.sleep(load_maximum)
        return True
    return False


# うごく
# 作戦報告書を作る
def make_fd(aem: AndroidEmuMacro) -> bool:
    # 工廠->マルチメニュー経由でデータルームへ
    __go_b2factory(aem)
    aem.sleep(load_maximum)
    __open_multi_menu(aem)
    aem.sleep(load_medium)
    __go_m2dataroom(aem)
    aem.sleep(load_maximum)

    # フロッピー作る処理
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
    # ベースから部隊編集へ
    if __go_b2ef(aem):
        aem.sleep(load_maximum)

        # 2部隊を選択
        __select_echelon_2(aem)
        aem.sleep(load_medium)

        # 陣形編集へ
        __go_ef2form(aem)
        aem.sleep(load_medium)
        __go_form2cfm(aem)
        aem.sleep(load_medium)

        # プリセット入れ替え
        if is_formation_1:
            result = __select_formation(aem, "df_img/ef2.png")
        else:
            result = __select_formation(aem, "df_img/ef1.png")

        aem.sleep(load_medium)
        __go_form2ef(aem)
        aem.sleep(load_medium)

        # 2部隊と1部隊を交換するコードを追加
        result = __change_e2_to_e1(aem)
        aem.sleep(load_medium)

        # TODO これバグいから変更, 下位APIに手動で部分比較させるコードを追加する部分
        # 2部隊が隊長が確実にいるように変更
        __set_reader(aem)
        aem.sleep(load_medium)

        # ベースへ
        __return_base(aem)
        aem.sleep(load_maximum)

    return result


# 0-2に侵入するコード
def go_02(aem: AndroidEmuMacro) -> bool:
    result = False
    # 戦役選択画面へ
    if __go_b2combat(aem):
        aem.sleep(load_maximum)
        # 02があったら押す
        if __select_02(aem):
            aem.sleep(load_medium)
            result = aem.tap_img("df_img/cbt_apply.png")
            aem.sleep(load_maximum)

    return result


# TODO posはintじゃなくてfloatでとれるから下層のシグネチャを変更しろ
# TODO 奴隷1号の破壊ぐわいを確認するコードを追記せよ
# 0-2で周回を行うコード
# ここは要検討, noteを参照するように
# 実装が適当になるのが確定
# return
# 1. is finishing this func : bool
# 2. is exp full : bool
def do_combat_02(aem: AndroidEmuMacro) -> list:
    # init
    ###############################
    # 部隊配置
    flg1, pos_e1 = __drop_e1(aem)
    flg2, pos_e2 = __drop_e2(aem)
    # 戦闘開始
    __start_combat(aem)
    aem.sleep(load_maximum)
    # 2部隊に補給
    __select_e(aem, pos_e2)
    aem.sleep(load_medium)
    __supply_e(aem, pos_e2)
    aem.sleep(load_medium)
    # 2部隊を退却
    __exit_e(aem, pos_e2)
    aem.sleep(load_maximum)
    # 1部隊を選択
    __select_e(aem, pos_e1)
    aem.sleep(load_medium)

    # set route
    ##############################
    # プランモードを開始
    __select_plan_mode(aem)
    aem.sleep(load_minimum)
    # ルートをセット
    __set_route_02(aem)
    aem.sleep(load_medium)

    # do combat
    ##############################
    __do_plan(aem)
    if aem.is_there_img("df_img/c02_warning.png"):
        return False

    # end process
    ##############################
    tmp = 0
    result = False
    while True and tmp < 10:
        tmp = tmp + 1
        aem.sleep(30)
        if aem.is_there_img("df_img/c02_result.png"):
            aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
            aem.sleep(load_medium)
            aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
            aem.sleep(load_medium)
            aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
            aem.sleep(load_medium)
            result = True
            break

    # return base
    ##############################
    __return_base(aem)
    aem.sleep(load_maximum)

    return [result, False]


###################################################
# 以下下層の実装
###################################################

# TODO 関数ごとに分別して後で然るべき場所に再配置せよ
# 一時的にここに戦闘のコード書くね...
# 明らかにラッパーにできる->あとでええやんけ

def __do_plan(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/c02_do_plan.png")


# 進行ルートを設定
def __set_route_02(aem: AndroidEmuMacro) -> bool:
    result = False
    result, pos = aem.match("df_img/c02_p6798.png")
    # power 4795 出現までスワイプする
    tmp = 0
    while result and not aem.is_there_img("df_img/c02_p4797.png") and tmp < 5:
        tmp = tmp + 1
        aem.swipe(pos[0], pos[1], pos[0], 900)

    # p4795をタップ
    aem.tap_img("df_img/c02_p4797.png")

    # 終点が見えるまでスワイプ x -> 700くらいまで
    tmp = 0
    while not aem.is_there_img("df_img/c02_endpoint.png") and tmp < 5:
        tmp = tmp + 1
        aem.swipe_img("df_img/c02_p6316.png", 110, 405)

    # 終点をタップ
    result = aem.tap_img("df_img/c02_endpoint.png")

    return result


def __swipe_c02_1(aem: AndroidEmuMacro, m_sec=500):
    return aem.swipe_img("df_img/c02_p6798.png", 200, 1050, m_sec=m_sec)


def __select_plan_mode(aem: AndroidEmuMacro):
    return aem.tap_img("df_img/c02_plan.png")


def __select_e(aem: AndroidEmuMacro, pos: list) -> bool:
    return aem.tap(pos[0], pos[1])


def __exit_e(aem: AndroidEmuMacro, pos: list) -> bool:
    aem.tap(pos[0], pos[1])
    aem.sleep(load_medium)
    aem.tap_img("df_img/c02_exit.png")
    aem.sleep(load_medium)
    return aem.tap_img("df_img/c02_exit_apply.png")


# 補給
def __supply_e(aem: AndroidEmuMacro, pos: list) -> bool:
    aem.tap(pos[0], pos[1])
    aem.sleep(load_medium)
    return aem.tap_img("df_img/c02_supply.png")


# 戦闘開始
def __start_combat(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/c02_apply.png")


# 部隊1の配置およびその位置の取得
def __drop_e1(aem: AndroidEmuMacro) -> list:
    result = aem.match("df_img/c02_hq.png")
    if result[0]:
        aem.tap(result[1][0], result[1][1])
        aem.sleep(load_medium)
        # 奴隷1号が壊れてたら修理する
        if __is_m16_broken(aem):
            # TODO 修復不可なら例外を投げるコードに改造する
            __repair_in_field(aem)
        # 配置する
        aem.tap_img("df_img/c02_drop.png")
        aem.sleep(load_medium)
        aem.sleep(load_medium)

    return result


# 部隊2の配置およびその位置の取得
def __drop_e2(aem: AndroidEmuMacro) -> list:
    result = aem.match("df_img/c02_h1.png")
    if result[0]:
        aem.tap(result[1][0], result[1][1])
        aem.sleep(load_medium)
        # 配置する
        aem.tap_img("df_img/c02_drop.png")
        aem.sleep(load_medium)
        aem.sleep(load_medium)

    return result


# 奴隷一号が壊れていないか確認する
def __is_m16_broken(aem: AndroidEmuMacro) -> bool:
    flg, pos = aem.match("df_img/c02_repair_m16.png")
    # hp bar の長さ y->218
    # y 位置 778
    y = 778
    if flg:
        aem.screenshot(0)
        img1 = cv2.imread("imgs/screenshot0.png")
        img2 = cv2.imread("df_img/c02_repair_bar.png")
        return np.array_equal(img1[y, int(pos[0]), ::], img2[0, 0, ::])

    return False


# パーティーを修理する
def __repair_in_field(aem: AndroidEmuMacro) -> bool:
    if aem.tap_img("df_img/c02_repair_apply.png"):
        return aem.tap_img("df_img/c02_repair_apply_re.png")


####
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


# 部隊編成へ戻る
def __go_form2ef(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/f_apply.png")


# うごく
# 工廠から回収分解に移動
def __go_ft2retire(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/ft_da.png")


# 部隊選択
def __select_echelon_2(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/e2_fix.png")


# 陣形プリセット選択
def __select_formation(aem: AndroidEmuMacro, img_path: str) -> bool:
    result = False
    if aem.tap_img(img_path):
        aem.sleep(load_medium)
        result = aem.tap_img("df_img/fc_apply.png")
        aem.sleep(load_medium)
        if aem.tap_img("df_img/fc_x.png") or aem.is_there_img("df_img/fc_v.png"):
            aem.sleep(load_minimum)
            aem.tap_img("df_img/fc_x_apply.png")
            aem.sleep(load_minimum)

    return result


def __set_reader(aem: AndroidEmuMacro) -> None:
    x = 424
    y = 304
    pitch = 277
    aem.screenshot(0)
    # TODO ここやっぱAPIの設計的に下層にしたほうよくね？
    img1 = cv2.imread("imgs/screenshot0.png")
    img2 = cv2.imread("df_img/kakera3.png")
    for i in range(1, 5):
        if not np.array_equal(img1[x, y + pitch * i, ::], img2[10, 10, ::]):
            aem.swipe((y + pitch * i), x, y, x)
            break


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
# 0-2を選択
def __select_02(aem: AndroidEmuMacro) -> bool:
    return aem.tap_img("df_img/cbt_02.png")


# 部隊2と部隊1を交換
def __change_e2_to_e1(aem: AndroidEmuMacro) -> bool:
    flag, pos = aem.match("df_img/e1_fix.png")
    if flag:
        aem.swipe_img("df_img/e2_active_fix.png", pos[0], pos[1], 1000)
        aem.sleep(load_medium)
        aem.tap_img("df_img/e_apply.png")

    return flag


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


#######################################################
# main func
def start_02_loop(aem: AndroidEmuMacro):
    # init
    print("初期化中......")
    is_ef1 = False
    is_exp_full = False
    check_logistic_support(aem)
    print("+準備完了+")
    print("------------------")

    # loop
    #############################
    # 人形の解体
    print("保有人形を解体中......")
    if disassemble_all_char(aem):
        print("全員解体")
    else:
        print("解体に失敗")
    check_logistic_support(aem)

    # 経験値たまってたらfd作る
    # 検知めんどいから回数と決め打ちでいいすか？
    if is_exp_full:
        make_fd(aem)
        check_logistic_support(aem)

    # 部隊の入れ替え
    print("アタッカーを交換中......")
    change_attacker(aem, is_ef1)
    print("アタッカーを交換")
    is_ef1 = not is_ef1
    check_logistic_support(aem)

    # やらかした即, break
    # 02侵入および戦闘
    print("0-2に侵入中")
    go_02(aem)
    print("0-2に侵入")
    print("戦闘開始")
    dummy, is_exp_full = do_combat_02(aem)
    print("戦闘終了")
    print("------------------")
    check_logistic_support(aem)
    ###############################

    # fd作る
    pass


def debug_func(aem: AndroidEmuMacro):
    # __set_reader(aem)
    # change_attacker(aem, True)
    # print(__is_m16_broken(aem))
    pass


# TODO 日付変更のに対応するコードを追加したほうがいいかも
if __name__ == '__main__':
    # init
    ###################################
    aem = AndroidEmuMacro()
    aem.connect()
    aem.sleep(2)
    print("周回を開始 : 停止 -> ctrl^c")
    print("==========================")

    # func
    ###################################
    start_02_loop(aem)
    # debug_func(aem)

    # destruct
    ###################################
    aem.disconnect()
    print("==========================")
    print("周回を終了")
    print("==========================")
