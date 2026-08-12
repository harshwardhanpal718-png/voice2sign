import os

def map_text_to_signs(words):
    """Map processed words to sign video paths"""
    sign_map = {
        "hello": "signs/hello.mp4",
        "help": "signs/Help.mp4",
        "please": "signs/Please.mp4",
        "thank you": "signs/Thank_You.mp4",
        "water": "signs/Water.mp4",
        "yes": "signs/Yes.mp4",
        "no": "signs/No_(Sign_2).mp4",
        "my name is": "signs/my_name_is.mp4",
        "bad": "signs/Bad.mp4",
        "food": "signs/Food.mp4",
        "you": "signs/You.mp4",
        "welcome": "signs/Welcome_(Reply_to_...).mp4"
    }
    
    videos = []
    for word in words:
        word_lower = word.lower()
        if word_lower in sign_map:
            videos.append({
                "name": word_lower,
                "path": sign_map[word_lower]
            })
        else:
            print(f"⚠️ Sign not found for: {word}")
    
    return videos