import mediapipe as mp
import cv2 as cv


class HandDetector:
    """
    手势识别
    """

    def __init__(self, mode=False, max_hands=2, complexity=1, detection_con=0.5, track_con=0.5):
        """
        手势识别初始化
        :param mode:是否为静态图片，默认为false（不是静态图片）
        :param max_hands: 最多检测几只手，默认为2
        :param complexity:模型复杂度，默认为1
        :param detection_con: 最小置信度，默认为0.5
        :param track_con:最小追踪置信度，默认为0.5
        """
        self.mode = mode
        self.max_hands = max_hands
        self.complexity = complexity
        self.detection_con = detection_con
        self.track_con = track_con
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=mode,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def find_hands(self, img,draw=True):
        """
        :param img: 输入图像
        :param draw: 是否绘制手部关键点和连接线
        :return: 处理过的图像
        """
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(imgRGB, handLms, mp.solutions.hands.HAND_CONNECTIONS)

        img = cv.cvtColor(imgRGB, cv.COLOR_BGR2RGB)
        return img

    def find_position(self, img, handNo=0):
        """
        获得手势数据
        :param img: 视频帧图片
        :param handNo: 手编号（默认为0，第一只手）
        :return: 关键点列表
        """
        self.lmsList = []

        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmsList.append([id, cx, cy])

        return self.lmsList