from android_emu_macro import AndroidEmuMacro
import random


# うごく
def check_logistic_support(aem: AndroidEmuMacro) -> bool:
    result = False
    while aem.is_there_img("df_img/h_ls.png"):
        result = True
        aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
        aem.sleep(1)
        aem.tap_img("df_img/h_ls_apply.png")
        aem.sleep(10)
    return result


def go_factory(aem: AndroidEmuMacro) -> bool:
    pass


if __name__ == '__main__':
    aem = AndroidEmuMacro()
    aem.connect()
    aem.sleep(2)

    # macro code
    print(check_logistic_support(aem))

    aem.disconnect()
