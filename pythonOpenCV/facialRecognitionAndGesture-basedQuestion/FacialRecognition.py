from flask import Flask, render_template, Response
import cv2 as cv
import json
import time
import csv
import os
import io

# 导入您原始代码中的核心函数
# 假设您将 load_mapping, mark_attendance 等函数放到了一个模块中，
# 但为了简洁，这里直接复制过来。

attendance_file = "logs/attendance.csv"


def load_mapping():
    # ... (您的 load_mapping 函数内容不变)
    with open("config/names_mapping.json", "r") as f:
        mapping = json.load(f)
    return {v: k for k, v in mapping.items()}


def mark_attendance(student_id, name):
    # ... (您的 mark_attendance 函数内容不变)
    exists = False
    today = time.strftime("%Y-%m-%d")

    if not os.path.exists(attendance_file):
        init_attendance_file()  # 假设 init_attendance_file 也已导入或定义

    with open(attendance_file, "r", encoding="utf-8") as f:
        # 使用更安全的csv reader/DictReader来检查
        reader = csv.reader(f)
        next(reader, None)  # 跳过标题行
        for row in reader:
            if len(row) >= 3 and str(student_id) == row[0] and today in row[2]:
                exists = True
                break

    if not exists:
        with open(attendance_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([student_id, name, time.strftime("%Y-%m-%d %H:%M:%S")])
            print(f"[考勤] {name} 已记录")


# --- M-JPEG 视频流生成函数 ---
def generate_frames():
    """
    这个函数取代了您原始代码中的 'while True' 循环和 cv.imshow()
    """
    # 重新加载模型和映射
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    face_cascade = cv.CascadeClassifier('config/haarcascade_frontalface_default.xml')
    names = load_mapping()

    cam = cv.VideoCapture(0)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    print("=== Flask 视频流启动 ===")

    while True:
        ret, img = cam.read()
        if not ret:
            # 如果摄像头读取失败，等待并重试
            time.sleep(1)
            continue

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            # 1. 识别
            student_id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            # 2. 绘制和考勤
            if conf < 80:  # 置信度判断
                name = names.get(student_id, "未知")
                mark_attendance(student_id, name)
                label = f"{name} ({conf:.1f})"
                color = (0, 255, 0)
            else:
                label = f"未知 ({conf:.1f})"
                color = (0, 0, 255)

            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv.putText(img, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 3. 编码为 JPEG
        ret, buffer = cv.imencode('.jpg', img)
        frame = buffer.tobytes()

        # 4. 返回 M-JPEG 格式数据
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cam.release()
    cv.destroyAllWindows()


app = Flask(__name__)


@app.route('/')
def index():
    """实时监控页面"""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """
    用于实时传输视频流的路由
    """
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/attendance_log')
def attendance_log():
    """
    读取并展示考勤记录
    """
    records = []
    if os.path.exists(attendance_file):
        with open(attendance_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = list(reader)
    return render_template('history.html', records=records)


if __name__ == '__main__':
    # 注意: debug=True 在生产环境不安全
    app.run(host='0.0.0.0', debug=True)