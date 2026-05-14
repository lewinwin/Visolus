import cv2
import numpy as np
import time
import PoseModule as pm
from video_source import open_video_source, parse_video_args, should_stop_for_key

def main():
    args = parse_video_args("Run elbow flexion extension pose detection.")
    cap = open_video_source(args.source)

    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0
    frame_count = 0
    while True:
        success, img = cap.read()
        if not success or img is None:
            break

        frame_count += 1
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        if len(lmList) != 0:
            angle = detector.findAngle(img, 12, 14, 16)
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))

            color = (52, 199, 89)
            if per == 100:
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0

            cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                        color, 4)

            cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (52, 199, 89), 25)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if pTime else 0
        pTime = cTime

        if not args.no_display:
            cv2.imshow("Image", img)
            if should_stop_for_key():
                break

        if args.max_frames and frame_count >= args.max_frames:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Processed {frame_count} frame(s). Final count: {int(count)}")


if __name__ == "__main__":
    main()
