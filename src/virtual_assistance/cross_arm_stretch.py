import cv2
import numpy as np
import time
import PoseModule as pm
import pyttsx3

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
cap.set(cv2.CAP_PROP_FPS, 60)

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
engine.startLoop(False)

detector = pm.poseDetector()
count = 0
dir = 0

last_feedback = None
feedback_cooldown = 2  # Cooldown time in seconds
last_feedback_time = 0

while True:
    success, img = cap.read()

    img = detector.findPose(img, True)
    lmList = detector.findPosition(img, True)

    current_time = time.time()
    feedback = None

    if len(lmList) == 0:
        feedback = "Please position yourself in front of the camera"
    else:
        x1, y1 = lmList[11][1:3]  # Left Shoulder
        x2, y2 = lmList[12][1:3]  # Right Shoulder
        x3, y3 = lmList[14][1:3]  # Right Elbow

        # Retrieve visibility for each point
        visibility1 = lmList[11][3]  
        visibility2 = lmList[12][3]  
        visibility3 = lmList[14][3]  

        # Check if points have sufficient visibility
        if visibility1 < 0.4 or visibility2 < 0.4 or visibility3 < 0.4:
            feedback = "Make sure your right arm is visible"

        if len(lmList) != 0:

            shoulder_diff = abs(y1 - y2)
            if shoulder_diff > 20:  # Threshold for shoulder level difference
                feedback = "Make sure both sides of your shoulder even"

            if abs(y3 - y2) > 50:  # Threshold for elbow height difference
                feedback = "Make sure your right elbow at shoulder height"

            angle = detector.findAngle(img, 11, 12, 14)
            per = np.interp(angle, (10, 100), (0, 100))
            # per = 100 - per
            bar = np.interp(angle, (10, 100), (100, 650))

            # Check by comparing the right elbow position relative to the left shoulder
            if dir == 0:
                if x3 <= x1:  # Right elbow crossed in front of the left shoulder
                    if per == 100:
                        dir = 1
                        count += 0.5
                        feedback = "Great! Now return your right arm to the starting position."
                    else:
                        feedback = "Cross your right arm in front of your body."
                else:
                    feedback = "Cross your right arm in front of your body."
            elif dir == 1:
                if x3 > x2:  # Right elbow returned to the right side
                    if per == 0:
                        dir = 0
                        count += 0.5
                        feedback = "Good job! Now cross your right arm again."
                    else: 
                        feedback = "Bring your right arm back to your side."
                else:
                    feedback = "Bring your right arm back to your side."

            cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (52, 199, 89), 25)

    # Speak feedback if necessary
    if feedback and (feedback != last_feedback or (current_time - last_feedback_time) > feedback_cooldown):
        engine.say(feedback)
        last_feedback = feedback
        last_feedback_time = current_time

    engine.iterate()  # Process the speech queue

    if cv2.waitKey(1) & 0xFF == ord('q'):  # for Mac
        break

    cv2.imshow("Image", img)
    cv2.waitKey(1)

engine.endLoop()
cap.release()
cv2.destroyAllWindows()
