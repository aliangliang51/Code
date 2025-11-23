# 📁 代码项目摘要：RK3568手势识别

## 文件: `handutil.py`

```python
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
```

---

## 文件: `main.py`

```python
import cv2 as cv
import numpy as np

from RK3568手势识别.handutil import HandDetector


def main():
    cap = cv.VideoCapture(0)
    detector = HandDetector()

    finger_img_list = [
        'fingers/0.png',
        'fingers/1.png',
        'fingers/2.png',
        'fingers/3.png',
        'fingers/4.png',
        'fingers/5.png',
    ]
    finger_list = []
    for fi in finger_img_list:
        i = cv.imread(fi)
        finger_list.append(i)

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        if success:
            img = detector.find_hands(img)
            lmslist = detector.find_position(img)
            tip_ids = [4, 8, 12, 16, 20]


            if len(lmslist) > 0:
                # print('lmslist:', lmslist)
                # print('lmslist.shape:', np.array(lmslist).shape)
                fingers = []
                for tid in tip_ids:
                    x,y = lmslist[tid][1], lmslist[tid][2]
                    cv.circle(img, (x,y), 10, (0,255,0), cv.FILLED)
                    if tid == 4:
                        # 根据食指和中指的位置判断左手右手
                        if lmslist[8][1] < lmslist[12][1]:
                            # 右手
                            if lmslist[tid][1] < lmslist[tid - 1][1]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                        else:
                            # 左手
                            if lmslist[tid][1] > lmslist[tid - 1][1]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                        # 如果是其他手指，如果这些手指的指尖的y位置大于第二关节的位置，则认为这个手指打开，否则认为这个手指关闭
                    else:
                        if lmslist[tid][2] < lmslist[tid - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                        # fingers是这样一个列表，5个数据，0代表一个手指关闭，1代表一个手指打开
                        # 判断有几个手指打开
                    cnt = fingers.count(1)
                    # print('cnt:', cnt)

                    # 找到对应的手势图片并显示
                    finger_img = finger_list[cnt]
                    w, h, c = finger_img.shape
                    img[0:w, 0:h] = finger_img



            cv.imshow("Image", img)

        k = cv.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()

```

---

## 文件: `test.py`

```python
import cv2 as cv
import numpy as np
import math

# 导入 pynput 库进行系统输入模拟
from pynput.mouse import Button, Controller as MouseController
import screeninfo

# 确保 HandDetector 类的导入路径正确
# 假设 handutil.py 文件就在 RK3568手势识别 目录下
from RK3568手势识别.handutil import HandDetector

# --- 初始化控制器和屏幕信息 ---
mouse = MouseController()

try:
    # 获取主屏幕分辨率
    screen = screeninfo.get_monitors()[0]
    SCREEN_W, SCREEN_H = screen.width, screen.height
except Exception as e:
    print(f"无法获取屏幕信息，使用默认值 1920x1080. 错误: {e}")
    SCREEN_W, SCREEN_H = 1920, 1080

# 摄像头分辨率
CAM_W, CAM_H = 640, 480

# --- 阈值和状态 ---
CLICK_DISTANCE_THRESHOLD = 35  # 拇指和食指尖捏合的最大距离 (像素)
SMOOTHING_FACTOR = 7  # 鼠标移动平滑系数 (值越大越平滑但延迟越大)

# 用于平滑鼠标移动的变量
plocX, plocY = 0, 0 # Previous location
clocX, clocY = 0, 0 # Current location

# 用于防止鼠标点击持续按下的状态
is_clicking = False


def main():
    global plocX, plocY, clocX, clocY, is_clicking

    cap = cv.VideoCapture(0)
    # 调整摄像头分辨率
    cap.set(3, CAM_W)
    cap.set(4, CAM_H)

    detector = HandDetector()

    print("--- 虚拟鼠标控制系统启动 (简化版) ---")
    print("功能：食指控制光标，拇指+食指捏合触发左键点击。")
    print("按 'q' 或 ESC 退出。")

    while True:
        success, img = cap.read()
        if not success:
            break

        # 左右翻转，提供“照镜子”体验
        img = cv.flip(img, 1)

        # 1. 检测手部关键点
        img = detector.find_hands(img, draw=True)
        lmslist = detector.find_position(img)

        if len(lmslist) > 0:

            # 获取食指尖 (ID 8) 和拇指尖 (ID 4) 的坐标
            # MediaPipe 关键点索引：8=食指尖，4=拇指尖
            x8, y8 = lmslist[8][1], lmslist[8][2]
            x4, y4 = lmslist[4][1], lmslist[4][2]

            # --- A. 坐标映射和光标移动 ---

            # 归一化并映射到屏幕坐标
            x_screen = int(np.interp(x8, (0, CAM_W), (0, SCREEN_W)))
            y_screen = int(np.interp(y8, (0, CAM_H), (0, SCREEN_H)))

            # 平滑处理：使用加权平均，减少光标抖动
            clocX = plocX + (x_screen - plocX) / SMOOTHING_FACTOR
            clocY = plocY + (y_screen - plocY) / SMOOTHING_FACTOR

            mouse.position = (int(clocX), int(clocY))

            # 更新前一次坐标
            plocX, plocY = clocX, clocY

            # 在图像上绘制食指尖和光标反馈
            cv.circle(img, (x8, y8), 10, (0, 255, 255), cv.FILLED)
            cv.putText(img, 'Cursor', (x8 + 15, y8 - 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)


            # --- B. 点击逻辑 (食指和拇指捏合) ---

            # 计算食指尖和拇指尖的距离
            distance = math.hypot(x8 - x4, y8 - y4)
            cv.line(img, (x8, y8), (x4, y4), (255, 0, 0), 2)

            if distance < CLICK_DISTANCE_THRESHOLD:
                # 捏合距离小于阈值 -> 触发点击
                cv.circle(img, (x4, y4), 10, (0, 0, 255), cv.FILLED)  # 捏合时拇指尖变红

                if not is_clicking:
                    print("--> Action: Mouse Left Click")
                    mouse.click(Button.left, 1) # 触发一次左键点击
                    is_clicking = True
            else:
                # 距离大于阈值 -> 允许下次点击
                is_clicking = False


        # 显示图像
        cv.imshow("Simple Virtual Mouse", img)

        k = cv.waitKey(1) & 0xff
        if k == ord('q') or k == 27:  # 按 'q' 或 ESC 退出
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
```

---

