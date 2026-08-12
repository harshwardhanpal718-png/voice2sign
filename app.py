import streamlit as st
from speech_to_text import transcribe_audio_file, transcribe_audio_from_mic
from text_processor import process_text
from sign_mapper import map_text_to_signs
from play_sign import play_videos
from sentence_mapper import get_sign_emoji
from fingerspell import fingerspell_word
import os
import tempfile

# ==================== AVATAR IMPORT (Cloud Safe) ====================
try:
    from avatar_sign import generate_avatar_sign, generate_avatar_sign_local
    AVATAR_AVAILABLE = True
except ImportError:
    AVATAR_AVAILABLE = False
    print("⚠️ Avatar module not available on cloud")
    def generate_avatar_sign(text):
        return None
    def generate_avatar_sign_local(text):
        return None

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="Voice to Sign Language", page_icon="🤟")
st.title("🎬 Voice to Sign Language Converter")
st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("⚙️ Settings")
    option = st.radio(
        "Choose input method:",
        ["📁 Upload Audio File", "🎤 Record from Microphone"]
    )
    
    if option == "🎤 Record from Microphone":
        duration = st.slider("Recording duration (seconds)", 3, 10, 5)
    
    st.markdown("---")
    st.subheader("🔧 Features")
    show_avatar = st.checkbox("🖐️ Show 3D Avatar", value=True)
    show_fingerspell = st.checkbox("🔤 Show Fingerspelling", value=True)
    show_isl_style = st.checkbox("🔄 Show ISL Style", value=True)

# ==================== MAIN ====================
if option == "📁 Upload Audio File":
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
    
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            # Save uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                tmpfile.write(uploaded_file.read())
                tmp_path = tmpfile.name
            
            # Transcribe
            text = transcribe_audio_file(tmp_path)
            
            if text:
                words = process_text(text)
                text_clean = " ".join(words)
                
                st.success(f"✅ Recognized: *{text}*")
                st.write(f"📝 Processed Words: {', '.join(words)}")
                
                # ==================== NEW FEATURES ====================
                col1, col2 = st.columns(2)
                
                with col1:
                    if show_fingerspell and words:
                        st.subheader("🔤 Fingerspelling")
                        for word in words:
                            st.write(f"*{word}* → {fingerspell_word(word)}")
                
                with col2:
                    if show_isl_style and words:
                        st.subheader("🔄 ISL Style (OSV)")
                        isl_words = words[::-1]
                        isl_emojis = [get_sign_emoji(w) for w in isl_words]
                        st.write(" → ".join(isl_emojis))
                        st.write(f"*ISL:* {' → '.join(isl_words)}")
                
                # ==================== 3D AVATAR ====================
                if show_avatar and words:
                    st.subheader("🖐️ 3D Avatar")
                    if AVATAR_AVAILABLE:
                        generate_avatar_sign(text_clean)
                    else:
                        st.info("💡 3D Avatar is only available locally. Showing fingerspelling instead.")
                        for word in words:
                            st.write(f"*{word}* → {fingerspell_word(word)}")
                
                # ==================== VIDEO PLAYBACK ====================
                st.subheader("🎬 Sign Videos")
                videos = map_text_to_signs(words)
                if videos:
                    st.write(f"🎯 Found {len(videos)} sign(s)")
                    play_videos(videos)
                else:
                    st.warning("⚠️ No signs found for the given text.")
                    st.info("💡 Using fingerspelling for all words:")
                    for word in words:
                        st.write(f"*{word}* → {fingerspell_word(word)}")
            
            os.unlink(tmp_path)

# ==================== MICROPHONE ====================
else:
    if st.button("🎤 Start Recording"):
        with st.spinner(f"Recording for {duration} seconds..."):
            text = transcribe_audio_from_mic(duration)
            
            if text:
                words = process_text(text)
                text_clean = " ".join(words)
                
                st.success(f"✅ Recognized: *{text}*")
                st.write(f"📝 Processed Words: {', '.join(words)}")
                
                # ==================== NEW FEATURES ====================
                col1, col2 = st.columns(2)
                
                with col1:
                    if show_fingerspell and words:
                        st.subheader("🔤 Fingerspelling")
                        for word in words:
                            st.write(f"*{word}* → {fingerspell_word(word)}")
                
                with col2:
                    if show_isl_style and words:
                        st.subheader("🔄 ISL Style (OSV)")
                        isl_words = words[::-1]
                        isl_emojis = [get_sign_emoji(w) for w in isl_words]
                        st.write(" → ".join(isl_emojis))
                        st.write(f"*ISL:* {' → '.join(isl_words)}")
                
                # ==================== 3D AVATAR ====================
                if show_avatar and words:
                    st.subheader("🖐️ 3D Avatar")
                    if AVATAR_AVAILABLE:
                        generate_avatar_sign(text_clean)
                    else:
                        st.info("💡 3D Avatar is only available locally. Showing fingerspelling instead.")
                        for word in words:
                            st.write(f"*{word}* → {fingerspell_word(word)}")
                
                # ==================== VIDEO PLAYBACK ====================
                st.subheader("🎬 Sign Videos")
                videos = map_text_to_signs(words)
                if videos:
                    st.write(f"🎯 Found {len(videos)} sign(s)")
                    play_videos(videos)
                else:
                    st.warning("⚠️ No signs found for the given text.")
                    st.info("💡 Using fingerspelling for all words:")
                    for word in words:
                        st.write(f"*{word}* → {fingerspell_word(word)}")
            else:
                st.error("❌ Could not recognize speech. Please try again.")

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")