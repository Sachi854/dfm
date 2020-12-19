from android_emu_macro import AndroidEmuMacro
import random

if __name__ == '__main__':
    aem = AndroidEmuMacro()
    aem.connect()
    aem.sleep(2)

    # macro area
    ##########################
    ct = 0
    ct1 = 0
    while True:
        print("転生:" + str(ct1))
        ct1 = ct1 + 1
        while aem.is_there_img("df/ks_kikan.png"):
            print(str(ct) + "回目の遠征おつかれさまだにゃ～～～")
            ct = ct + 1
            aem.tap(random.randrange(400, 1500, 1), random.randrange(200, 800, 1))
            aem.sleep(1)
            aem.tap_img("df/ks_kakunin.png")
            aem.sleep(20)

        aem.sleep(120)
    ##########################

    aem.disconnect()
