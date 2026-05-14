import argparse
import sys
from pathlib import Path

PROJECT_SRC = Path(__file__).resolve().parents[1]
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

try:
    import cv2
    import mediapipe as mp
except ModuleNotFoundError as exc:
    missing_package = "opencv-python" if exc.name == "cv2" else exc.name
    print(
        f"Missing dependency: {exc.name}\n"
        f"Install it with: py -3.12 -m pip install {missing_package}\n"
        "Then run: py -3.12 src\\AI\\main.py -t squat",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

from AI.utils import score_table
from types_of_exercise import TypeOfExercise


EXERCISE_TYPES = ("push-up", "pull-up", "squat", "walk", "sit-up")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--exercise_type",
        choices=EXERCISE_TYPES,
        default="squat",
        help="Type of activity to do",
    )
    parser.add_argument(
        "-vs",
        "--video_source",
        type=str,
        help="Video filename or path. Defaults to the webcam.",
        required=False,
    )
    return vars(parser.parse_args())


args = parse_args()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


if args["video_source"] is not None:
    video_path = Path(args["video_source"])
    if not video_path.exists():
        video_path = Path(__file__).resolve().parent / "videos" / args["video_source"]
    cap = cv2.VideoCapture(str(video_path))
else:
    cap = cv2.VideoCapture(0)  # webcam

if not cap.isOpened():
    source = args["video_source"] or "webcam"
    raise SystemExit(f"Could not open video source: {source}")

cap.set(3, 800)  # width
cap.set(4, 480)  # height

# setup mediapipe
with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    counter = 0  # movement of exercise
    status = True  # state of move
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        # result_screen = np.zeros((250, 400, 3), np.uint8)

        frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
        # recolor frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        # make detection
        results = pose.process(frame)
        # recolor back to BGR
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            counter, status = TypeOfExercise(landmarks).calculate_exercise(
                args["exercise_type"], counter, status)
        except AttributeError:
            pass

        frame = score_table(args["exercise_type"], frame, counter, status)
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255),
                                   thickness=2,
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(174, 139, 45),
                                   thickness=2,
                                   circle_radius=2),
        )

        cv2.imshow('Video', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
