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
