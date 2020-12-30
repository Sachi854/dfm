from android_emu_macro import AndroidEmuMacro
import random


def check_logistic_support(aem: AndroidEmuMacro) -> bool:
    result = False
    # 後方支援が帰ってるか判定
    while aem.is_there_img("df_img/b_ls.png"):
        result = True
        aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
        aem.sleep(2)
        aem.tap_img("df_img/b_ls_apply.png")
        aem.sleep(8)
    return result


if __name__ == '__main__':
    aem = AndroidEmuMacro()
    aem.connect()
    aem.sleep(2)

    # macro area
    ##########################
    ct = 0
    while True:
        if check_logistic_support(aem):
            print("遠征:" + str(ct) + '回目 お" 疲" れ" さ" ま" に" ゃ" ぁ" ぁ" ぁ" ぁ" ぁ"～')
            ct = ct + 1
        aem.sleep(120)
    ##########################

    aem.disconnect()
