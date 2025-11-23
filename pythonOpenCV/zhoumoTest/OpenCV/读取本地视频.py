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