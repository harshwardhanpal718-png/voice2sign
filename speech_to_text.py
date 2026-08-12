import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment

# Cloud par microphone available nahi hai
MIC_AVAILABLE = False

def transcribe_audio_file(audio_file):
    """Transcribe audio file (supports MP3, WAV, M4A)"""
    try:
        # Agar MP3/M4A hai toh WAV mein convert karo
        if audio_file.endswith('.mp3') or audio_file.endswith('.m4a'):
            print("🔄 Converting to WAV...")
            audio = AudioSegment.from_file(audio_file)
            wav_path = tempfile.mktemp(suffix=".wav")
            audio.export(wav_path, format="wav")
            audio_file = wav_path
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except Exception as e:
        print(f"Error: {e}")
        return ""

def transcribe_audio_from_mic(duration=5):
    """Microphone feature only works locally"""
    return "🎤 Microphone feature is only available when running locally."

if __name__ == "__main__":
    result = transcribe_audio_file("voice_1.mp3")
    print("Result:", result)