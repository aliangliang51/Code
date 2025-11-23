import cv2 as cv
import numpy as np
from PIL import Image
import os
import json


dataset_path = 'dataset'
trainer_path = 'trainer'
names_mapping_path = 'names_mapping.json'


def main():
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    if not os.path.exists(trainer_path):
        os.makedirs(trainer_path)

    while True:
        print("请选择一个操作：")
        print("1. 数据采集")
        print("2. 训练模型")
        print("3. 实时识别")
        print("4. 退出")
        choice = input("请输入您的选择：")
        if choice == '1':
            face_id = input_names()
            capture_faces(face_id)
        elif choice == '2':
            train_model()
        elif choice == '3':
            recognize_faces()
        elif choice == '4':
            break
        else:
            print("无效的选择，请重新输入。")


def input_names():
    if os.path.exists(names_mapping_path):
        with open(names_mapping_path, 'r') as f:
            names_mapping = json.load(f)
    else:
        names_mapping = {}

    new_id = max(names_mapping.values(), default=0) + 1
    name = input(f"请入输入名字（ID 将自动分配）{new_id}:")
    names_mapping[name] = new_id

    with open(names_mapping_path, 'w') as f:
        json.dump(names_mapping, f)

    return new_id


def capture_faces(face_id):
    """
    :param face_id: 人脸ID
    :return:
    """

    cam = cv.VideoCapture(0)

    # cam = cv.VideoCapture(2)
    if not cam.isOpened():
        print("无法打开摄像头")
        return

    cam.set(3, 640)
    cam.set(4, 480)

    face_detetor = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    print("\n 正在初始化人脸捕捉，看摄像头并等待")

    count = 0
    detect_interval = 5
    frame_count = 0

    while True:
        ret, img = cam.read()
        if not ret:
            print("无法获取图像")
            break

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        if frame_count % detect_interval == 0:
            faces = face_detetor.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                cv.imwrite(f"{dataset_path}/{face_id}_{count}.jpg", gray[y:y + h, x:x + w])

                if count >= 10:
                    break
        cv.imshow("image", img)
        frame_count += 1
        k = cv.waitKey(1) & 0xff
        if k == ord('q') or count >= 10:
            break
    cam.release()
    cv.destroyAllWindows()


def train_model():
    """
    训练人脸并保存
    :return:
    """
    recognizer = cv.face.LBPHFaceRecognizer_create()
    detector = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

    def getImagesAndLabels(path):
        """
        :param path:
        :return:
        """

        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split("_")[0])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids

    print("正在训练人脸识别模型训练中...")
    faces, ids = getImagesAndLabels(dataset_path)
    recognizer.train(faces, np.array(ids))

    recognizer.write('trainer/trainer.yml')


def recognize_faces():
    """
    RK3568人脸识别
    :return:
    """

    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = 'haarcascade_frontalface_default.xml'
    faceCascade = cv.CascadeClassifier(cascadePath)
    font = cv.FONT_HERSHEY_SIMPLEX

    if os.path.exists(names_mapping_path):
        with open(names_mapping_path, 'r') as f:
            names_mapping = json.load(f)
            names = {v: k for k, v in names_mapping.items()}
    else:
        print("未找到人脸映射文件")
        return

    cam = cv.VideoCapture(0)

    # cam = cv.VideoCapture(2)

    if not cam.isOpened():
        print("无法打开摄像头")
        return

    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        if not ret:
            print("无法获取图像")
            break

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 100:
                name = names.get(id, "未知")

            else:
                name = "未知"

            cv.putText(img, name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)

            k = cv.waitKey(1) & 0xff
            if k == ord('q'):
                break

        cv.imshow("image", img)
    cam.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
