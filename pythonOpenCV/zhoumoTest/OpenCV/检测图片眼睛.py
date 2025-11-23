import cv2

img = cv2.imread("images/eye.jpg")

faceCascade = cv2.CascadeClassifier("data/haarcascade_eye.xml")

eyes = faceCascade.detectMultiScale(img,scaleFactor=1.15,minNeighbors=50)

for (x,y,w,h) in eyes:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("eyes",img)

cv2.waitKey()

cv2.destroyAllWindows()

