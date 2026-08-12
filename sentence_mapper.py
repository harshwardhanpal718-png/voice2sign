def map_sentence_to_signs(sentence):
    """Break sentence into signs and map"""
    words = sentence.lower().split()
    
    # ISL grammar: Object-Subject-Verb (OSV)
    # For now, we just reverse order (basic ISL style)
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
        "is": "✅"
    }
    
    signs = []
    for word in isl_style:
        signs.append(sign_map.get(word, f"❓{word}"))
    
    return signs

# Test
if _name_ == "_main_":
    print(map_sentence_to_signs("my name is harsh"))  # ISL style: harsh is name my