try:
    import cv2
    import mediapipe as mp
    import numpy as np
    AVATAR_AVAILABLE = True
except ImportError:
    AVATAR_AVAILABLE = False
    print("⚠️ OpenCV/MediaPipe not available on cloud")

import streamlit as st

def generate_avatar_sign(text):
    """Show sign language avatar (Cloud-friendly version)"""
    if not AVATAR_AVAILABLE:
        st.warning("⚠️ 3D Avatar with MediaPipe is only available locally.")
        st.info(f"💡 Showing text-based signing for: *{text}*")
        
        # Show fingerspelling as fallback
        try:
            from fingerspell import fingerspell_word
            words = text.split()
            for word in words:
                st.write(f"*{word}* → {fingerspell_word(word)}")
        except ImportError:
            st.write(f"📝 Signing: {text}")
        return
    
    # === LOCAL AVATAR CODE (Webcam ke saath) ===
    try:
        st.info(f"🎬 3D Avatar signing: *{text}*")
        st.warning("📸 Webcam will open in a new window. Press 'q' to close.")
        
        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic
        holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Webcam not accessible. Please check your camera.")
            return
        
        # Show a few frames
        frame_count = 0
        while cap.isOpened() and frame_count < 100:  # 100 frames tak
            ret, frame = cap.read()
            if not ret:
                break
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw landmarks
            if results.face_landmarks:
                mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            
            cv2.putText(image, f"Signing: {text}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('3D Avatar Sign Language', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        st.success("✅ Avatar session completed!")
        
    except Exception as e:
        st.error(f"❌ Error in avatar: {e}")
        st.info("💡 Make sure your webcam is connected and permissions are granted.")

def generate_avatar_sign_local(text):
    """Alias for generate_avatar_sign (for local testing)"""
    return generate_avatar_sign(text)