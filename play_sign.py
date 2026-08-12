import cv2
import os

def play_video(video_path):
    """Play a single video file"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Sign Language', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def play_videos(videos):
    """Play multiple videos in sequence"""
    for idx, video_dict in enumerate(videos, 1):
        print(f"Playing sign {idx}: {video_dict['name']}")
        play_video(video_dict['path'])  # path key use karna