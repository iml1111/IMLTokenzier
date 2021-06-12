import re


class Refiner:
    """Refiner Class"""

    def __init__(
        self,
        low=True,
        emoji=True,
        special_char=True,
        whitespace=True,
    ):
        self.low = low
        self.emoji = emoji
        self.special_char = special_char
        self.whitespace = whitespace

        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F" # emoticons
            u"\U0001F300-\U0001F5FF" # symbols & pictographs
            u"\U0001F680-\U0001F6FF" # transport & map symbols
            u"\U0001F1E0-\U0001F1FF" # flags (iOS)
        "]+", flags=re.UNICODE)

    def char_filter(self, phrase: str):
        """Refine Text."""
        phrase = phrase.strip()
        if self.low:
            phrase = phrase.lower()
        if self.emoji:
            phrase = self.emoji_pattern.sub(r' ', phrase)
        if self.special_char:
            phrase = re.sub(r'[^ ㄱ-ㅣ가-힣|a-z|0-9|:]+', ' ', phrase)
        if self.whitespace:
            phrase = re.sub(r'\s+', ' ', phrase)

        return phrase

    def token_filter(self, tokens: list):
        pass