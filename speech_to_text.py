import speech_recognition as sr

def transcribe_audio_file(audio_file):
    """Transcribe audio file with detailed logging"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            print(f"🎤 File loaded: {audio_file}")
            print(f"📊 Duration: {source.DURATION} seconds")
            
            print("🔧 Adjusting for noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("🎙️ Recording audio...")
            audio = recognizer.record(source)
            print(f"📦 Audio data captured: {len(audio.frame_data)} bytes")
            
            print("🌐 Sending to Google API...")
            text = recognizer.recognize_google(audio, language="en-IN", show_all=True)
            print(f"📝 Google response: {text}")
            
            if text and isinstance(text, dict) and 'alternative' in text:
                best_text = text['alternative'][0]['transcript']
                print(f"✅ Recognized: {best_text}")
                return best_text
            else:
                print("❌ No text recognized")
                return ""
                
    except sr.UnknownValueError:
        print("❌ Could not understand audio — Google API couldn't parse")
        return ""
    except sr.RequestError as e:
        print(f"❌ API request failed: {e}")
        print("💡 Check internet connection and try again")
        return ""
    except FileNotFoundError:
        print(f"❌ File not found: {audio_file}")
        return ""
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return ""

def transcribe_audio_from_mic(duration=5):
    return "Microphone feature is only available when running locally."

if __name__ == "__main__":
    result = transcribe_audio_file("hello.wav")
    print(f"🎯 Final Result: {result}")