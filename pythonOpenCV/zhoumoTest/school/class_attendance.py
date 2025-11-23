import cv2
import numpy as np
import csv
from datetime import datetime

# 加载 OpenCV 人脸检测器
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# 加载本地学生人脸数据库（CSV 文件）
student_db = {}
try:
    with open("student_face_db.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 读取学号、姓名，将特征字符串转为数组
            sid = row["学号"]
            sname = row["姓名"]
            feature = np.array(list(map(float, row["人脸特征（10000维）"].split(","))))
            student_db[sid] = {"name": sname, "feature": feature}
    print(f"成功加载 {len(student_db)} 名学生的人脸数据！")
except FileNotFoundError:
    print("未找到学生人脸数据库（student_face_db.csv），请先执行人脸采集！")
    exit()

# 初始化摄像头（提高分辨率，适配多人检测）
cap = cv2.VideoCapture(0)

cap.set(3, 1280)  # 宽度 1280px
cap.set(4, 720)  # 高度 720px

# 考勤记录字典（key：学号，value：签到时间）
attendance_records = {}
print("\n课堂考勤已启动，按 'q' 结束考勤...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("读取摄像头画面失败，退出程序！")
        break

    # 转换为灰度图，优化检测效率
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测画面中的所有人脸（调整参数，适配多人场景）
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)

    # 遍历每一个检测到的人脸
    for (x, y, w, h) in faces:
        # 提取当前人脸的特征（与采集时格式保持一致）
        face_roi = gray[y:y + h, x:x + w]
        face_roi = cv2.resize(face_roi, (100, 100))
        current_feature = face_roi.flatten()

        # 与数据库中的人脸特征比对（计算欧氏距离，距离越小匹配度越高）
        min_dist = float("inf")  # 初始化最小距离
        matched_sid = None  # 匹配到的学生学号

        for sid, info in student_db.items():
            # 计算当前特征与数据库特征的欧氏距离
            dist = np.linalg.norm(current_feature - info["feature"])
            # 距离小于阈值（5000）且为最小值时，判定为匹配
            if dist < min_dist and dist < 5000:
                min_dist = dist
                matched_sid = sid

        # 根据匹配结果绘制矩形框与标签
        if matched_sid:
            sname = student_db[matched_sid]["name"]
            # 未签到则记录时间，已签到则仅显示姓名
            if matched_sid not in attendance_records:
                attendance_records[matched_sid] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 已签到：绿色框 + 标签
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{sname}（已签到）", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                # 已签到过：蓝色框 + 标签
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, sname, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        else:
            # 未匹配到学生：红色框 + 标签
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "未知人员", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # 在画面顶部显示考勤统计信息（黄色文字）
    total_students = len(student_db)
    checked_students = len(attendance_records)
    cv2.putText(frame, f"课堂考勤 | 总人数：{total_students} | 已签到：{checked_students}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # 显示考勤画面
    cv2.imshow("课堂人脸考勤（按 'q' 结束）", frame)

    # 按 'q' 键结束考勤
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 保存考勤记录到 CSV 文件（文件名含时间戳，避免覆盖）
output_filename = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(output_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["学号", "姓名", "签到状态", "签到时间"])
    # 写入已签到学生
    for sid, check_time in attendance_records.items():
        writer.writerow([sid, student_db[sid]["name"], "已签到", check_time])
    # 写入未签到学生
    for sid, info in student_db.items():
        if sid not in attendance_records:
            writer.writerow([sid, info["name"], "未签到", ""])

# 打印考勤结果 summary
print(
    f"\n考勤结束！本次考勤共 {total_students} 人，已签到 {checked_students} 人，未签到 {total_students - checked_students} 人。")
print(f"考勤记录已保存到：{output_filename}")

# 释放资源
cap.release()
cv2.destroyAllWindows()