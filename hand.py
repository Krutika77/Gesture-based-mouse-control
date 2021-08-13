"""    REFERENCE
Murtaza's Workshop - Robotics and AI
Date 08/11/2021 (mm/dd/yy)
https://www.computervision.zone/courses/hand-tracking/
"""

# This is the First Program Which detects hand using MediaPipe. Therefore, We import MediaPipe and Opencv.
import cv2
import time
import mediapipe as mp
import numpy as np


# detectHands function is the first function to run and its aim is to detect the hand(s) in the frame.
class detectHands:
    # MediaPipe takes Several default parameter such as:
    # imgMode --> image mode(bool),
    # maxHands--> Maximum number of hand you want to detect (integer).
    # detection_conf = Detection confidence percentage (Floating value (0.1 to 1))
    # tracking_conf = tracking confidence percentage (Floating value (0.1 to 1))
    def __init__(self, imgMode=False, maxHands=1, detection_conf=0.5, tracking_conf=0.5):

        self.imgMode = imgMode
        self.maxHands = maxHands
        self.tracking_conf = tracking_conf
        self.detection_conf = detection_conf

        self.mediapipe_hands = mp.solutions.hands
        # Recognize hands using Hands(STATIC_IMAGE_MODE, MAX_NUM_HANDS, MIN_DETECTION_CONFIDENCE,
        # MIN_TRACKING_CONFIDENCE) function
        self.hand_recog = self.mediapipe_hands.Hands(self.imgMode, self.maxHands, self.detection_conf,
                                                     self.tracking_conf)
        self.mediapipe_draw = mp.solutions.drawing_utils
        # All the fINGER-TIPS id to process.
        self.tipId = [4, 8, 12, 16, 20]

    # locateHands locates the hand and draw all the points and connects them using draw_landmarks.
    def locateHands(self, img, draw=True):

        # Convert to RGB as Hands() function only works on RGB images
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hand_recog.process(img_rgb)

        # Display hand landmarks using mediapipe draw_landmarks function
        if self.results.multi_hand_landmarks:
            for i in self.results.multi_hand_landmarks:

                # Draw hand landmarks with hand coordinate connections
                if draw:
                    self.mediapipe_draw.draw_landmarks(img, i, self.mediapipe_hands.HAND_CONNECTIONS)

        return img

    # FindLandmarkPos function returns the X, Y coordinate in 3D plane for each id ( all the point labeled between 0-20)
    def findLandmarkPos(self, image, hand_number=0, draw=True):

        x_coordinate = []
        y_coordinate = []
        bbox = []
        self.lmlist = []

        if self.results.multi_hand_landmarks:
            h_hand = self.results.multi_hand_landmarks[hand_number]
            # finding X,Y coordinate value for each points in hand.
            for id, h_landmarks in enumerate(h_hand.landmark):
                height, width, channel = image.shape

                c_x, c_y = int(h_landmarks.x * width), int(h_landmarks.y * height)

                x_coordinate.append(c_x)
                y_coordinate.append(c_y)

                self.lmlist.append([id, c_x, c_y])

                if draw:
                    cv2.circle(image, (c_x, c_y), 5, (0, 255, 255), cv2.FILLED)

            x_minimum, x_maximum = min(x_coordinate), max(x_coordinate)
            y_minimum, y_maximum = min(y_coordinate), max(y_coordinate)
            # Drawing bounding box around the hand.
            bbox = x_minimum, y_minimum, x_maximum, y_maximum

            if draw:
                cv2.rectangle(image, (x_minimum - 20, y_minimum - 20), (x_maximum + 20, y_maximum + 20), (255, 0, 0), 2)

        return self.lmlist, bbox

    # locateFinger function is used to locate each individual finger in 3D plane.
    def locateFinger(self):

        check_finger = []
        if len(self.lmlist) != 0:
            if self.lmlist[self.tipId[0]] > self.lmlist[self.tipId[0] - 1]:
                check_finger.append(1)
            else:
                check_finger.append(0)
        # finding all the 5 fingers in 3D plane and appending in check_finger
        for id in range(1, 5):

            if len(self.lmlist) != 0:
                if self.lmlist[self.tipId[id]][2] < self.lmlist[self.tipId[id] - 2][2]:
                    check_finger.append(1)
                else:
                    check_finger.append(0)

        return check_finger

    # Calculating euclidean distance between any 2 fingers.
    def calculateDistance(self, point_1, point_2, image, draw=True, radius=8, thickness=3):

        p1, q1 = self.lmlist[point_1][1:]  # first finger Tip
        p2, q2 = self.lmlist[point_2][1:]  # second finger Tip

        c_x, c_y = (p1 + p2) // 2, (q1 + q2) // 2  # finding centre of both the fingers
        # Drawing the circle on selected fingers and their centre, also connecting them with a line.
        if draw:
            cv2.circle(image, (p1, q1), radius, (0, 255, 255), cv2.FILLED)
            cv2.circle(image, (p2, q2), radius, (0, 255, 255), cv2.FILLED)
            cv2.circle(image, (c_x, c_y), radius, (0, 0, 255), cv2.FILLED)
            cv2.line(image, (p1, q1), (p2, q2), (255, 0, 255), thickness)

            array1 = np.array((p1, q1))
            array2 = np.array((p2, q2))

            length = np.linalg.norm(array1 - array2)

            return length, image, [p1, q1, p2, q2, c_x, c_y]


# The main function
def main():
    previous_time = 0
    """"" Read image from camera at port 0 which is internal webcam
    in case you are using external webcam, use port 1"""""
    cam = cv2.VideoCapture(0)  # using laptops internal webcam port=0
    detect_Hands = detectHands()

    while True:
        frame, img = cam.read()
        img = detect_Hands.locateHands(img)
        lmlist, bbox = detect_Hands.findLandmarkPos(img)

        # To display Frames Per Second - FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(img, str(int(fps)), (30, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow('HandCapture', img)
        # To exit from program anytime press q on keyboard.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()


if __name__ == "__main__":
    main()
