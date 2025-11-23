import cv2 as cv
import numpy as np

from RK3568手势识别.handutil import HandDetector


def main():
    cap = cv.VideoCapture(0)
    detector = HandDetector()

    finger_img_list = [
        'fingers/0.png',
        'fingers/1.png',
        'fingers/2.png',
        'fingers/3.png',
        'fingers/4.png',
        'fingers/5.png',
    ]
    finger_list = []
    for fi in finger_img_list:
        i = cv.imread(fi)
        finger_list.append(i)

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        if success:
            img = detector.find_hands(img)
            lmslist = detector.find_position(img)
            tip_ids = [4, 8, 12, 16, 20]


            if len(lmslist) > 0:
                # print('lmslist:', lmslist)
                # print('lmslist.shape:', np.array(lmslist).shape)
                fingers = []
                for tid in tip_ids:
                    x,y = lmslist[tid][1], lmslist[tid][2]
                    cv.circle(img, (x,y), 10, (0,255,0), cv.FILLED)
                    if tid == 4:
                        # 根据食指和中指的位置判断左手右手
                        if lmslist[8][1] < lmslist[12][1]:
                            # 右手
                            if lmslist[tid][1] < lmslist[tid - 1][1]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                        else:
                            # 左手
                            if lmslist[tid][1] > lmslist[tid - 1][1]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                        # 如果是其他手指，如果这些手指的指尖的y位置大于第二关节的位置，则认为这个手指打开，否则认为这个手指关闭
                    else:
                        if lmslist[tid][2] < lmslist[tid - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                        # fingers是这样一个列表，5个数据，0代表一个手指关闭，1代表一个手指打开
                        # 判断有几个手指打开
                    cnt = fingers.count(1)
                    # print('cnt:', cnt)

                    # 找到对应的手势图片并显示
                    finger_img = finger_list[cnt]
                    w, h, c = finger_img.shape
                    img[0:w, 0:h] = finger_img



            cv.imshow("Image", img)

        k = cv.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
