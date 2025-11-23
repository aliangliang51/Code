import cv2 as cv
import mediapipe as mp
import csv
import os
import time


log_file = "logs/hand_raise.csv"


def init_log():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists(log_file):
        with open(log_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Status"])


def hand_raise_detector():
    init_log()

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cam = cv.VideoCapture(0)

    print("=== 举手检测已启动 ===")

    while True:
        ret, img = cam.read()
        if not ret:
            break

        img = cv.flip(img, 1)
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        result = pose.process(rgb)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            wrist_y = landmarks[15].y  # 右手腕
            shoulder_y = landmarks[11].y  # 右肩膀

            if wrist_y < shoulder_y:
                status = "举手中"
                cv.putText(img, "Hand Raised", (50, 50),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                with open(log_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), status])

            mp_drawing.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv.imshow("Hand Raise Detect", img)

        if cv.waitKey(1) & 0xff == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    hand_raise_detector()
