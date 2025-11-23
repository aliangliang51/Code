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
