from speech_to_text import transcribe_audio_file, transcribe_audio_from_mic
from text_processor import process_text
from sign_mapper import map_text_to_signs
from play_sign import play_videos
import os

def main():
    print("=" * 50)
    print("🎬 VOICE TO SIGN LANGUAGE CONVERTER")
    print("=" * 50)
    
    # Choose input method
    choice = input("Choose option:\n1. Use existing audio file (voice_1.mp3)\n2. Record from microphone\nYour choice (1/2): ")
    
    if choice == "2":
        duration = int(input("Enter recording duration (seconds): "))
        text = transcribe_audio_from_mic(duration)
    else:
        if not os.path.exists("voice_1.mp3"):
            print("❌ voice_1.mp3 not found!")
            return
        text = transcribe_audio_file("voice_1.mp3")
    
    if not text:
        print("❌ No text recognized. Exiting.")
        return
    
    # Step 2: Process text
    print("\n📝 Step 2: Processing text...")
    processed_words = process_text(text)
    print(f"✅ Processed: {processed_words}")
    
    # Step 3: Map to signs
    print("\n🎯 Step 3: Mapping to sign language...")
    videos = map_text_to_signs(processed_words)
    
    if not videos:
        print("❌ No signs found for the given text.")
        return
    
    print(f"✅ Found {len(videos)} sign(s)")
    
    # Step 4: Play signs
    print("\n🎬 Step 4: Playing signs...")
    play_videos(videos)
    
    print("\n" + "=" * 50)
    print("✅ Translation completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()