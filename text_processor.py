import re


STOP_WORDS = {
    "i",
    "am",
    "is",
    "are",
    "the",
    "a",
    "an",
    "to",
    "of",
    "and",
    "in",
    "on",
    "for"
}


def clean_text(text):
    """
    Cleans raw speech text.
    """

    text = text.lower().strip()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


def process_text(text):
    """
    Converts raw sentence into meaningful words.
    """

    text = clean_text(text)

    words = text.split()

    processed_words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    return processed_words


if __name__ == "__main__":

    sample = "Hello, my name is Harsh!"

    print("Original:", sample)
    print("Processed:", process_text(sample))