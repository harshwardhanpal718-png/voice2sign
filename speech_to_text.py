import speech_recognition as sr
import tempfile
import os
from pydub import AudioSegment

def transcribe_audio_file(audio_file):
    """Transcribe audio file (supports MP3, WAV, M4A)"""
    try:
        file_extension = os.path.splitext(audio_file)[1].lower()
        
        # Handle MP3 and other formats
        if file_extension in ['.mp3', '.m4a', '.wav', '.flac']:
            print(f"🔄 Processing {file_extension} file...")
            audio = AudioSegment.from_file(audio_file)
            wav_path = tempfile.mktemp(suffix=".wav")
            audio.export(wav_path, format="wav")
            audio_file = wav_path
            print("✅ Conversion complete!")
        
        # Transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio)
                print(f"📝 Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return ""
            except sr.RequestError:
                print("❌ API request failed")
                return ""
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return ""
    finally:
        if 'wav_path' in locals():
            try:
                os.remove(wav_path)
            except:
                pass

def transcribe_audio_from_mic(duration=5):
    """Microphone feature only works locally"""
    return "Microphone feature is only available when running locally."

if _name_ == "_main_":
    result = transcribe_audio_file("voice_1.mp3")
    print("Result:", result)