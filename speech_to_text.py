import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tempfile
import os
import time

def record_audio(duration=5, sample_rate=16000):
    """Record audio from microphone"""
    print("🎤 Recording... Speak now!")
    recording = sd.rec(int(duration * sample_rate), 
                       samplerate=sample_rate, 
                       channels=1, 
                       dtype='int16')
    sd.wait()
    print("✅ Recording complete!")
    return recording, sample_rate

def transcribe_audio_from_mic(duration=5):
    """Record and transcribe in one go"""
    audio_data, sr_rate = record_audio(duration)
    
    # Save to temp file
    tmp_path = tempfile.mktemp(suffix=".wav")
    wav.write(tmp_path, sr_rate, audio_data)
    
    # Transcribe
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
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
        finally:
            # Wait and delete
            time.sleep(0.2)
            try:
                os.remove(tmp_path)
            except:
                pass  # Ignore errors

def transcribe_audio_file(audio_file):
    """Transcribe an existing audio file"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
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

if __name__ == "__main__":
    result = transcribe_audio_file("voice_1.mp3")
    print("Result:", result)