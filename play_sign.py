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
        video_path = video.get('path', '')
        if video_path and os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"⚠️ Video not available: {video_path}")

# Cloud-friendly - no main guard with streamlit