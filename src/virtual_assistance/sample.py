import pyttsx3
from math import fabs
from utils import get_angle, PartsEnum
from PoseModule import poseDetector
import cv2

# class ElbowFlexionExtensionExercise:
#     def __init__(self):
#         self.current_step = 0
#         self.current_count = 0
#         self.engine = pyttsx3.init()  # Initialize the TTS engine

#         # Configure TTS settings
#         self.engine.setProperty('rate', 150)  # Speed of speech
#         self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

#     def speak(self, text):
#         """Function to speak the given text."""
#         self.engine.say(text)
#         self.engine.runAndWait()

        
        
#         def findPose(self, img, draw=True):
#             imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             self.results = self.pose.process(imgRGB)
#             if self.results.pose_landmarks:
#                 if draw:
#                     self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
#                                             self.mpPose.POSE_CONNECTIONS)
#             return img
       
        # angle = detector.findAngle(img, 12, 14, 16)



        # if len(lmList) != 0:
        #     # Right Arm
        #     angle = detector.findAngle(img, 12, 14, 16)

            #angle = detector.findAngle(img, 11, 13, 15,False)
            # per = np.interp(angle, (210, 310), (0, 100))
            # bar = np.interp(angle, (220, 310), (650, 100))
            # print(angle, per)



# import cv2
# import mediapipe as mp

# # Initialize MediaPipe Pose
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()

# # Initialize video capture (or use an image)
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert the BGR frame to RGB
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Process the image to detect pose landmarks
#     results = pose.process(image)

#     # Check if landmarks are detected
#     if results.pose_landmarks:
#         # Iterate over specific landmarks (e.g., shoulder, elbow, wrist)
#         for landmark in [mp_pose.PoseLandmark.LEFT_SHOULDER, 
#                          mp_pose.PoseLandmark.LEFT_ELBOW, 
#                          mp_pose.PoseLandmark.LEFT_WRIST]:
#             # Get the specific landmark
#             landmark_data = results.pose_landmarks.landmark[landmark]

#             # Extract visibility
#             visibility = landmark_data.visibility

#             # Check visibility
#             if visibility > 0.5:  # Example threshold
#                 print(f"{landmark.name} is visible with visibility {visibility:.2f}")
#             else:
#                 print(f"{landmark.name} is not sufficiently visible")

#     # Display the frame
#     cv2.imshow('MediaPipe Pose', frame)

#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

    # def perform_exercise(self, joints):
    #     if not joints or len(joints) == 0:
    #         feedback = "Please position yourself in front of the camera"
    #         self.speak(feedback)
    #         return {"currentCount": self.current_count, "feedback": feedback}

    #     right_shoulder = joints[PartsEnum.right_shoulder]
    #     right_elbow = joints[PartsEnum.right_elbow]
    #     right_wrist = joints[PartsEnum.right_wrist]

    #     angle = fabs(get_angle(right_shoulder, right_elbow, right_wrist))


    #     if any(item.visibility < 0.2 for item in [right_shoulder, right_elbow, right_wrist]):
    #         feedback = "Make sure limbs are visible"
    #         self.speak(feedback)
    #         return {"currentCount": self.current_count, "feedback": feedback}

    #     print(angle)

    #     if self.current_step == 0:
    #         if angle < 60:  # Flexion phase (angle decreases)
    #             self.current_step = 1
    #             self.current_count += 1
    #             feedback = "Great! Now extend your arm."
    #             self.speak(feedback)
    #             return {"currentCount": self.current_count, "feedback": feedback}
    #         else:
    #             feedback = "Bend your elbow further."
    #             self.speak(feedback)
    #             return {"currentCount": self.current_count, "feedback": feedback}
    #     elif self.current_step == 1:
    #         if angle > 150:  # Extension phase (angle increases)
    #             self.current_step = 0
    #             feedback = "Good Job! Now flex your elbow again."
    #             self.speak(feedback)
    #             return {"currentCount": self.current_count, "feedback": feedback}
    #         else:
    #             feedback = "Straighten your arm more."
    #             self.speak(feedback)
    #             return {"currentCount": self.current_count, "feedback": feedback}



# import cv2
# import numpy as np
# import time
# import PoseModule as pm
# import pyttsx3
# from PoseModule import poseDetector
# import threading
# # from AI.utils import *

# cap = cv2.VideoCapture(0) 
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
# cap.set(cv2.CAP_PROP_FPS, 60)

# current_step = 0
# current_count = 0

# engine = pyttsx3.init() 
# engine.setProperty('rate', 150)  # Speed of speech
# engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
# engine.startLoop(False)


# # def threaded_speak(text):
# #     t = threading.Thread(target=speak, args=(text,))
# #     t.start()

# detector = pm.poseDetector()
# count = 0
# dir = 0
# pTime = 0

# while True:
#     success, img = cap.read()

#     img = detector.findPose(img, True)
#     lmList = detector.findPosition(img, False)

#     # Check pose
#     # if len(lmList) == 0:
#     #     feedback = "Please position yourself in front of the camera"
#     #     tts = _TTS()
#     #     tts.start(feedback)
#     #     del(tts)

#     x1, y1 = lmList[12][1:3]
#     x2, y2 = lmList[14][1:3]
#     x3, y3 = lmList[16][1:3]

#     # Retrieve visibility for each point
#     visibility1 = lmList[12][3]
#     visibility2 = lmList[14][3]
#     visibility3 = lmList[16][3]

#     # Check if all points have sufficient visibility
#     if visibility1 < 0.4 or visibility2 < 0.4 or visibility3 < 0.4:
#         feedback = "Make sure limbs are visible"
#         engine.say(feedback)

#     if len(lmList) != 0:
#         # Right Arm
#         angle = detector.findAngle(img, 12, 14, 16)
#         #angle = detector.findAngle(img, 11, 13, 15,False)
#         per = np.interp(angle, (210, 310), (0, 100))
#         bar = np.interp(angle, (220, 310), (650, 100))

#         color = (52, 199, 89)
#         if dir == 0:
#             if per == 100:
#                 dir = 1
#                 count += 0.5
#                 feedback = "Great! Now extend your right arm."
#             else: 
#                 feedback = "Bend your right elbow further."
#             engine.say(feedback)


#         if dir == 1:
#             if per == 0:
#                 dir = 0
#                 count += 0.5
#                 feedback = "Good Job! Now flex your right elbow again."
#             else:
#                 feedback = "Straighten your right arm more."
#             engine.say(feedback)
    
#     engine.iterate()
      
# #        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
# #        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
# #        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
# #                    color, 4)

#         # cv2.rectangle(img, (0, 450), (250, 720), (52, 199, 89), cv2.FILLED)
# #        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (52, 199, 89), 25)

#     # cTime = time.time()
#     # fps = 1 / (cTime - pTime)
#     # pTime = cTime
#     # cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
#     #             (255, 0, 0), 5)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'): #for my mac
#         break

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

# engine.endLoop()