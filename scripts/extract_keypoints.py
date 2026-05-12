"""Extract pose + face + hand keypoints from video using MediaPipe Tasks API (0.10+).

Output: (T, 1086) — compatible con Signformer / LSA-T.
  Pose:       33 kp × 2 (x,y) =  66 features  [ 0   : 66  ]
  Face:      468 kp × 2 (x,y) = 936 features  [ 66  : 1002]
  Mano izq:  21 kp × 2 (x,y) =  42 features  [1002 : 1044]
  Mano der:  21 kp × 2 (x,y) =  42 features  [1044 : 1086]
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
import yaml

MODELS_DIR = Path(__file__).parent.parent / "models"

N_POSE  = 33
N_FACE  = 468   # FaceLandmarker devuelve 478; tomamos los primeros 468 (face mesh sin iris)
N_HAND  = 21
FEATURE_SIZE = (N_POSE + N_FACE + N_HAND + N_HAND) * 2  # 1086


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def _build_detectors(config: dict):
    mp_cfg = config["mediapipe"]
    det_conf = mp_cfg["min_detection_confidence"]
    trk_conf = mp_cfg["min_tracking_confidence"]

    pose_det = mp_vision.PoseLandmarker.create_from_options(
        mp_vision.PoseLandmarkerOptions(
            base_options=mp_python.BaseOptions(
                model_asset_path=str(MODELS_DIR / "pose_landmarker.task")
            ),
            running_mode=mp_vision.RunningMode.VIDEO,
            min_pose_detection_confidence=det_conf,
            min_tracking_confidence=trk_conf,
        )
    )

    face_det = mp_vision.FaceLandmarker.create_from_options(
        mp_vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(
                model_asset_path=str(MODELS_DIR / "face_landmarker.task")
            ),
            running_mode=mp_vision.RunningMode.VIDEO,
            min_face_detection_confidence=det_conf,
            min_tracking_confidence=trk_conf,
        )
    )

    hand_det = mp_vision.HandLandmarker.create_from_options(
        mp_vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(
                model_asset_path=str(MODELS_DIR / "hand_landmarker.task")
            ),
            running_mode=mp_vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=det_conf,
            min_tracking_confidence=trk_conf,
        )
    )

    return pose_det, face_det, hand_det


def _lm_to_xy(landmarks, n: int) -> np.ndarray:
    """Convierte landmarks a array (n, 2). Rellena con ceros si faltan."""
    arr = np.zeros((n, 2), dtype=np.float32)
    if landmarks:
        lms = landmarks[:n]
        for i, lm in enumerate(lms):
            arr[i] = [lm.x, lm.y]
    return arr


def _extract_frame(pose_res, face_res, hand_res) -> np.ndarray:
    """Arma el vector de 1086 features para un frame."""
    # Pose: 33 kp
    pose_lms = pose_res.pose_landmarks[0] if pose_res.pose_landmarks else None
    pose_xy = _lm_to_xy(pose_lms, N_POSE)

    # Cara: 468 kp (tomamos los primeros 468 de los 478 que devuelve FaceLandmarker)
    face_lms = face_res.face_landmarks[0] if face_res.face_landmarks else None
    face_xy = _lm_to_xy(face_lms, N_FACE)

    # Manos
    left_xy  = np.zeros((N_HAND, 2), dtype=np.float32)
    right_xy = np.zeros((N_HAND, 2), dtype=np.float32)
    for i, handedness in enumerate(hand_res.handedness):
        label = handedness[0].category_name  # "Left" o "Right"
        lms = hand_res.hand_landmarks[i]
        xy = _lm_to_xy(lms, N_HAND)
        if label == "Left":
            left_xy = xy
        else:
            right_xy = xy

    # Concatenar en orden: pose | face | left | right → (1086,)
    return np.concatenate([
        pose_xy.flatten(),   #  66
        face_xy.flatten(),   # 936
        left_xy.flatten(),   #  42
        right_xy.flatten(),  #  42
    ])


def _confidence_avg(pose_res) -> float:
    if not pose_res.pose_landmarks:
        return 0.0
    vis = [lm.visibility for lm in pose_res.pose_landmarks[0]]
    return float(np.mean(vis))


def extract_keypoints(
    video_path: Path,
    config: dict,
    frame_start: int = 0,
    frame_end: int = None,
) -> dict:
    pose_det, face_det, hand_det = _build_detectors(config)

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_end = frame_end or total_frames
    sample_rate = config["dataset"]["sample_rate"]

    frames_data = []
    confidences = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx > frame_end:
            break

        if frame_idx >= frame_start and (frame_idx - frame_start) % sample_rate == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            ts_ms = int(frame_idx * 1000 / fps)

            pose_res = pose_det.detect_for_video(mp_img, ts_ms)
            face_res = face_det.detect_for_video(mp_img, ts_ms)
            hand_res = hand_det.detect_for_video(mp_img, ts_ms)

            vector = _extract_frame(pose_res, face_res, hand_res)
            conf   = _confidence_avg(pose_res)
            confidences.append(conf)

            frames_data.append({
                "frame": frame_idx,
                "vector": vector.tolist(),        # (1086,) — listo para guardar
                "pose_detected":  bool(pose_res.pose_landmarks),
                "face_detected":  bool(face_res.face_landmarks),
                "left_hand":      any(h[0].category_name == "Left"  for h in hand_res.handedness),
                "right_hand":     any(h[0].category_name == "Right" for h in hand_res.handedness),
                "confidence":     round(conf, 4),
            })

        frame_idx += 1

    cap.release()
    pose_det.close()
    face_det.close()
    hand_det.close()

    return {
        "video": str(video_path),
        "fps": fps,
        "feature_size": FEATURE_SIZE,
        "frame_range": [frame_start, frame_end],
        "n_frames_processed": len(frames_data),
        "confidence_avg": round(float(np.mean(confidences)) if confidences else 0.0, 4),
        "frames": frames_data,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Path al video")
    parser.add_argument("--output", help="Salida JSON")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--frame-start", type=int, default=0)
    parser.add_argument("--frame-end",   type=int, default=None)
    parser.add_argument("--sample-rate", type=int, default=None,
                        help="1 de cada N frames (sobreescribe config)")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.sample_rate:
        config["dataset"]["sample_rate"] = args.sample_rate

    video_path = Path(args.video)
    result = extract_keypoints(video_path, config, args.frame_start, args.frame_end)

    output_path = (
        Path(args.output)
        if args.output
        else Path(config["paths"]["keypoints"]) / f"{video_path.stem}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f)

    print(f"Guardado: {output_path}")
    print(f"Frames: {result['n_frames_processed']} | feature_size: {result['feature_size']} | confidence: {result['confidence_avg']:.4f}")
