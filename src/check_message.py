import re
from better_profanity import profanity

def bad_words_pars(file: str) -> list[str]:
    with open(file, "r") as f:
        arr = []
        for line in f:
            arr.append(line.strip())
    return arr

profanity.add_censor_words(bad_words_pars("ban.txt"))

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def contains_profanity(text: str) -> bool:
    return profanity.contains_profanity(normalize(text))