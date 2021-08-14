"""    REFERENCE
Murtaza's Workshop - Robotics and AI
Date 08/11/2021 (mm/dd/yy)
https://www.computervision.zone/courses/hand-tracking/
"""

# This is the Second Program allows us to control the mouse. Therefore, We import autopy, MediaPipe and Opencv.
import cv2
import autopy  # GUI library used for controlling mouse.
import numpy as np
import time
import hand as hg  # Importing first program hands.py as hgq

# Defining the frame size. This is the best chosen frame size after 163 sample run. Remember: Frame size is inversely
# proportional to the Frame Rate. The smaller the Frame Size, the better the frame rate.
width, height = 330, 230

smoothning = 7  # Threshold mouse cursor smoothing value. This value shows best result after 163 sample run
frame_rate = 50
previous_time = 0

c_X, c_Y = 0, 0
p_X, p_Y = 0, 0

""""" Read image from camera at port 0 which is internal webcam
    in case you are using external webcam, use port 1"""""
cam = cv2.VideoCapture(0)  # capture video from inbuilt camera port = 0
cam.set(3, width)
cam.set(4, height)

detect = hg.detectHands(maxHands=1)  # defining the maximum number of hand(s) we need.

# Passing monitor size to autopy library
w_screen, h_screen = autopy.screen.size()

while True:

    frame, image = cam.read()

    image = detect.locateHands(image)

    lmlist, bbox = detect.findLandmarkPos(image)

    if len(lmlist) != 0:
        p1, q1 = lmlist[8][1:]  # value 8 is Middle Finger Tip
        p2, q2 = lmlist[12][1:]  # value 12 is Index Finger Tip

    fingers = detect.locateFinger()

    cv2.rectangle(image, (frame_rate, frame_rate), (width - frame_rate, height - frame_rate), (255, 0, 255), 2)

    if len(fingers) != 0:
        # If index finger is pointing,then enable mouse hover function.
        if fingers[1] == 1 and fingers[2] == 0:
            p3 = np.interp(p1, (frame_rate, width - frame_rate), (0, w_screen))
            q3 = np.interp(q1, (frame_rate, height - frame_rate), (0, h_screen))
            # applying smoothing
            c_X = p_X + (p3 - p_X) / smoothning
            c_Y = p_Y + (q3 - p_Y) / smoothning
            autopy.mouse.move(w_screen - c_X, c_Y)  # Moving mouse in fingers direction.
            cv2.circle(image, (p1, q1), 7, (255, 0, 255), cv2.FILLED)
            p_X, p_Y = c_X, c_Y
        # if Index and Middle finger are up, Enable click function and wait till they join.
        if fingers[1] == 1 and fingers[0] == 1:
            # Calculate the distance and see id its below threshold which is 18. This value is accurate and defined
            # after 163 samples
            length, image, lineInf = detect.calculateDistance(8, 12, image)

            if length < 18:
                cv2.circle(image, (lineInf[4], lineInf[5]), 7, (0, 255, 0), cv2.FILLED)
                #  Unable Click.
                autopy.mouse.click()
    # To display Frames Per Second - FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    cv2.putText(image, str(int(fps)), (30, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow('HandCapture', image)

    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

cam.release()
