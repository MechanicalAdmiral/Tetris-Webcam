import cv2
import time
import numpy as np
import math
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture("http://192.168.1.2:4747/video?640x480")

ret, frame = cap.read()

previous_frame = frame

frame = cv2.flip(frame, 1)

movecount = 0
ismoving = 0
movetimeout = 5
lastmove = [2, 2]

def playtetris(bigf):
    match(bigf):
        case [0, 0]:
            print("Tetris rotate")
            keyboard.press("z")
            keyboard.release("z")
        case [0, 1]:
            print("Tetris to right")
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        case [1, 0]:
            print("Tetris to left")
            keyboard.press(Key.left)
            keyboard.release(Key.left)
        case [1, 1]:
            print("Tetris down right now")
            keyboard.press(Key.down)
            keyboard.release(Key.down)
        case _:
            print("No function")

def dividetotwo(framey):
    height = framey.shape[0]
    width = framey.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    left1 = framey[:, :width_cutoff]
    right1 = framey[:, width_cutoff:]
    return [left1, right1]

print("done")

while True:
    # Capture the next frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imshow("real", frame)
    for i in range(len(dividetotwo(frame))):

        diff = cv2.absdiff(dividetotwo(frame)[i], dividetotwo(previous_frame)[i])

        # Threshold the difference image to only keep pixels that have changed by more than a certain amount
        threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        # Calculate the average intensity of the changed pixels
        mean = cv2.mean(threshold)[0]

        # If the average intensity is above a certain threshold, consider it significant motion
        if mean > 40:
            significant_motion = True
            movecount += 1
            movetimeout = 5
            if not ismoving:
                ismoving = 1
                print("Move started.",i)
                lastmove[0] = i
            # print("Moved: ", movecount, " ", mean)
        else:
            if movetimeout == 0:
                if ismoving:
                    print("Move ended.", i)
                    lastmove[1] = i
                    playtetris(lastmove)
                    ismoving = 0
                movecount = 0
            else:
                movetimeout -= 1
            significant_motion = False
    if cv2.waitKey(1) == 27: 
            break  # esc to quit
    previous_frame = frame
cv2.destroyAllWindows()