# Kelompok 1
# Peter Ciawi (242401510)
# Luis Levin Halim (242303078)
# Moses Yosafat Immanuel (242401553)


import math
import cv2
import mediapipe as mp
import time
import HandTrackingModule as hd
from directkeys import PressKey, ReleaseKey
from directkeys import UP, DOWN

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 1, 1, 0.5, 0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

detector = hd.handDetector()
upKeyPressed = UP
downKeyPressed = DOWN


validate = True

while validate:
    time.sleep(0.2)
    on_off = input(f"Do you want to start the app (y/n)? ").lower()

    if on_off == "y":
        print("Opening the camera.....")
        validate = False
        while True:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = detector.findHands(img)

            results = hands.process(imgRGB)

            try:
                fingers = detector.getFingers(img)
                print(fingers)
            except Exception as ex:
                print(f'An Exception Occurred: {ex}')

            if hands:
                try:
                    fingerUp = detector.getFingers(img)
                    totalFinger = fingerUp[0] + fingerUp[1] + fingerUp[2] + fingerUp[3] + fingerUp[4]
                    print(fingerUp)
                    cv2.putText(img, f'Finger count: {totalFinger}', (20, 460), cv2.FONT_ITALIC, 1, (100, 55, 255), 2,
                                cv2.LINE_AA)

                except Exception as ex:
                    print(f'An Exception Occurred: {ex}')

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    x1 = 0
                    y1 = 0
                    x2 = 0
                    y2 = 0
                    x3 = 0
                    y3 = 0
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)

                        if id == 8:
                            cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                            x1 = cx
                            y1 = cy

                        if id == 4:
                            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                            x2 = cx
                            y2 = cy

                        if id == 12:
                            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                            x3 = cx
                            y3 = cy

                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                    cv2.line(img, (x2, y2), (x3, y3), (0, 255, 0), 3)

                    lengthUp = math.hypot(x2 - x1, y2 - y1)
                    lengthDown = math.hypot(x3 - x2, y3 - y2)
                    # print(lengthUp)
                    # print(lengthDown)

                    if lengthUp < 25:
                        command = "ON"
                        cv2.putText(img, "Jumping", (420, 460), cv2.FONT_ITALIC, 1, (100, 55, 255), 3)

                        PressKey(upKeyPressed)
                    else:
                        print("")
                        command = "OFF"
                        cv2.putText(img, "Not Jumping", (420, 460), cv2.FONT_ITALIC, 1, (100, 55, 255), 3)

                        ReleaseKey(upKeyPressed)

                    if lengthDown < 25:
                        print("DOWN")
                        cv2.putText(img, "Crouching", (380, 390), cv2.FONT_ITALIC, 1, (100, 55, 255), 3)
                        PressKey(downKeyPressed)
                    else:
                        print("")
                        cv2.putText(img, "Not Crouching", (380, 390), cv2.FONT_ITALIC, 1, (100, 55, 255), 3)
                        ReleaseKey(downKeyPressed)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, f"FPS : {str(int(fps))}", (420, 50), cv2.FONT_ITALIC, 1.5, (0, 255, 0), 4)
            cv2.putText(img, "by : Peter Ciawi", (10,30), cv2.FONT_ITALIC,0.8,(0, 0, 0), 2)
            cv2.putText(img, "     Luis", (10,60), cv2.FONT_ITALIC,0.8,(0, 0, 0), 2)
            cv2.putText(img, "     Moses", (10,90), cv2.FONT_ITALIC,0.8,(0, 0, 0), 2)
            cv2.putText(img, "   (IEE 2024)", (10,120), cv2.FONT_ITALIC,0.8,(0, 0, 0), 2)

            cv2.imshow("Image", img)
            cv2.waitKey(1)

    elif on_off == "n":
        print("Thank you, see you again")
        quit()
    else:
        print("Invalid input, please input again")
        validate = True