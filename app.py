import streamlit as st
from speech_to_text import transcribe_audio_file, transcribe_audio_from_mic
from text_processor import process_text
from sign_mapper import map_text_to_signs
from play_sign import play_videos
from sentence_mapper import get_sign_emoji
from fingerspell import fingerspell_word
import os
import tempfile
import time

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Voice to Sign Language", 
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS (Purple Galaxy Theme) ==========
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1a0b2e, #3d1f6e, #6c3cb0);
        color: #ffffff;
    }
    
    /* Main Title */
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #e0aaff, #c77dff, #9d4edd, #7b2cbf);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    .sub-title {
        text-align: center;
        color: rgba(255,255,255,0.7);
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    /* Cards */
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(157, 78, 221, 0.3);
        border-color: rgba(157, 78, 221, 0.4);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #9d4edd, #7b2cbf);
        color: #ffffff;
        font-weight: 700;
        border-radius: 50px;
        padding: 12px 35px;
        border: none;
        transition: all 0.3s ease;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(157, 78, 221, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(157, 78, 221, 0.5);
        background: linear-gradient(90deg, #7b2cbf, #9d4edd);
    }
    
    .stButton > button:active {
        transform: scale(0.95);
    }
    
    /* File Uploader */
    .upload-container {
        border: 2px dashed rgba(157, 78, 221, 0.3);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.02);
    }
    
    .upload-container:hover {
        border-color: #9d4edd;
        background: rgba(157, 78, 221, 0.05);
    }
    
    /* Success/Error/Info Boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid;
        backdrop-filter: blur(10px);
        background: rgba(255,255,255,0.05);
    }
    
    .stSuccess {
        border-left-color: #9d4edd;
        color: #e0aaff;
    }
    
    .stError {
        border-left-color: #ff4757;
        color: #ff6b81;
    }
    
    .stWarning {
        border-left-color: #ffd200;
        color: #ffd200;
    }
    
    .stInfo {
        border-left-color: #7b2cbf;
        color: #c77dff;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(26, 11, 46, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(157, 78, 221, 0.2);
    }
    
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e0aaff;
        margin-bottom: 20px;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: rgba(255,255,255,0.9);
        font-weight: 500;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: rgba(255,255,255,0.9);
        font-weight: 500;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #7b2cbf, #9d4edd, #c77dff) !important;
        border-radius: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: rgba(255,255,255,0.3);
        font-size: 0.9rem;
        border-top: 1px solid rgba(157, 78, 221, 0.1);
        margin-top: 40px;
    }
    
    .footer a {
        color: #c77dff;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
        color: #e0aaff;
    }
    
    /* Feature boxes */
    .feature-box {
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(157, 78, 221, 0.1);
    }
    
    .feature-box h4 {
        color: #c77dff;
        margin-bottom: 15px;
    }
    
    /* Word chips */
    .word-chip {
        display: inline-block;
        background: rgba(157, 78, 221, 0.2);
        color: #e0aaff;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 3px;
        font-size: 0.9rem;
        border: 1px solid rgba(157, 78, 221, 0.2);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease forwards;
    }
</style>
""", unsafe_allow_html=True)

# ========== AVATAR IMPORT (Cloud Safe) ==========
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

# ========== TITLE SECTION ==========
st.markdown('<p class="main-title">🎬 Voice to Sign Language</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Convert your voice into Indian Sign Language (ISL) videos in real-time</p>', unsafe_allow_html=True)
st.markdown("---")

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown('<p class="sidebar-title">⚙️ Settings</p>', unsafe_allow_html=True)
    
    option = st.radio(
        "Choose input method:",
        ["📁 Upload Audio File", "🎤 Record from Microphone"],
        index=0
    )
    
    if option == "🎤 Record from Microphone":
        duration = st.slider("⏱️ Recording duration (seconds)", 3, 10, 5, value=5)
    
    st.markdown("---")
    st.markdown("### 🔧 Features")
    show_avatar = st.checkbox("🖐️ 3D Avatar", value=True)
    show_fingerspell = st.checkbox("🔤 Fingerspelling", value=True)
    show_isl_style = st.checkbox("🔄 ISL Style (OSV)", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.markdown("""
    - *Words Supported:* 15+
    - *Languages:* English → ISL
    - *Status:* ✅ Active
    """)

# ========== MAIN CONTENT ==========
if option == "📁 Upload Audio File":
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    
    st.markdown("### 📂 Upload Your Audio File")
    st.markdown("Supported formats: *MP3, WAV, M4A* (Max: 200MB)")
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["mp3", "wav", "m4a"],
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        
        # File info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 File Name", uploaded_file.name[:30] + "..." if len(uploaded_file.name) > 30 else uploaded_file.name)
        with col2:
            st.metric("📊 File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col3:
            st.metric("📁 Format", uploaded_file.type or "Unknown")
        
        if st.button("🚀 Process Audio", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("💾 Saving file...")
                progress_bar.progress(10)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                    tmpfile.write(uploaded_file.read())
                    tmp_path = tmpfile.name
                
                status_text.text("🎤 Transcribing audio...")
                progress_bar.progress(30)
                time.sleep(0.5)
                
                text = transcribe_audio_file(tmp_path)
                
                if text:
                    status_text.text("🧠 Processing text...")
                    progress_bar.progress(60)
                    time.sleep(0.5)
                    
                    words = process_text(text)
                    text_clean = " ".join(words)
                    
                    status_text.text("✨ Generating results...")
                    progress_bar.progress(80)
                    time.sleep(0.5)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Done!")
                    
                    st.balloons()
                    st.success(f"✅ *Recognized:* {text}")
                    st.write(f"*Processed Words:* {' '.join([f'<span class="word-chip">{w}</span>' for w in words])}", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if show_fingerspell and words:
                            st.markdown('<div class="feature-box">', unsafe_allow_html=True)
                            st.markdown("#### 🔤 Fingerspelling")
                            for word in words:
                                st.write(f"*{word}* → {fingerspell_word(word)}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        if show_isl_style and words:
                            st.markdown('<div class="feature-box">', unsafe_allow_html=True)
                            st.markdown("#### 🔄 ISL Style (OSV)")
                            isl_words = words[::-1]
                            isl_emojis = [get_sign_emoji(w) for w in isl_words]
                            st.write(" → ".join(isl_emojis))
                            st.write(f"*ISL:* {' → '.join(isl_words)}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    if show_avatar and words:
                        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
                        st.markdown("#### 🖐️ 3D Avatar")
                        if AVATAR_AVAILABLE:
                            generate_avatar_sign(text_clean)
                        else:
                            st.info("💡 3D Avatar is only available locally. Showing fingerspelling instead.")
                            for word in words:
                                st.write(f"*{word}* → {fingerspell_word(word)}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
                    st.markdown("#### 🎬 Sign Videos")
                    videos = map_text_to_signs(words)
                    if videos:
                        st.write(f"🎯 Found {len(videos)} sign(s)")
                        play_videos(videos)
                    else:
                        st.warning("⚠️ No signs found for the given text.")
                        st.info("💡 Using fingerspelling for all words:")
                        for word in words:
                            st.write(f"*{word}* → {fingerspell_word(word)}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 Download Result",
                        data=text,
                        file_name="recognized_text.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                else:
                    progress_bar.progress(100)
                    status_text.text("❌ Failed")
                    st.error("❌ Could not recognize speech. Please try again.")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
            
            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.markdown("### 🎤 Record from Microphone")
    st.info("ℹ️ This feature works best on local machine. On cloud, it will show a fallback message.")
    
    if st.button("🎤 Start Recording", use_container_width=True):
        with st.spinner(f"🎧 Recording for {duration} seconds..."):
            text = transcribe_audio_from_mic(duration)
            
            if text:
                words = process_text(text)
                st.success(f"✅ *Recognized:* {text}")
                
                st.markdown("#### 🔤 Fingerspelling (Fallback)")
                for word in words:
                    st.write(f"*{word}* → {fingerspell_word(word)}")
            else:
                st.error("❌ Could not recognize speech. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("""
<div class="footer">
    Made with ❤️ using Streamlit & Python | 
    <a href="https://github.com/harshwardhanpal718-png/voice2sign" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)