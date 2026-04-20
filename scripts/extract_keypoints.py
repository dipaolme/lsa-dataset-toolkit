"""Extract pose + hand keypoints from video using MediaPipe Holistic."""
import argparse
import json
from pathlib import Path

import cv2
import mediapipe as mp
import yaml


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def extract_keypoints(video_path: Path, config: dict, frame_start: int = 0, frame_end: int = None) -> dict:
    mp_cfg = config["mediapipe"]
    holistic = mp.solutions.holistic.Holistic(
        model_complexity=mp_cfg["model_complexity"],
        min_detection_confidence=mp_cfg["min_detection_confidence"],
        min_tracking_confidence=mp_cfg["min_tracking_confidence"],
        static_image_mode=mp_cfg["static_image_mode"],
    )

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_end = frame_end or total_frames
    sample_rate = config["dataset"]["sample_rate"]

    frames_data = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx > frame_end:
            break

        if frame_idx >= frame_start and (frame_idx - frame_start) % sample_rate == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(rgb)
            frames_data.append({
                "frame": frame_idx,
                "pose": _landmarks_to_list(results.pose_landmarks),
                "left_hand": _landmarks_to_list(results.left_hand_landmarks),
                "right_hand": _landmarks_to_list(results.right_hand_landmarks),
            })

        frame_idx += 1

    cap.release()
    holistic.close()

    confidences = [
        lm["visibility"]
        for f in frames_data
        if f["pose"]
        for lm in f["pose"]
        if "visibility" in lm
    ]
    confidence_avg = sum(confidences) / len(confidences) if confidences else 0.0

    return {
        "video": str(video_path),
        "fps": fps,
        "frame_range": [frame_start, frame_end],
        "n_frames_processed": len(frames_data),
        "confidence_avg": round(confidence_avg, 4),
        "frames": frames_data,
    }


def _landmarks_to_list(landmarks) -> list | None:
    if landmarks is None:
        return None
    return [
        {"x": lm.x, "y": lm.y, "z": lm.z, **({"visibility": lm.visibility} if hasattr(lm, "visibility") else {})}
        for lm in landmarks.landmark
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract keypoints from video")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--output", help="Output JSON path (default: data/keypoints/<video_id>.json)")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--frame-start", type=int, default=0)
    parser.add_argument("--frame-end", type=int, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    video_path = Path(args.video)
    result = extract_keypoints(video_path, config, args.frame_start, args.frame_end)

    output_path = Path(args.output) if args.output else Path(config["paths"]["keypoints"]) / f"{video_path.stem}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Keypoints saved to {output_path}")
    print(f"Frames processed: {result['n_frames_processed']}, confidence avg: {result['confidence_avg']}")
