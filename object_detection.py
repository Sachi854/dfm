import cv2
import numpy as np


class ObjectDetection:

    # ここに画像のセーブ機能をマージしてしまう
    # てか保持してるフィールドを減らす
    # まず,　フィールドを整理する
    @staticmethod
    def __pre_calc_akaze(query_img_path: str, train_img_path: str) -> list:
        # 正規化処理もあるっぽいけど精度おちる...
        gamma22LUT = np.array([pow(x / 255.0, 2.2) for x in range(256)],
                              dtype='float32')
        # gray1 = cv2.LUT(cv2.imread(query_img_path), gamma22LUT)
        # gray2 = cv2.LUT(cv2.imread(train_img_path), gamma22LUT)
        gray1 = cv2.imread(query_img_path, 0)
        gray2 = cv2.imread(train_img_path, 0)

        detector = cv2.AKAZE_create()
        kp1, des1 = detector.detectAndCompute(gray1, None)
        kp2, des2 = detector.detectAndCompute(gray2, None)

        return [kp1, des1, kp2, des2]

    #  こっちのマッチングはたぶん使わない
    def __match_akaze(self, query_img_path: str, train_img_path: str) -> list:
        kp1, des1, kp2, des2 = self.__pre_calc_akaze(query_img_path, train_img_path)

        bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        return [matches, kp1, des1, kp2, des2]

    def __match_knn_akaze(self, query_img_path: str, train_img_path: str) -> list:
        kp1, des1, kp2, des2 = self.__pre_calc_akaze(query_img_path, train_img_path)
        bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)

        # 下流のdes2が輝度不足でNoneになって全部死ぬのどうにかしないとx
        matches = None
        if des2 is not None:
            matches = bf.knnMatch(des1, des2, 2)

        return [matches, kp1, des1, kp2, des2]

    # akazeはグレースケールでマッチングさせるので色で判別できないので注意
    # ratio testで振り分ける方を採用(今後は一番いい順と組み合わせて精度上げたい)
    def __match_img_akaze(self, query_img_path: str, train_img_path: str, ratio=0.5,
                          save_img=[False, "mif.png"]) -> list:
        result = [None, None]
        # くそみてぇな例外の握り潰しになってるから
        # 今後, 輝度が足りねぇ時に画像を加工するコードを追加するように
        try:
            result = self.__match_knn_akaze(query_img_path, train_img_path)
        except:
            pass

        good = []
        if result[0] is None:
            return []
        for m, n in result[0]:
            if m.distance < ratio * n.distance:
                good.append(m)

        good = sorted(good, key=lambda x: x.distance)

        if save_img[0]:
            self.__save_match_feature_img(cv2.imread(query_img_path, 1), result[1], cv2.imread(train_img_path, 1),
                                          result[3], good, save_img[1])

        coordinate = []
        for elem in good:
            coordinate.append(result[1][elem.queryIdx].pt)

        return coordinate

    @staticmethod
    def __save_match_feature_img(img1, kp1, img2, kp2, match_obj, save_path):
        match_img = cv2.drawMatches(img1, kp1, img2, kp2, match_obj[:10], None, flags=2)
        # match_img = cv2.drawMatches(img1, kp1, img2, kp2, match_obj, None, flags=2)
        cv2.imwrite(save_path, match_img)

    @staticmethod
    def __save_match_template_img(img1, img2, loc, save_path):
        s, w, h = img2.shape[::-1]
        img = img1.copy()

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

        cv2.imwrite(save_path, img)

    def match_img_feature(self, query_img_path: str, train_img_path: str, threshold=4, sample_num=20,
                          ratio=0.5, save_img=[False, "mif.png"]) -> list:
        mr = self.__match_img_akaze(query_img_path, train_img_path, ratio, save_img=save_img)[:sample_num]

        # もっとましな方法あるはずだから要検討
        # 高精度でマッチングした点が4以上であれば処理をする
        if len(mr) >= threshold:
            r_std = np.std(np.array(mr), axis=0)
            r_average = np.average(np.array(mr), axis=0)

            # 標準偏差以上に差がある座標を削除
            result = list(
                filter(lambda x: np.abs(r_average[0] - x[0]) < r_std[0] and np.abs(r_average[1] - x[1]) < r_std[1], mr))

            return [True, np.average(np.array(result), axis=0).tolist()]
        else:
            return [False, [None, None]]

    # 複数個検知なんてもんはない()
    # 複数個発見した場合にすべての座標を返すように変更する
    # ここに画像のセーブ機能をマージしてしまう <- 頭悪い設計
    def match_img_template(self, query_img_path: str, train_img_path: str, threshold=0.8,
                           save_img=[False, "mit.png"]) -> list:
        img1 = cv2.imread(query_img_path, 1)
        img2 = cv2.imread(train_img_path, 1)

        s, w, h = img2.shape[::-1]
        # TM_CCOEFF_NORMED(相関係数法(正規化))が一番精度いいらしい, 他には相互関数, 最小二乗法等がある
        # 予測精度は1に近いほどよい(最小二乗法は0に近いほうがよい)
        res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)
        if loc[0].size == 0:
            return [False, [None, None]]

        coordinate = np.average(loc, axis=1).tolist()
        coordinate.reverse()

        coordinate[0] = coordinate[0] + (w / 2.0)
        coordinate[1] = coordinate[1] + (h / 2.0)

        if save_img[0]:
            self.__save_match_template_img(img1, img2, loc, save_img[1])

        return [True, coordinate]


# debug
if __name__ == '__main__':
    od = ObjectDetection()
    cd = od.match_img_template("imgs/screenshot18.png", "df_img/h_koho.png", save_img=[True, "tinko.png"])
    print(cd)
    mf = od.match_img_feature("imgs/screenshot18.png", "img/h_koho.png", save_img=[True, "tintin.png"])
    print(mf)
