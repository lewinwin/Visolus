# Visolus Project Documentation

Visolus is a computer-vision physical therapy and exercise-monitoring project. It uses a camera to detect human body landmarks, calculate joint angles, count repetitions, and give visual or voice feedback during rehabilitation-style movements.

The name combines the idea of vision-based tracking with health and well-being. The main project idea is described in `README.md`; this file explains how the repository is structured and how the code works.

## Project Purpose

The project explores how computer vision can support physical therapy by:

- Detecting body landmarks in real time from a webcam or video.
- Calculating angles at joints such as elbows, knees, hips, shoulders, and abdomen.
- Counting repetitions for exercises.
- Giving feedback when a movement is incomplete or the body is not visible.
- Comparing a user movement against a reference movement using Dynamic Time Warping, or DTW.
- Testing voice output with `pyttsx3`.
- Exporting pose landmark data for experimental 3D visualization in Unity.

## Technology Stack

Core stack:

- Python: main programming language for pose detection and exercise logic.
- OpenCV (`opencv-python`): camera/video capture, image processing, drawing overlays, and display windows.
- MediaPipe: body pose landmark detection with the Pose/BlazePose model.
- NumPy: angle interpolation, arrays, and numeric processing.
- Pandas: landmark table generation in the generic AI module.
- cvzone: simplified pose helpers used in experimental MediaPipe and 3D motion capture scripts.
- pyttsx3: offline text-to-speech feedback.
- fastdtw and SciPy: Dynamic Time Warping comparison between movement sequences.
- Matplotlib and Pillow: plotting, pose classification visualization, and image rendering in the Google Colab workflow.
- C# and Unity: experimental playback of exported landmark animation data.

Dependencies are listed in `requirements.txt`.

## Repository Layout

```text
Visolus/
  README.md
  PROJECT_DOCUMENTATION.md
  requirements.txt
  assets/
  IMAGE_FILES/
  VIDEO_FILES/
  src/
    AI/
    Google Colab/
    mediapipe/
    pose_estimation/
    trainer/
    virtual_assistance/
    3d_motion_capture/
```

Root files:

- `README.md`: research summary, abstract, methodology, results, limitations, and report links.
- `requirements.txt`: Python package dependencies.
- `LICENSE`: project license.
- `CODE_OF_CONDUCT.md`: community behavior guidelines.
- `PROJECT_DOCUMENTATION.md`: this technical guide.

Asset folders:

- `assets/`: project poster, report PDF, and pipeline workflow image.
- `IMAGE_FILES/`: image examples and datasets for body-part exercises and pose classification.
- `VIDEO_FILES/`: exercise demonstration videos organized by body region.

Generated/cache folders:

- `__pycache__/`: Python bytecode cache files. These are generated automatically and are not part of the project logic.
- `.vscode/`: local editor configuration.

## Installation

Recommended setup from the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3.12 -m pip install -r requirements.txt
```

If `py -3.12` is not available, use your installed Python command:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Most scripts require a webcam. Press `q` in OpenCV windows to stop many of the local scripts. Some MediaPipe demo scripts use `Esc` instead.

## Main Concepts

### Pose Landmarks

MediaPipe Pose returns 33 body landmarks. The code references landmarks by index or MediaPipe landmark name.

Common landmark indexes used in this project:

- `11`: left shoulder
- `12`: right shoulder
- `13`: left elbow
- `14`: right elbow
- `15`: left wrist
- `16`: right wrist
- `23`: left hip
- `24`: right hip
- `25`: left knee
- `26`: right knee
- `27`: left ankle
- `28`: right ankle

### Angle Calculation

Most exercise scripts calculate an angle from three landmarks:

```text
point 1 -> point 2 -> point 3
```

The middle point is the joint being measured. For example:

- Right elbow flexion/extension: shoulder `12`, elbow `14`, wrist `16`.
- Right knee flexion/extension: hip `24`, knee `26`, ankle `28`.
- Cross-arm stretch: left shoulder `11`, right shoulder `12`, right elbow `14`.

### Repetition Counting

The exercise scripts usually convert the joint angle into a percentage with `numpy.interp`. A `dir` state tracks whether the user is moving toward the end position or returning to the start position. The counter increases by `0.5` at each end of the movement, so one full repetition becomes `1`.

### Feedback

Some scripts provide feedback with:

- On-screen OpenCV overlays.
- `pyttsx3` voice prompts.
- Visibility checks to ensure required landmarks are visible.
- DTW comparison against saved reference landmark data.

## `src/AI`

This folder contains a generic exercise counter for several exercise types.

### `src/AI/main.py`

Purpose: runs a real-time or video-based exercise counter.

Supported exercise types:

- `push-up`
- `pull-up`
- `squat`
- `walk`
- `sit-up`

Important logic:

- Parses command-line arguments with `parse_args()`.
- Opens the webcam or a selected video file.
- Runs MediaPipe Pose.
- Calls `TypeOfExercise(...).calculate_exercise(...)`.
- Draws the pose skeleton and score table.

Run examples:

```powershell
python src\AI\main.py -t squat
python src\AI\main.py -t push-up -vs push-up.mp4
python src\AI\main.py -t sit-up -vs src\AI\videos\sit-up.mp4
```

Arguments:

- `-t` or `--exercise_type`: exercise type.
- `-vs` or `--video_source`: optional video filename/path. If omitted, webcam `0` is used.

### `src/AI/body_part_angle.py`

Purpose: provides reusable body-angle calculations.

Class:

- `BodyPartAngle`: receives MediaPipe landmarks and calculates joint/body angles.

Methods:

- `angle_of_the_left_arm()`: angle at left elbow.
- `angle_of_the_right_arm()`: angle at right elbow.
- `angle_of_the_left_leg()`: angle at left knee.
- `angle_of_the_right_leg()`: angle at right knee.
- `angle_of_the_neck()`: neck/body alignment angle based on mouth, shoulders, and hips.
- `angle_of_the_abdomen()`: torso/abdomen angle based on shoulders, hips, and knees.

### `src/AI/types_of_exercise.py`

Purpose: converts angles and landmarks into exercise-specific repetition counts.

Class:

- `TypeOfExercise(BodyPartAngle)`: extends `BodyPartAngle` with exercise counting rules.

Methods:

- `push_up(counter, status)`: counts push-up movement using arm angle thresholding.
- `pull_up(counter, status)`: counts pull-up movement using nose and elbow position.
- `squat(counter, status)`: counts squat movement using leg angle thresholding.
- `walk(counter, status)`: counts walking steps using relative knee positions.
- `sit_up(counter, status)`: counts sit-ups using abdomen angle.
- `calculate_exercise(exercise_type, counter, status)`: dispatches to the correct exercise method.

Notes:

- `counter` stores the current repetition count.
- `status` stores whether the movement is ready to count the next phase.

### `src/AI/utils.py`

Purpose: helper functions for angle math, landmark extraction, and screen overlay.

Functions:

- `calculate_angle(a, b, c)`: calculates the angle at point `b`.
- `detection_body_part(landmarks, body_part_name)`: returns `[x, y, visibility]` for a named MediaPipe landmark.
- `detection_body_parts(landmarks)`: builds a Pandas table of landmark names and coordinates.
- `score_table(exercise, frame, counter, status)`: writes activity, counter, and status text on the OpenCV frame.

### `src/AI/videos`

Purpose: sample videos for the generic AI counter.

Files:

- `pull-up.mp4`
- `push-up.mp4`
- `sit-up.mp4`
- `squat.mp4`
- `walk.mp4`

## `src/pose_estimation`

This folder contains a simple reusable pose detector and basic demo scripts.

### `src/pose_estimation/PoseModule.py`

Purpose: wrapper around MediaPipe Pose.

Class:

- `poseDetector`

Methods:

- `__init__(...)`: configures MediaPipe Pose settings.
- `findPose(img, draw=True)`: detects pose landmarks and optionally draws the skeleton.
- `findPosition(img, draw=True)`: returns landmark positions as pixel coordinates.
- `findAngle(img, p1, p2, p3, draw=True)`: calculates and optionally draws an angle.
- `main()`: demo that opens webcam, detects landmarks, prints landmark `14`, and displays FPS.

### `src/pose_estimation/basic.py`

Purpose: basic pose estimation experiment.

### `src/pose_estimation/main.py`

Purpose: small entry script for running pose detection experiments.

## `src/trainer`

This folder contains exercise-specific trainer scripts that count repetitions from webcam or video files.

### `src/trainer/pose/PoseModule.py`

Purpose: trainer copy of the MediaPipe pose wrapper. It is similar to `src/pose_estimation/PoseModule.py`.

Class and methods:

- `poseDetector`
- `findPose(img, draw=True)`
- `findPosition(img, draw=True)`
- `findAngle(img, p1, p2, p3, draw=True)`
- `main()`

### `src/trainer/pose/video_source.py`

Purpose: shared command-line video source helper for trainer scripts.

Functions:

- `parse_video_args(description)`: adds `--source`, `--no-display`, and `--max-frames` arguments.
- `open_video_source(source)`: opens webcam index or video file path and configures resolution/FPS.
- `should_stop_for_key()`: returns true when the user presses `q`.

### `src/trainer/pose/elbow_flexion_extension.py`

Purpose: counts right elbow flexion/extension repetitions.

Landmarks:

- `12`: right shoulder
- `14`: right elbow
- `16`: right wrist

Run examples:

```powershell
python src\trainer\pose\elbow_flexion_extension.py --source 0
python src\trainer\pose\elbow_flexion_extension.py --source src\trainer\test_vid\elbow_flexion_extension.mp4
python src\trainer\pose\elbow_flexion_extension.py --source src\trainer\test_vid\elbow_flexion_extension.mp4 --no-display --max-frames 200
```

### `src/trainer/pose/knee_flexion_extension.py`

Purpose: counts right knee flexion/extension repetitions.

Landmarks:

- `24`: right hip
- `26`: right knee
- `28`: right ankle

Run example:

```powershell
python src\trainer\pose\knee_flexion_extension.py --source src\trainer\test_vid\knee_flexion_extension.mp4
```

### `src/trainer/pose/cross_arm_stretch.py`

Purpose: counts cross-arm stretch repetitions.

Landmarks:

- `11`: left shoulder
- `12`: right shoulder
- `14`: right elbow

Run example:

```powershell
python src\trainer\pose\cross_arm_stretch.py --source src\trainer\test_vid\cross_arm_stretch.mp4
```

### `src/trainer/pose/scaption_with_dumbells.py`

Purpose: processes a scaption-with-dumbbells movement and plots tracked joint coordinates.

Functions:

- `video_processing(source="0", no_display=False, max_frames=0)`: reads frames, detects pose, collects coordinates for landmarks `11`, `23`, and `25`.
- `plot_joint_coords(joint_coords_1, joint_coords_2, joint_coords_3)`: plots X/Y coordinate movement for the collected landmarks.

Run examples:

```powershell
python src\trainer\pose\scaption_with_dumbells.py --source 0
python src\trainer\pose\scaption_with_dumbells.py --source src\trainer\test_vid\scaption_with_dumbbells.mp4
```

### `src/trainer/pose/scaption_with_dumbbells_voice.py`

Purpose: scaption experiment with text-to-speech feedback.

Functions:

- `notify(message)`: speaks a message with `pyttsx3`.
- `video_processing()`: runs webcam pose detection, tracks arm-raise percentage, counts repetitions, and speaks feedback.

### `src/trainer/pose/offline_tts.py`

Purpose: experiments with `pyttsx3` voice settings.

It demonstrates:

- Setting speech rate.
- Setting volume.
- Selecting a voice.
- Speaking text.
- Commented examples for callbacks and saving audio.

### `src/trainer/test_vid`

Purpose: test videos for trainer scripts.

Files:

- `cross_arm_stretch.mp4`
- `elbow_flexion_extension.mp4`
- `knee_flexion_extension.mp4`
- `scaption_with_dumbbells.mp4`

## `src/virtual_assistance`

This folder contains real-time virtual-assistant scripts with more user feedback, including voice prompts and DTW experiments.

### `src/virtual_assistance/PoseModule.py`

Purpose: virtual-assistance copy of the pose detector wrapper.

Difference from some other copies:

- `findPosition()` returns `[id, x, y, visibility]`, including landmark visibility.
- Visibility is used by assistant scripts to check whether the required body part is visible.

Class:

- `poseDetector`

Methods:

- `findPose(img, draw=True)`
- `findPosition(img, draw=True)`
- `findAngle(img, p1, p2, p3, draw=False)`
- `main()`

### `src/virtual_assistance/elbow_flexion_extension.py`

Purpose: real-time right elbow flexion/extension assistant with voice feedback.

Function:

- `speak(engine, text)`: speaks feedback in a separate thread.

Behavior:

- Opens webcam.
- Detects right shoulder, right elbow, and right wrist.
- Checks landmark visibility.
- Calculates right elbow angle.
- Converts the angle into a movement percentage.
- Draws a vertical progress bar and repetition count.
- Gives voice prompts such as bending or straightening the right arm.

Run:

```powershell
python src\virtual_assistance\elbow_flexion_extension.py
```

### `src/virtual_assistance/cross_arm_stretch.py`

Purpose: real-time cross-arm stretch assistant with voice feedback.

Behavior:

- Opens webcam.
- Checks shoulder and elbow visibility.
- Checks shoulder level.
- Checks right elbow height.
- Calculates stretch angle.
- Counts repetitions.
- Speaks corrective feedback.

Run:

```powershell
python src\virtual_assistance\cross_arm_stretch.py
```

### `src/virtual_assistance/elbow_flexion_extension_dtw.py`

Purpose: elbow flexion/extension assistant with DTW comparison against reference landmarks.

Functions:

- `speak(engine, text)`: speaks feedback.
- `dtw_comparison_thread(landmark_history, reference_landmarks, feedback_callback)`: compares collected landmark history against reference landmarks.
- `update_feedback(new_feedback)`: thread-safe callback that updates feedback text.

Behavior:

- Loads `reference_landmarks.npy`.
- Collects shoulder, elbow, and wrist positions.
- Every 30 collected frames, compares the movement to the reference sequence with `fastdtw`.
- Gives feedback based on DTW distance.

Preparation:

```powershell
python src\virtual_assistance\extract_npy.py
python src\virtual_assistance\elbow_flexion_extension_dtw.py
```

Important note: `reference_landmarks.npy` is loaded from the current working directory. Run from the same directory where the `.npy` file exists, or adjust the path in the script.

### `src/virtual_assistance/extract_npy.py`

Purpose: extracts reference landmarks from a reference elbow flexion/extension video and saves them to `reference_landmarks.npy`.

Behavior:

- Opens `Active Elbow Flexion & Extension.mp4`.
- Detects landmarks for each frame.
- Stores right shoulder, right elbow, and right wrist coordinates.
- Saves the result as a NumPy `.npy` file.

### `src/virtual_assistance/test.py`

Purpose: experimental DTW assistant using a `Queue` for thread-safe feedback and a count milestone callback.

Functions:

- `speak(engine, text)`
- `dtw_comparison_thread(landmark_history, reference_landmarks, feedback_queue, count_callback)`
- `check_count_milestone()`

### `src/virtual_assistance/sample.py`

Purpose: experimental/sample virtual-assistance script. It is not the main documented entry point, but it belongs to the same assistant exploration area.

### `src/virtual_assistance/Active Elbow Flexion & Extension.mp4`

Purpose: reference video for extracting elbow flexion/extension landmark sequences.

## `src/mediapipe`

This folder contains standalone MediaPipe/cvzone experiments. These are useful for learning and prototyping, not the main exercise counter.

### `src/mediapipe/img_pose.py`

Purpose: runs MediaPipe Pose on static images.

Behavior:

- Loads selected images from `IMAGE_FILES`.
- Runs pose detection with segmentation.
- Draws pose landmarks.
- Writes annotated output images.
- Plots world landmarks.

### `src/mediapipe/vid_pose.py`

Purpose: simple webcam pose demo using MediaPipe directly.

Behavior:

- Opens webcam.
- Detects pose.
- Draws pose landmarks.
- Displays the flipped frame.
- Stops on `Esc`.

### `src/mediapipe/PoseEstimationExample.py`

Purpose: cvzone pose-estimation example.

Behavior:

- Opens webcam.
- Detects landmarks with `cvzone.PoseModule.PoseDetector`.
- Calculates distance and left-arm angle.
- Checks whether the angle is close to a target value.

### `src/mediapipe/updated_pose.py`

Purpose: cvzone experiment that calculates many body angles.

Behavior:

- Defines multiple landmark triplets.
- Calculates angles for arms, legs, body sides, shoulders, and neck.

## `src/Google Colab`

This folder contains a Google Colab-style pose classification pipeline. It is more dataset/classification focused than the real-time trainer scripts.

### `basic_main.ipynb`

Purpose: notebook version of a pose-classification workflow.

### `exteded_embedding.py`

Purpose: creates normalized full-body pose embeddings from 3D landmarks.

Functions/classes:

- `show_image(img, figsize=(10, 10))`: displays an image with Matplotlib.
- `FullBodyPoseEmbedder`: normalizes landmarks and creates a distance-based pose embedding.
- `PoseSample`: stores sample name, landmarks, class name, and embedding.
- `PoseSampleOutlier`: stores information about classification outliers.

### `extended_bootstrap.py`

Purpose: converts labeled pose images into CSV landmark datasets.

Classes/functions:

- `BootstrapHelper`: bootstraps image folders into pose landmark CSVs.
- `bootstrap(per_pose_class_limit=None)`: processes images and writes landmark CSVs.
- `_draw_xz_projection(...)`: draws a side projection of pose landmarks.
- `align_images_and_csvs(...)`: keeps image folders and CSV rows in sync.
- `analyze_outliers(outliers)`: displays suspicious samples.
- `remove_outliers(outliers)`: deletes outlier images.
- `print_images_in_statistics()`: prints input image counts.
- `print_images_out_statistics()`: prints output image counts.
- `dump_for_the_app()`: merges per-class CSV files into one CSV for app use.

### `extended_classification_smoothing.py`

Purpose: classifies pose landmarks and smooths classification results.

Classes:

- `PoseClassifier`: nearest-neighbor pose classifier using pose embeddings.
- `EMADictSmoothing`: applies exponential moving average smoothing to classification values.

### `extended_counter_visualizer.py`

Purpose: counts repetitions from classification confidence and renders visualization overlays.

Classes:

- `RepetitionCounter`: counts exits from a target pose class using enter/exit thresholds.
- `PoseClassificationVisualizer`: draws classification history and repetition count on output frames.

### `extended-main.py`

Purpose: Colab pipeline script that ties the embedding, classifier, smoother, counter, and visualizer together.

Flow:

1. Upload a video.
2. Open video with OpenCV.
3. Initialize MediaPipe Pose.
4. Load pose samples from CSVs.
5. Classify each frame.
6. Smooth classifications.
7. Count repetitions.
8. Draw overlay.
9. Save and download output video.

## `src/3d_motion_capture`

This folder is an experiment for exporting pose landmarks and replaying them in Unity.

### `src/3d_motion_capture/main.py`

Purpose: captures pose landmark coordinates from webcam or video and writes them to `AnimationFile.txt`.

Behavior:

- Uses `cvzone.PoseModule.PoseDetector`.
- Collects landmark coordinate strings frame by frame.
- Press `s` to save collected frames to `src/3d_motion_capture/AnimationFile.txt`.

### `src/3d_motion_capture/AnimationFile.txt`

Purpose: saved pose landmark coordinates for animation playback.

### `src/3d_motion_capture/animation.cs`

Purpose: Unity script that reads `AnimationFile.txt` and moves body landmark objects.

Main behavior:

- Reads each line of saved landmark data.
- Splits coordinates.
- Updates positions of `Body` objects.
- Loops back to the start when all frames are played.

Note: the script expects x, y, and z values per landmark, while the current Python export has a 2D coordinate line active and a 3D line commented out. If using Unity playback, make sure the Python export format matches the C# reader.

### `src/3d_motion_capture/line.cs`

Purpose: Unity script for drawing a line between two body landmarks.

Behavior:

- Uses a `LineRenderer`.
- Updates line start and end positions every frame.

### `src/3d_motion_capture/Video.mp4`

Purpose: sample video for motion capture experiments.

## Data And Media Folders

### `IMAGE_FILES`

Purpose: stores image examples and pose datasets.

Notable folders:

- `back/`: back-related exercise images.
- `foot/`: foot/leg exercise images.
- `shoulders & arms/`: shoulder and arm exercise images.
- `fitness_poses_images_in/`: labeled pose-class image dataset, including `pushups_up` and `pushups_down`.

### `VIDEO_FILES`

Purpose: stores demonstration videos grouped by body region.

Notable folders:

- `back/`: back exercise videos.
- `foot/`: foot/leg exercise videos.
- `shoulders & arms/`: shoulder and arm exercise videos.

## Common Workflows

### Run A Webcam Exercise Counter

```powershell
python src\trainer\pose\elbow_flexion_extension.py --source 0
```

Use `q` to stop.

### Run A Trainer Script On A Test Video

```powershell
python src\trainer\pose\cross_arm_stretch.py --source src\trainer\test_vid\cross_arm_stretch.mp4
```

### Run Without Display For A Quick Check

```powershell
python src\trainer\pose\elbow_flexion_extension.py --source src\trainer\test_vid\elbow_flexion_extension.mp4 --no-display --max-frames 100
```

### Run Generic AI Counter

```powershell
python src\AI\main.py -t squat
python src\AI\main.py -t squat -vs squat.mp4
```

### Create DTW Reference Landmarks

```powershell
python src\virtual_assistance\extract_npy.py
```

This creates `reference_landmarks.npy`.

### Run DTW-Based Assistant

```powershell
python src\virtual_assistance\elbow_flexion_extension_dtw.py
```

## How To Add A New Exercise

The simplest path is to copy an existing trainer script and adjust the measured landmarks and angle thresholds.

1. Choose the three landmarks that form the target joint angle.
   Example: for right elbow, use `12, 14, 16`.

2. Create a new file in `src/trainer/pose/`.
   Example: `shoulder_external_rotation.py`.

3. Import shared helpers:

```python
import cv2
import numpy as np
import PoseModule as pm
from video_source import open_video_source, parse_video_args, should_stop_for_key
```

4. Open the camera/video using `parse_video_args()` and `open_video_source()`.

5. Detect landmarks using:

```python
img = detector.findPose(img, False)
lmList = detector.findPosition(img, False)
```

6. Calculate the movement angle:

```python
angle = detector.findAngle(img, p1, p2, p3)
```

7. Convert the angle to a percentage:

```python
per = np.interp(angle, (min_angle, max_angle), (0, 100))
```

8. Use a direction state to count a full repetition:

```python
if per == 100 and dir == 0:
    count += 0.5
    dir = 1
if per == 0 and dir == 1:
    count += 0.5
    dir = 0
```

9. Draw the progress bar and count using OpenCV.

10. Test with webcam and with a saved video.

## How To Add Voice Feedback

Use `pyttsx3`:

```python
import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1)

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()
```

To avoid blocking video processing, run speech in a thread:

```python
speech_thread = threading.Thread(target=speak, args=(engine, feedback))
speech_thread.start()
```

Use cooldown logic so the same feedback is not repeated every frame.

## How To Use DTW For Movement Comparison

DTW is useful when the same movement may happen at different speeds. The project approach is:

1. Extract reference landmarks from a correct exercise video.
2. Save them as `reference_landmarks.npy`.
3. During webcam use, collect the same landmarks over multiple frames.
4. Flatten both sequences.
5. Compare with `fastdtw(..., dist=euclidean)`.
6. Give feedback based on the distance.

Current DTW scripts focus on right elbow flexion/extension using landmarks:

- right shoulder
- right elbow
- right wrist

## Troubleshooting

### Missing Dependency

Install packages:

```powershell
python -m pip install -r requirements.txt
```

### Webcam Does Not Open

Try a different source:

```powershell
python src\trainer\pose\elbow_flexion_extension.py --source 1
```

Or use a video file:

```powershell
python src\trainer\pose\elbow_flexion_extension.py --source src\trainer\test_vid\elbow_flexion_extension.mp4
```

### No Pose Detected

Check:

- Person is fully visible.
- Lighting is bright enough.
- Camera is far enough away.
- Exercise body part is not hidden.
- Video path is correct.

### Voice Does Not Work

`pyttsx3` depends on local system voices. Check the installed voices with the examples in `src/trainer/pose/offline_tts.py`.

### DTW File Not Found

Run:

```powershell
python src\virtual_assistance\extract_npy.py
```

Then make sure `reference_landmarks.npy` is in the working directory used by the DTW script.

## Development Notes

- Many scripts are experiments and are not packaged as a single application.
- Several folders contain their own `PoseModule.py`; these are similar but not identical.
- The virtual-assistance `PoseModule.py` includes visibility values, which are important for feedback.
- `src/trainer/pose/video_source.py` is the cleanest reusable helper for camera/video source handling.
- `__pycache__` files are generated and should not be edited manually.
- Some paths in older scripts are hard-coded and may need adjustment depending on where the script is run from.
- The project currently uses OpenCV windows rather than a web or desktop GUI.

## Best Entry Points

For learning the code:

1. Start with `src/pose_estimation/PoseModule.py`.
2. Read `src/trainer/pose/elbow_flexion_extension.py`.
3. Read `src/trainer/pose/video_source.py`.
4. Read `src/AI/main.py` for the generic exercise counter.
5. Read `src/virtual_assistance/elbow_flexion_extension.py` for voice feedback.
6. Read `src/virtual_assistance/elbow_flexion_extension_dtw.py` for DTW feedback.

For running demos:

```powershell
python src\trainer\pose\elbow_flexion_extension.py --source 0
python src\trainer\pose\cross_arm_stretch.py --source src\trainer\test_vid\cross_arm_stretch.mp4
python src\AI\main.py -t squat
```
