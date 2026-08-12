def map_sentence_to_signs(sentence):
    """Break sentence into signs and map"""
    words = sentence.lower().split()
    
    # ISL grammar: Object-Subject-Verb (OSV)
    isl_style = words[::-1]
    
    sign_map = {
        "hello": "👋",
        "help": "🆘",
        "please": "🙏",
        "thank": "🙏",
        "you": "👉",
        "water": "💧",
        "food": "🍽️",
        "name": "📛",
        "my": "🤚",
        "is": "✅",
        "yes": "👍",
        "no": "👎",
        "bad": "👎",
        "welcome": "🤗"
    }
    
    signs = []
    for word in isl_style:
        signs.append(sign_map.get(word, f"❓{word}"))
    
    return signs

def get_sign_emoji(word):
    """Return emoji for a single word"""
    sign_map = {
        "hello": "👋",
        "help": "🆘",
        "please": "🙏",
        "thank": "🙏",
        "you": "👉",
        "water": "💧",
        "food": "🍽️",
        "name": "📛",
        "my": "🤚",
        "is": "✅",
        "yes": "👍",
        "no": "👎",
        "bad": "👎",
        "welcome": "🤗"
    }
    return sign_map.get(word.lower(), f"❓{word}")

if _name_ == "_main_":
    print(map_sentence_to_signs("my name is harsh"))