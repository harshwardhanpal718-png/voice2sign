def fingerspell_word(word):
    """Convert word to fingerspelling (letter by letter)"""
    alphabet_map = {
        'a': '🤟 A', 'b': '🤟 B', 'c': '🤟 C', 'd': '🤟 D',
        'e': '🤟 E', 'f': '🤟 F', 'g': '🤟 G', 'h': '🤟 H',
        'i': '🤟 I', 'j': '🤟 J', 'k': '🤟 K', 'l': '🤟 L',
        'm': '🤟 M', 'n': '🤟 N', 'o': '🤟 O', 'p': '🤟 P',
        'q': '🤟 Q', 'r': '🤟 R', 's': '🤟 S', 't': '🤟 T',
        'u': '🤟 U', 'v': '🤟 V', 'w': '🤟 W', 'x': '🤟 X',
        'y': '🤟 Y', 'z': '🤟 Z'
    }
    
    letters = []
    for char in word.lower():
        if char.isalpha():
            letters.append(alphabet_map.get(char, char))
        else:
            letters.append(char)
    
    return " → ".join(letters)

def fingerspell_sentence(sentence):
    """Convert each word to fingerspelling"""
    words = sentence.split()
    result = {}
    for word in words:
        result[word] = fingerspell_word(word)
    return result

if __name__ == "__main__":
    print(fingerspell_word("hello"))
    print(fingerspell_sentence("my name is harsh"))