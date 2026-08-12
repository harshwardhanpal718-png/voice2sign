import streamlit as st
import os

def play_video(video_path):
    """Play video using Streamlit's video player"""
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.warning(f"⚠️ Video not found: {video_path}")

def play_videos(videos):
    """Play multiple videos in sequence"""
    if not videos:
        st.warning("No videos to play")
        return
    
    for idx, video in enumerate(videos, 1):
        st.write(f"*Sign {idx}: {video.get('name', 'unknown')}*")
        
        # Check if video path exists
        video_path = video.get('path', '')
        if video_path and os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"⚠️ Video not available: {video_path}")
            # Fallback: show text instead
            st.info(f"Sign for: {video.get('name', 'unknown')}")

if _name_ == "_main_":
    print("play_sign.py is a video player module.")