import cv2
import numpy as np
import time
import PoseModule as pm
import matplotlib.pyplot as plt
from video_source import open_video_source, parse_video_args, should_stop_for_key

def video_processing(source="0", no_display=False, max_frames=0):
    cap = open_video_source(source)

    # Initialize the pose detector
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0

    # Lists to store coordinates
    joint_coords_1 = []
    joint_coords_2 = []
    joint_coords_3 = []
    frame_count = 0

    while True:
        success, img = cap.read()
        if not success or img is None:
            break

        frame_count += 1
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        if len(lmList) != 0:
            # Example joints: 11 (left shoulder), 23 (left hip), 25 (left knee)
            joint_coords_1.append((lmList[11][1], lmList[11][2]))
            joint_coords_2.append((lmList[23][1], lmList[23][2]))
            joint_coords_3.append((lmList[25][1], lmList[25][2]))

            # Visualization
            cv2.circle(img, (lmList[11][1], lmList[11][2]), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (lmList[23][1], lmList[23][2]), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (lmList[25][1], lmList[25][2]), 15, (0, 255, 0), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        if not no_display:
            cv2.imshow("Image", img)
            if should_stop_for_key():
                break

        if max_frames and frame_count >= max_frames:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Processed {frame_count} frame(s).")

    return joint_coords_1, joint_coords_2, joint_coords_3

def plot_joint_coords(joint_coords_1, joint_coords_2, joint_coords_3):
    if not joint_coords_1 or not joint_coords_2 or not joint_coords_3:
        print("No pose landmarks were detected, so there is nothing to plot.")
        return

    plt.figure(figsize=(10, 5))

    # Plot joint 1
    plt.subplot(1, 3, 1)
    joint_coords_1 = np.array(joint_coords_1)
    plt.plot(joint_coords_1[:, 0], joint_coords_1[:, 1], label='Joint 1')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Joint 1')

    # Plot joint 2
    plt.subplot(1, 3, 2)
    joint_coords_2 = np.array(joint_coords_2)
    plt.plot(joint_coords_2[:, 0], joint_coords_2[:, 1], label='Joint 2')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Joint 2')

    # Plot joint 3
    plt.subplot(1, 3, 3)
    joint_coords_3 = np.array(joint_coords_3)
    plt.plot(joint_coords_3[:, 0], joint_coords_3[:, 1], label='Joint 3')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Joint 3')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    args = parse_video_args("Run scaption with dumbbells pose detection.")
    joint_coords_1, joint_coords_2, joint_coords_3 = video_processing(
        source=args.source,
        no_display=args.no_display,
        max_frames=args.max_frames,
    )
    if not args.no_display:
        plot_joint_coords(joint_coords_1, joint_coords_2, joint_coords_3)
