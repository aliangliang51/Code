import cv2

img =cv2.imread("images/body.jpg")

faceCascade = cv2.CascadeClassifier("data/haarcascade_fullbody.xml")

body = faceCascade.detectMultiScale(img,1.15)

for (x,y,w,h) in body:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("body",img)
cv2.waitKey()
cv2.destroyAllWindows()