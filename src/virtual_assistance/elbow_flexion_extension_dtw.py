import cv2
import numpy as np
import time
import PoseModule as pm
import pyttsx3
import threading
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def dtw_comparison_thread(landmark_history, reference_landmarks, feedback_callback):
    while True:
        if len(landmark_history) >= 30:  # Check if enough landmarks are collected
            # Flatten landmarks to ensure they are 1-D for DTW
            current_landmarks = np.array([np.array(point).flatten() for frame in landmark_history for point in frame])
            flattened_reference = np.array([np.array(point).flatten() for frame in reference_landmarks for point in frame])

            # Perform DTW comparison
            distance, path = fastdtw(current_landmarks, flattened_reference, dist=euclidean)

            # Determine feedback based on DTW distance
            if distance > 100:  
                feedback = "Try to follow the reference movement more closely."
            else:
                feedback = "Good form!"

            feedback_callback(feedback)

            landmark_history.clear()

        time.sleep(0.1)  

reference_landmarks = np.load('reference_landmarks.npy')  

cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
cap.set(cv2.CAP_PROP_FPS, 60)

engine = pyttsx3.init() 
engine.setProperty('rate', 150)  
engine.setProperty('volume', 1)  

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

last_feedback = None
feedback_cooldown = 2  # Cooldown time in seconds
last_feedback_time = 0
speech_thread = None

landmark_history = []  # Store the history of landmarks for DTW
feedback_lock = threading.Lock()  # Lock to manage feedback safely across threads

# Feedback variable to be accessed by both the DTW and main threads
feedback = None

def update_feedback(new_feedback):
    """Callback to update feedback safely from the DTW thread."""
    global feedback, last_feedback_time
    with feedback_lock:
        feedback = new_feedback
        last_feedback_time = time.time()

# Start DTW comparison in a separate thread
dtw_thread = threading.Thread(target=dtw_comparison_thread, args=(landmark_history, reference_landmarks, update_feedback))
dtw_thread.daemon = True  # Set as a daemon thread to exit when the main program exits
dtw_thread.start()

while True:
    success, img = cap.read()

    img = detector.findPose(img, True)
    lmList = detector.findPosition(img, True)

    current_time = time.time()

    if len(lmList) == 0:
        feedback = "Please position yourself in front of the camera"
    else:
        x1, y1 = lmList[12][1:3]
        x2, y2 = lmList[14][1:3]
        x3, y3 = lmList[16][1:3]

        visibility1 = lmList[12][3]
        visibility2 = lmList[14][3]
        visibility3 = lmList[16][3]

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
            cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

            cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (52, 199, 89), 25)

            # Add current frame's landmarks to history
            landmark_history.append([(x1, y1), (x2, y2), (x3, y3)])

    # Feedback handling
    if feedback and (feedback != last_feedback or (current_time - last_feedback_time) > feedback_cooldown):
        if speech_thread is None or not speech_thread.is_alive():  
            speech_thread = threading.Thread(target=speak, args=(engine, feedback))
            speech_thread.start()
        last_feedback = feedback
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
