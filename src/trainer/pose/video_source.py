import argparse
from pathlib import Path

import cv2


def parse_video_args(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--source",
        default="0",
        help="Video file path, camera index, or 0 for the default webcam.",
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Process frames without opening an OpenCV preview window.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=0,
        help="Stop after this many frames. Use 0 to process until the video ends.",
    )
    return parser.parse_args()


def open_video_source(source):
    if str(source).isdigit():
        cap = cv2.VideoCapture(int(source), cv2.CAP_DSHOW)
    else:
        path = Path(source)
        cap = cv2.VideoCapture(str(path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    cap.set(cv2.CAP_PROP_FPS, 60)
    return cap


def should_stop_for_key():
    return cv2.waitKey(1) & 0xFF == ord("q")
