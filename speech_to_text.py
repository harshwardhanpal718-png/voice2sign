import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment
import subprocess

def transcribe_audio_file(audio_file):
    """Transcribe audio file (supports MP3, WAV, M4A)"""
    try:
        file_extension = os.path.splitext(audio_file)[1].lower()
        
        # Handle MP3 and other formats
        if file_extension in ['.mp3', '.m4a', '.wav', '.flac']:
            print(f"🔄 Processing {file_extension} file...")
            
            # Convert to WAV using pydub
            audio = AudioSegment.from_file(audio_file)
            wav_path = tempfile.mktemp(suffix=".wav")
            audio.export(wav_path, format="wav")
            audio_file = wav_path
            print("✅ Conversion complete!")
        
        # Transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)
            
            # Try different recognizers for better accuracy
            try:
                text = recognizer.recognize_google(audio)
                print(f"📝 Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return "Could not understand audio"
            except sr.RequestError:
                print("❌ API request failed")
                return "API request failed"
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Error: {str(e)}"
    finally:
        # Clean up temp files
        if 'wav_path' in locals():
            try:
                os.remove(wav_path)
            except:
                pass