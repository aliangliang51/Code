# 📁 代码项目摘要：OpenCV

## 文件: `demo1.py`

```python
import cv2

def face_detect(img):
    if img is None:
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")


    faces = faceCascade.detectMultiScale(gray, 1.15)
    print(faces)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("faces",img)


video = cv2.VideoCapture('videos/t3.mp4')
while True:
    retval, image = video.read()
    if not retval:
        break
    face_detect(image)
    key = cv2.waitKey(1)
    if key == 27:
        break
video.release()
cv2.destroyAllWindows()

```

---

## 文件: `plate_number.py`

```python
import cv2

img = cv2.imread("images/plate.jpg")
# 加载识别眼睛的级联分类器
faceCascade = cv2.CascadeClassifier("data/haarcascade_russian_plate_number.xml")
# 识别出图像所有眼睛，一一定比例缩放显示
plate_number = faceCascade.detectMultiScale(img, 1.5,minNeighbors=50)
# 遍历所有眼睛
for (x, y, w, h) in plate_number:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 显示图片
cv2.imshow('img1', img)

cv2.waitKey()

cv2.destroyAllWindows()

```

---

## 文件: `摄像头检测人脸.py`

```python
import cv2

def face_detect(img):

    frame = cv2.flip(img,1) # 翻转，照镜子
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(gray,1.15)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow("faces",img)

video = cv2.VideoCapture(0)
while True:
    retval, image = video.read()
    if not retval:
        break
    face_detect(image)
    key = cv2.waitKey(1)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()
```

---

## 文件: `检测图片人脸.py`

```python
import cv2

img = cv2.imread("images/test.jpg")
# 将图片转换成灰度图
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 加载识别人脸的级联分类器
faceCascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")

faces = faceCascade.detectMultiScale(grey, 1.15)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('ima1', img)

cv2.waitKey()

cv2.destroyAllWindows()

```

---

## 文件: `检测图片侧脸.py`

```python
import cv2

img = cv2.imread("images/profileface.jpg")
# 将图片转换成灰度图
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 加载识别人脸的级联分类器
faceCascade = cv2.CascadeClassifier("data/haarcascade_profileface.xml")

faces = faceCascade.detectMultiScale(grey, 1.15)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('ima1', img)

cv2.waitKey()

cv2.destroyAllWindows()

```

---

## 文件: `检测图片眼睛.py`

```python
import cv2

img = cv2.imread("images/eye.jpg")

faceCascade = cv2.CascadeClassifier("data/haarcascade_eye.xml")

eyes = faceCascade.detectMultiScale(img,scaleFactor=1.15,minNeighbors=50)

for (x,y,w,h) in eyes:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("eyes",img)

cv2.waitKey()

cv2.destroyAllWindows()


```

---

## 文件: `检测图片身体.py`

```python
import cv2

img =cv2.imread("images/body.jpg")

faceCascade = cv2.CascadeClassifier("data/haarcascade_fullbody.xml")

body = faceCascade.detectMultiScale(img,1.15)

for (x,y,w,h) in body:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("body",img)
cv2.waitKey()
cv2.destroyAllWindows()
```

---

## 文件: `检测行人.py`

```python
import cv2
import numpy as np

# 初始化视频捕捉对象，用于读取视频文件
camera = cv2.VideoCapture('videos/vtest.avi')
# 创建一个椭圆结构的元素，用于形态学操作
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
# 创建一个5x5的矩阵，用于图像处理中的膨胀或腐蚀操作
kernel = np.ones((5, 5), np.uint8)
# 初始化背景变量，开始时为None
background = None

while True:
    # 读取视频的下一帧
    ret, frame = camera.read()
    # 如果正确读取帧，ret为True，否则为False，表示视频结束或读取出错
    if not ret:
        break  # 如果没有帧可以读取，退出循环
    # 如果背景还未初始化，则使用第一帧作为背景
    if background is None:
        # 将当前帧转换为灰度图像
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 对背景进行高斯模糊处理，以减少图像噪声
        background = cv2.GaussianBlur(background, (21, 21), 0)
        continue  # 继续下一次循环，直到读取到第一帧

    # 将当前帧转换为灰度图像
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 对当前帧进行高斯模糊处理，以减少图像噪声
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    # 计算当前帧与背景的差分图，以识别移动物体
    diff = cv2.absdiff(background, gray_frame)
    # 应用阈值化，将差分图转换为二值图像，便于轮廓检测
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    # 对二值图像进行膨胀操作，填补物体内部的空洞
    diff = cv2.dilate(diff, es, iterations=2)
    # 在膨胀后的图像中查找轮廓
    cnts, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 遍历所有检测到的轮廓
    for c in cnts:
        # 如果轮廓面积小于1500像素，则忽略它，可能是噪声
        if cv2.contourArea(c) < 1500:
            continue
        # 计算轮廓的边界框
        (x, y, w, h) = cv2.boundingRect(c)
        # 在原始帧上绘制矩形框，标记出移动物体的位置
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
    # 显示结果帧
    cv2.imshow("contours", frame)
    # 按'q'键退出
    if cv2.waitKey(30) & 0xff == ord("q"):
        break

# 释放窗口，关闭程序
cv2.destroyAllWindows()
# 释放视频捕捉对象
camera.release()

```

---

## 文件: `检测视频人脸.py`

```python
import cv2


def face_demo(img):
    if img is None:
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(gray, 1.15)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("faces", img)

video = cv2.VideoCapture("videos/video1.mp4")
while True:
    retval, image = video.read()
    if not retval:
        break
    face_demo(image)
    key = cv2.waitKey(1)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()

```

---

## 文件: `检测车辆.py`

```python

import cv2

# 使用KNN算法创建背景减除对象，detectShadows=True表示检测阴影
bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
# 初始化视频捕捉对象，用于读取视频文件
camera = cv2.VideoCapture('videos/traffic.flv')

# 循环直到视频结束或用户退出
while True:
    # 读取视频的下一帧
    ret, frame = camera.read()
    # 如果ret为False，表示视频结束或读取出错，退出循环
    if not ret:
        break
    # 使用背景减除算法处理当前帧，得到前景掩模
    fgmask = bs.apply(frame)
    # 对前景掩模应用阈值化，得到二值图像，244是阈值
    th = cv2.threshold(fgmask, 244, 255, cv2.THRESH_BINARY)[1]
    # 创建一个椭圆形态的结构元素
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3))
    # 对二值图像进行膨胀操作，增强前景物体的轮廓
    dilated = cv2.dilate(th, element, iterations=2)
    # 在膨胀后的图像中查找所有轮廓
    contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历所有检测到的轮廓
    for c in contours:
        # 如果轮廓的面积大于1000像素，认为是有效的物体
        if cv2.contourArea(c) > 1000:
            # 计算轮廓的边界框
            (x, y, w, h) = cv2.boundingRect(c)
            # 在原始帧上绘制矩形框，标记出前景物体的位置
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
    # 显示处理后的视频帧
    cv2.imshow('video', frame)
    # 按'q'键退出循环
    if cv2.waitKey(30) & 0xff == ord('q'):
        break

# 释放视频捕捉对象
camera.release()
# 销毁所有OpenCV窗口
cv2.destroyAllWindows()
```

---

## 文件: `读取本地视频.py`

```python
import cv2

# 打开视频文件
video = cv2.VideoCapture("videos/video1.mp4")
# 在无线循环中，读取视频帧
while True:

    ret , frame = video.read()
    if ret == True:

        cv2.imshow("frame",frame)

    else:
        break
    # 等待100毫秒
    key = cv2.waitKey(100)
    # ESC键按下时退出循环
    if key == 27:
        break
# 释放资源
video.release()
cv2.destroyAllWindows()
```

---

