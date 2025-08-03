import re
from better_profanity import profanity
from pathlib import Path

class ProfanityFilter:
    def __init__(self, banned_words_file: str):
        self.banned_words_file = banned_words_file
        self._load_and_set_censor_words()

    def _load_banned_words(self) -> list[str]:
        try:
            with open(Path.cwd() / "src" / self.banned_words_file, "r", encoding="utf-8") as file:
                words = [line.strip().lower() for line in file if line.strip()]
            return words
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл с запрещёнными словами не найден: {self.banned_words_file}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при чтении файла {self.banned_words_file}: {e}")

    def _load_and_set_censor_words(self):
        banned_words = self._load_banned_words()
        profanity.add_censor_words(banned_words)

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def contains_profanity(self, text: str) -> bool:
        normalized_text = self.normalize(text)
        return profanity.contains_profanity(normalized_text)

    def censor(self, text: str) -> str:
        normalized_text = self.normalize(text)
        return profanity.censor(normalized_text)
    
