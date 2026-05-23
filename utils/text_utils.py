import re


class Utils:

    @staticmethod
    def normalize_text(text: str) -> list[str]:
        text = text.lower()
        text = re.sub(r"\[\d+]", "", text)
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text.split()

    @staticmethod
    def count_unique_words(text: str) -> int:
        words = Utils.normalize_text(text)
        return len(set(words))