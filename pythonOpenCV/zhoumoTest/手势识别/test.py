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