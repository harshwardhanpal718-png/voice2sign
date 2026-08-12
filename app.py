import streamlit as st
from speech_to_text import transcribe_audio_file, transcribe_audio_from_mic
from text_processor import process_text
from sign_mapper import map_text_to_signs
from play_sign import play_videos
import os
import tempfile

st.set_page_config(page_title="Voice to Sign Language", page_icon="🤟")

st.title("🎬 Voice to Sign Language Converter")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    option = st.radio(
        "Choose input method:",
        ["📁 Upload Audio File", "🎤 Record from Microphone"]
    )
    
    if option == "🎤 Record from Microphone":
        duration = st.slider("Recording duration (seconds)", 3, 10, 5)

# Main area
if option == "📁 Upload Audio File":
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
    
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                tmpfile.write(uploaded_file.read())
                tmp_path = tmpfile.name
            
            # Transcribe
            text = transcribe_audio_file(tmp_path)
            
            if text:
                # Process
                words = process_text(text)
                
                # Map to signs
                videos = map_text_to_signs(words)
                
                # Display results
                st.success(f"✅ Recognized: *{text}*")
                st.write(f"📝 Processed Words: {', '.join(words)}")
                
                if videos:
                    st.write(f"🎯 Found {len(videos)} sign(s)")
                    st.info("🎬 Playing signs in a new window...")
                    
                    # Play videos
                    play_videos(videos)
                else:
                    st.warning("⚠️ No signs found for the given text.")
            
            os.unlink(tmp_path)

else:  # Microphone option
    if st.button("🎤 Start Recording"):
        with st.spinner(f"Recording for {duration} seconds..."):
            text = transcribe_audio_from_mic(duration)
            
            if text:
                # Process
                words = process_text(text)
                
                # Map to signs
                videos = map_text_to_signs(words)
                
                # Display results
                st.success(f"✅ Recognized: *{text}*")
                st.write(f"📝 Processed Words: {', '.join(words)}")
                
                if videos:
                    st.write(f"🎯 Found {len(videos)} sign(s)")
                    st.info("🎬 Playing signs in a new window...")
                    
                    # Play videos
                    play_videos(videos)
                else:
                    st.warning("⚠️ No signs found for the given text.")
            else:
                st.error("❌ Could not recognize speech. Please try again.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
from avatar_sign import generate_avatar_sign
from sentence_mapper import map_sentence_to_signs

# After text processing
if st.button("🎬 Show 3D Avatar"):
    avatar_text = " ".join(processed_words)
    generate_avatar_sign(avatar_text)
    
    # Show ISL style sentence
    isl_signs = map_sentence_to_signs(avatar_text)
    st.write("🖐️ ISL Style:", " → ".join(isl_signs))