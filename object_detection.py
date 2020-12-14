import cv2


class ObjectDetection:
    def __init__(self):
        self.__color_base_src = None
        self.__color_temp_src = None
        self.__kp1 = []
        self.__kp2 = []
        self.__matches = []
        self.__good = []

    def save_match_img(self, save_path="./match_img.png", display_num=20):
        match_img = cv2.drawMatches(self.__color_base_src, self.__kp1, self.__color_temp_src, self.__kp2,
                                    self.__good[:display_num], None,
                                    flags=2)
        cv2.imwrite(save_path, match_img)

    def akaze_knn_match(self, query_img_path: str, train_img_path: str):
        result = []

        gray1 = cv2.imread(query_img_path, 0)
        gray2 = cv2.imread(train_img_path, 0)

        detector = cv2.AKAZE_create()

        self.__kp1, des1 = detector.detectAndCompute(gray1, None)
        self.__kp2, des2 = detector.detectAndCompute(gray2, None)

        bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)
        self.__matches = bf.knnMatch(des1, des2, 2)

        return result

    def match_img(self, query_img_path: str, train_img_path: str, ratio=0.5) -> list:
        self.__color_base_src = cv2.imread(query_img_path, 1)
        self.__color_temp_src = cv2.imread(train_img_path, 1)

        self.akaze_knn_match(query_img_path, train_img_path)

        for m, n in self.__matches:
            if m.distance < ratio * n.distance:
                self.__good.append(m)

        self.__good = sorted(self.__good, key=lambda x: x.distance)

        coordinate = []
        for elem in self.__good:
            coordinate.append(self.__kp1[elem.queryIdx].pt)

        return coordinate


# debug
if __name__ == '__main__':
    od = ObjectDetection()
    cd = od.match_img("img/screenshot7.png", "img/screenshot6.png")
    od.save_match_img()
    for elem in cd[:20]:
        print(elem)
