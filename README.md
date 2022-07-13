## Mouse Control using Hand Gesture Recognition (v 1.0)
Computer vision is the most mainstream field today. 
Hand Gesture is quite possibly the most development continuous 
Research. MediaPipe is an open-source library created by Google 
to comprehend the essentials of computer vision. 


### Files
- hand.py ---------- > First Python file which detects hand.
- mouse.py ---------> Second python file which use first file and blend with a mouse functionality.   


### Description
Mediapipe is an exceptionally progressed cv library, created by Google.
[ Visit the site for information ](https://google.github.io/mediapipe/solutions/hands.html "Mediapipe Hands"). 
They make use of two main models Palm detection model and the Hand landmarks model. The point of _hand.py_ is to 
distinguish hand(s) in the 3d plane and return its (x, y, z) facilitates. 
Any hand(s) has 21 focuses (0 - 20) as displayed underneath. 
Moreover, _mouse.py_ is the main program that interprets 
the hand from hand.py and enables mouse movement using GUI library Autopy.

The following code finds the hand and its coordinate in 3D plane.
``` python
            or id, h_landmarks in enumerate(h_hand.landmark):
                height, width, channel = image.shape

                c_x, c_y = int(h_landmarks.x * width), int(h_landmarks.y * height)

                x_coordinate.append(c_x)
                y_coordinate.append(c_y)

                self.lmlist.append([id, c_x, c_y])
```
### Installation
(Optional) setup a virtual environment to install necessary packages.
``` commandline
virtualenv .venv
source .venv/bin/activate
```
Install the packages listed in Requirement.txt file
```shell
pip install -r requirements.txt
```
Run Mouse.py to see the final result.

__Note__: Autopy library is only supported on python 3.7 or lower.

### Usage
This program is simple and can be run using command line in system where python is already installed
```shell
Python mouse.py
```
#### Steps:
1. First, run _hands.py_, You will see an external window capturing your video and detecting hands.
2. After a successful run, open mouse.py and run the file. 
3. Now you must point your index finger towards the screen to move the mouse. 
   Any moment if you wish to right-click join your Index and Middle finger. 
4. To quit any time simply press q on your keyboard.

_Remember_ the Port(0) is for an internal webcam and Port(1) for any external webcam. Make sure you have assigned
correct Port in a program at below block.
```python
cam = cv2.VideoCapture(0)  # capture video from inbuilt camera port = 0
#or
cam = cv2.VideoCapture(1)  # capture video from external camera port = 1
```
