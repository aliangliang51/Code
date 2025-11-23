from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2 as cv
import mediapipe as mp
import json
import time
import csv
import os
import numpy as np
from PIL import Image


# --- 1. HandDetector 类 (手势识别核心逻辑) ---

class HandDetector:
    """
    手势识别
    """

    def __init__(self, mode=False, max_hands=2, complexity=1, detection_con=0.5, track_con=0.5):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            model_complexity=complexity,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.tip_ids = [4, 8, 12, 16, 20]  # 指尖的关键点ID

    def find_hands(self, img, draw=False):
        """
        处理图像并检测手势。
        :param img: 输入图像 (BGR)
        :param draw: 是否绘制手部关键点和连接线
        :return: 原始 BGR 帧 (可能已被绘制修改)
        """
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if draw and self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, handNo=0):
        """
        获得手势关键点数据
        :param img: 视频帧图片
        :param handNo: 手编号（默认为0，第一只手）
        :return: 关键点列表 [[id, cx, cy], ...]
        """
        lmsList = []
        if self.results.multi_hand_landmarks and handNo < len(self.results.multi_hand_landmarks):
            Hand = self.results.multi_hand_landmarks[handNo]
            h, w, c = img.shape
            for id, lm in enumerate(Hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmsList.append([id, cx, cy])
        return lmsList

    def count_fingers(self, lmslist):
        """
        根据关键点列表计算伸出的手指数量 (0-5)
        """
        fingers = []

        if not lmslist:
            return 0

        # 1. 拇指 (ID 4) 判断：指尖 (4) 的 X 坐标是否在倒数第二个关节 (3) 的 X 坐标的外侧
        if lmslist[self.tip_ids[0]][1] < lmslist[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 2. 其它四个手指 (ID 8, 12, 16, 20) 判断：指尖的 Y 坐标是否小于倒数第二个关节的 Y 坐标
        for id in range(1, 5):
            tip_id = self.tip_ids[id]
            if lmslist[tip_id][2] < lmslist[tip_id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)


# --- 2. 全局状态配置 ---
ATTENDANCE_FILE = "logs/attendance.csv"
ANSWER_LOG_FILE = "logs/answer_log.csv"  # 作答日志文件
FACE_CASCADE_PATH = 'config/haarcascade_frontalface_default.xml'
# PROFILE_FACE_CASCADE_PATH 已移除
RECOGNIZER_PATH = 'trainer/trainer.yml'
MAPPING_PATH = 'config/names_mapping.json'
DATASET_PATH = 'dataset'
TRAINER_PATH = 'trainer'

# --- 全局状态管理 (用于人脸采集) ---
global_capture_state = {
    'is_capturing': False,
    'capture_id': 0,
    'capture_name': '',
    'capture_count': 0,
    'target_count': 30  # 目标采集数量
}


# --- 3. 初始化和日志函数 (保持不变) ---

def load_mapping():
    """加载 ID 到姓名的映射"""
    try:
        with open(MAPPING_PATH, "r", encoding='utf-8') as f:
            mapping = json.load(f)
        return {v: k for k, v in mapping.items()}  # {id: name}
    except FileNotFoundError:
        print("警告: names_mapping.json 文件未找到，将创建新文件。")
        return {}
    except Exception as e:
        print(f"警告: names_mapping.json 加载失败: {e}，将使用空映射。")
        return {}


def init_logs():
    """初始化 logs 和 dataset 文件夹以及 CSV 文件"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs(DATASET_PATH, exist_ok=True)
    os.makedirs(TRAINER_PATH, exist_ok=True)

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["ID", "Name", "Time"])

    if not os.path.exists(ANSWER_LOG_FILE):
        with open(ANSWER_LOG_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["Time", "Name", "Answer_Choice", "Fingers_Count"])


def log_attendance(student_id, name):
    """记录考勤 (每人每天只记录一次)"""
    today = time.strftime("%Y-%m-%d")
    exists = False

    try:
        with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3 and str(student_id) == row[0] and today in row[2]:
                    exists = True
                    break
    except Exception:
        pass  # 忽略读取错误

    if not exists and name != "未知":
        with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([student_id, name, time.strftime("%Y-%m-%d %H:%M:%S")])
            print(f"[考勤] {name} 已记录")


def log_answer(name, fingers_count):
    """记录作答事件"""
    if fingers_count < 1 or fingers_count > 5:
        return

    answer_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
    answer_choice = answer_map.get(fingers_count, 'N/A')

    with open(ANSWER_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([time.strftime("%Y-%m-%d %H:%M:%S"), name, answer_choice, fingers_count])


# --- 4. 模型加载与检查 ---
init_logs()
names_map = load_mapping()


def load_cascade(path, name):
    """加载级联分类器并检查文件是否存在"""
    if not os.path.exists(path):
        print(f"致命错误: {name} 文件未找到。请将 {path} 放入正确位置。")
        exit()
    return cv.CascadeClassifier(path)


# OpenCV 正脸识别/检测
face_cascade = load_cascade(FACE_CASCADE_PATH, "正面人脸分类器")
# profile_face_cascade = load_cascade(PROFILE_FACE_CASCADE_PATH, "侧面人脸分类器") # 已移除

recognizer = cv.face.LBPHFaceRecognizer_create()
try:
    recognizer.read(RECOGNIZER_PATH)
except cv.error:
    print("警告: 训练文件 trainer.yml 未找到或为空，无法进行人脸识别。")

# 使用 HandDetector
hand_detector = HandDetector()


# --- 5. 核心训练逻辑 (保持不变) ---
def train_model_logic():
    """训练人脸并保存模型"""
    global recognizer

    temp_recognizer = cv.face.LBPHFaceRecognizer_create()
    detector = cv.CascadeClassifier(FACE_CASCADE_PATH)

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:
            try:
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')
                filename_parts = os.path.split(imagePath)[-1].split("_")
                if len(filename_parts) < 2:
                    continue

                id = int(filename_parts[0])
                faces = detector.detectMultiScale(img_numpy)

                if len(faces) == 1:
                    x, y, w, h = faces[0]
                    # LBPH 需要统一尺寸的脸部 ROI
                    face_roi = cv.resize(img_numpy[y:y + h, x:x + w], (100, 100))
                    faceSamples.append(face_roi)
                    ids.append(id)

            except Exception as e:
                continue
        return faceSamples, ids

    print("正在训练人脸识别模型训练中...")
    faces, ids = getImagesAndLabels(DATASET_PATH)

    if len(faces) < 2 or len(np.unique(ids)) < 2:
        print("错误: 训练集中的人数少于两人或数据量不足，无法训练。")
        return False

    temp_recognizer.train(faces, np.array(ids))
    temp_recognizer.write(RECOGNIZER_PATH)

    # 重新加载识别器到全局变量
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.read(RECOGNIZER_PATH)

    print("模型训练完成并已保存到 trainer/trainer.yml")
    return True


# --- 6. 视频流生成函数 (考勤与作答逻辑分离) ---
def generate_frames():
    """统一处理所有检测、识别和作答逻辑，并生成视频流"""
    camera_index = int(os.environ.get('CAMERA_INDEX', 0))
    cam = cv.VideoCapture(camera_index)

    if not cam.isOpened():
        print(f"致命错误: 无法打开摄像头 (索引: {camera_index})。请检查设备是否连接或索引是否正确。")
        return

    cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    print(f"=== 智能系统启动中... (摄像头索引: {camera_index}) ===")
    last_answer_log_time = time.time()  # 记录上次作答时间
    frame_count = 0
    detect_interval = 5

    while True:
        ret, frame = cam.read()

        if not ret:
            print("警告: 摄像头读取失败，视频流结束或设备断开。")
            break

        frame = cv.flip(frame, 1)
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # 实时绘制手部关键点
        frame = hand_detector.find_hands(frame, draw=True)

        # ----------------------------------------------------
        # ⭐️ 1. 人脸数据采集/录制逻辑
        # ----------------------------------------------------
        if global_capture_state['is_capturing']:

            status_text = f"录制中: {global_capture_state['capture_name']} ({global_capture_state['capture_count']}/{global_capture_state['target_count']})"
            cv.putText(frame, status_text, (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            faces = face_cascade.detectMultiScale(gray_frame, 1.2, 5)

            if frame_count % detect_interval == 0 and global_capture_state['capture_count'] < global_capture_state[
                'target_count']:

                if len(faces) == 1:
                    x, y, w, h = faces[0]
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)

                    # 采集时调整尺寸以匹配训练尺寸
                    face_roi = cv.resize(gray_frame[y:y + h, x:x + w], (100, 100))

                    global_capture_state['capture_count'] += 1
                    cv.imwrite(
                        f"{DATASET_PATH}/{global_capture_state['capture_id']}_{global_capture_state['capture_count']}.jpg",
                        face_roi  # 保存调整大小后的灰度图 ROI
                    )

                elif len(faces) > 1:
                    cv.putText(frame, "请确保画面中只有一张人脸!", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),
                               2)

                elif len(faces) == 0:
                    cv.putText(frame, "请将人脸对准摄像头!", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            if global_capture_state['capture_count'] >= global_capture_state['target_count']:
                global_capture_state['is_capturing'] = False
                print(f"人脸采集完成: {global_capture_state['capture_name']}")

            frame_count += 1
            # identified_faces 仅用于识别，采集模式下不使用
            identified_faces = []

            # ----------------------------------------------------
        # ⭐️ 2. 考勤与作答逻辑
        # ----------------------------------------------------
        else:
            identified_faces = []

            # --- A. 人脸识别与考勤 (考勤子系统) ---
            faces = face_cascade.detectMultiScale(gray_frame, 1.2, 5)
            first_identified_name = "未知作答者"

            for (x, y, w, h) in faces:

                # 裁剪并调整尺寸到 LBPH 训练的尺寸 (100x100)
                face_roi = gray_frame[y:y + h, x:x + w]
                try:
                    face_roi_resized = cv.resize(face_roi, (100, 100))
                    student_id, conf = recognizer.predict(face_roi_resized)
                except cv.error:
                    continue

                # 使用 conf < 80 作为识别阈值 (LBPH 距离越小越好，此处 conf 是距离)
                if conf < 80:
                    name = names_map.get(student_id, "未知")
                    log_attendance(student_id, name)
                    label = name
                    color = (0, 255, 0)  # 绿色：已识别
                else:
                    name = "未知"
                    label = f"未知 ({conf:.1f})"
                    color = (0, 0, 255)  # 红色：未识别

                cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv.putText(frame, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                # 记录第一个识别到的学生信息，用于作答关联
                if name != "未知" and not identified_faces:
                    first_identified_name = name

                if name != "未知":
                    identified_faces.append({'rect': (x, y, w, h), 'name': name, 'id': student_id})

            # --- 侧脸检测逻辑已移除 ---

            # --- B. 手势识别与作答 (作答子系统) ---
            lmslist_hands = hand_detector.find_position(frame, handNo=0)
            fingers_count = hand_detector.count_fingers(lmslist_hands)

            # 使用识别到的第一个人脸姓名作为作答者
            answer_name = first_identified_name

            if fingers_count >= 1 and fingers_count <= 5:
                answer_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
                answer_choice = answer_map.get(fingers_count, '?')

                display_text = f"作答: {answer_name} 选 {answer_choice} ({fingers_count} 根手指)"

                # 将作答提示放在右上角
                cv.putText(frame, display_text, (frame.shape[1] - 500, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255),
                           2)

                # 记录作答事件 (节流，每 2 秒记录一次)
                if time.time() - last_answer_log_time > 2:
                    log_answer(answer_name, fingers_count)
                    last_answer_log_time = time.time()
            else:
                # 未作答或手势不明确的提示
                cv.putText(frame, "请伸出 1-5 根手指作答", (frame.shape[1] - 500, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9,
                           (0, 0, 255), 2)

        # --- 3. 编码并返回帧 ---
        ret, buffer = cv.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cam.release()
    cv.destroyAllWindows()


# --- 7. Flask 路由配置 (保持不变) ---

app = Flask(__name__)


@app.route('/')
def index():
    """实时监控页面"""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """实时视频流路由"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/history')
def history():
    """读取并展示考勤和作答记录"""
    attendance_records = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
            attendance_records = list(csv.DictReader(f))

    answer_records = []
    if os.path.exists(ANSWER_LOG_FILE):
        with open(ANSWER_LOG_FILE, "r", encoding="utf-8") as f:
            answer_records = list(csv.DictReader(f))

    return render_template('history.html',
                           attendance_records=attendance_records,
                           answer_records=answer_records)


@app.route('/record', methods=['GET', 'POST'])
def record_page():
    """人脸录制主页面"""
    global global_capture_state

    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return render_template('record.html', error="姓名不能为空", state=global_capture_state)

        if os.path.exists(MAPPING_PATH):
            with open(MAPPING_PATH, 'r', encoding='utf-8') as f:
                names_mapping = json.load(f)
        else:
            names_mapping = {}

        if name in names_mapping:
            return render_template('record.html', error=f"姓名 '{name}' 已存在，请直接训练。", state=global_capture_state)

        # 获取下一个可用的 ID
        current_ids = [v for v in names_mapping.values() if isinstance(v, int)]
        new_id = max(current_ids, default=0) + 1

        names_mapping[name] = new_id
        with open(MAPPING_PATH, 'w', encoding='utf-8') as f:
            json.dump(names_mapping, f, ensure_ascii=False, indent=4)

        global_capture_state.update({
            'is_capturing': True,
            'capture_id': new_id,
            'capture_name': name,
            'capture_count': 0
        })
        print(f"开始录制：Name={name}, ID={new_id}")
        return redirect(url_for('record_page'))

    return render_template('record.html', state=global_capture_state)


@app.route('/train', methods=['POST'])
def train_route():
    """触发模型训练的路由"""
    if global_capture_state['is_capturing']:
        return jsonify({'status': 'error', 'message': '正在采集数据，请完成后再训练！'})

    success = train_model_logic()
    if success:
        global names_map
        names_map = load_mapping()
        return jsonify({'status': 'success', 'message': '模型训练完成！请刷新实时监控页面。'})
    else:
        return jsonify({'status': 'error', 'message': '训练失败，请检查数据集是否为空。'})


@app.route('/status')
def get_status():
    """提供给前端的实时状态接口"""
    return jsonify(global_capture_state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)