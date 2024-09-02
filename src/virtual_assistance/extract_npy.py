import cv2
import numpy as np
import PoseModule as pm  

detector = pm.poseDetector()

cap = cv2.VideoCapture('Visolus/src/virtual_assistance/Active Elbow Flexion & Extension.mp4')  

reference_landmarks = [] 

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
    
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        frame_landmarks = [(lmList[12][1:3]), (lmList[14][1:3]), (lmList[16][1:3])]
        reference_landmarks.append(frame_landmarks)
    
    cv2.imshow("Reference Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Convert the list to a NumPy array
reference_landmarks = np.array(reference_landmarks)

# Save the landmarks to a file
np.save('reference_landmarks.npy', reference_landmarks)
