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
