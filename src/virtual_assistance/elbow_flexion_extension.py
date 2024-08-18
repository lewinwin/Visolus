import cv2
import numpy as np
import time
import PoseModule as pm
import pyttsx3

cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
cap.set(cv2.CAP_PROP_FPS, 60)

current_step = 0
current_count = 0

engine = pyttsx3.init() 
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
engine.startLoop(False)

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

last_feedback = None
feedback_cooldown = 2  # Cooldown time in seconds
last_feedback_time = 0

while True:
    success, img = cap.read()

    img = detector.findPose(img, True)
    lmList = detector.findPosition(img, True)

    current_time = time.time()
    feedback = None

    # Check pose
    if len(lmList) == 0:
        feedback = "Please position yourself in front of the camera"
    else:
        x1, y1 = lmList[12][1:3]
        x2, y2 = lmList[14][1:3]
        x3, y3 = lmList[16][1:3]

        # Retrieve visibility for each point
        visibility1 = lmList[12][3]
        visibility2 = lmList[14][3]
        visibility3 = lmList[16][3]

        # Check if all points have sufficient visibility
        if visibility1 < 0.4 or visibility2 < 0.4 or visibility3 < 0.4:
            feedback = "Make sure your right arm is visible"
        
        if len(lmList) != 0:
            # Right Arm
            angle = detector.findAngle(img, 12, 14, 16, True)
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))

            color = (52, 199, 89)
            if dir == 0:
                if per == 100:
                    dir = 1
                    count += 0.5
                    feedback = "Great! Now extend your right arm."
                else: 
                    feedback = "Bend your right elbow further."
            
            if dir == 1:
                if per == 0:
                    dir = 0
                    count += 0.5
                    feedback = "Good Job! Now flex your right elbow again."
                else:
                    feedback = "Straighten your right arm more."

            cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                        color, 4)

            # cv2.rectangle(img, (0, 450), (250, 720), (52, 199, 89), cv2.FILLED)
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
