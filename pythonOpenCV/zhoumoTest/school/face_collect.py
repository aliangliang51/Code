import cv2
import numpy as np
import csv
from os.path import exists

# 加载 OpenCV 人脸检测器（使用内置 Haar 级联分类器）
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# 初始化摄像头（0 为默认 USB 摄像头，可根据实际调整为 1）
cap = cv2.VideoCapture(0)

cap.set(3, 640)  # 设置画面宽度为 640px
cap.set(4, 480)  # 设置画面高度为 480px

# 输入学生信息（支持终端或 SecureCRT 远程输入）
student_id = input("请输入学生学号：")
student_name = input("请输入学生姓名：")

# 人脸特征存储列表（用于存储多帧人脸特征，取平均值降低噪声）
face_features = []
count = 0  # 采集计数器（采集 20 帧特征）

print("请面向摄像头，开始采集人脸（共采集 20 张，按 'q' 可提前退出）...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("读取摄像头画面失败！")
        break

    # 转换为灰度图（降低计算量，提升检测效率）
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测人脸（返回人脸矩形坐标：x 横坐标，y 纵坐标，w 宽度，h 高度）
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # 在画面上绘制人脸矩形框（绿色，线宽 2）
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        count += 1

        # 提取人脸区域（ROI）并统一尺寸（100x100px）
        face_roi = gray[y:y + h, x:x + w]
        face_roi = cv2.resize(face_roi, (100, 100))

        # 将人脸特征转为一维数组，存入列表
        face_features.append(face_roi.flatten())

        # 在画面上显示采集进度
        cv2.putText(frame, f"采集进度：{count}/20", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # 显示采集画面
    cv2.imshow("人脸采集（按 'q' 退出）", frame)

    # 采集满 20 帧或按 'q' 退出
    if count >= 20 or cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 保存人脸特征到本地数据库（CSV 文件）
if face_features:
    # 取前 20 帧特征的平均值，作为该学生的基准特征（去噪）
    avg_feature = np.mean(face_features[:20], axis=0)

    # 检查数据库文件是否存在，不存在则创建并写入表头
    file_exists = exists("student_face_db.csv")
    with open("student_face_db.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["学号", "姓名", "人脸特征（10000维）"])
        # 将特征数组转为字符串，存入 CSV
        writer.writerow([student_id, student_name, ",".join(map(str, avg_feature))])

    print(f"\n{student_name}（学号：{student_id}）人脸采集完成，已存入数据库！")
else:
    print("\n未采集到有效人脸，请重新运行程序！")

# 释放摄像头与窗口资源
cap.release()
cv2.destroyAllWindows()