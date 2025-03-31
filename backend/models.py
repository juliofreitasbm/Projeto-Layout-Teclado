import json
import string
import unicodedata
from collections import defaultdict

class TextInput:
    def __init__(self, text: str = None, filename: str = None, layout_filename="layout.json"):
        self.text = text
        self.filename = filename 
        self.character_count = defaultdict(int)
        self.bigram_count = defaultdict(int)
        self.trigram_count = defaultdict(int)
        
        if text:
            self.process_text(text)
        
        self.layout_filename = layout_filename
        self.layout = self.load_layout()

    def process_text(self, text: str):
        text_normalized = text.lower()

        # Contagem de caracteres, bigramas e trigramas
        for i, char in enumerate(text_normalized):
            
            if char.isalnum() or char in string.punctuation:
                self.character_count[char] += 1

        words = text_normalized.split()

        for word in words:
            word = ''.join(c for c in word if c.isalpha())

            for i in range(len(word) - 1):
                bigram = word[i:i+2]
                if all(c.isalpha() for c in bigram): 
                    self.bigram_count[bigram] += 1

            for i in range(len(word) - 2):
                trigram = word[i:i+3]
                if all(c.isalpha() for c in trigram):  
                    self.trigram_count[trigram] += 1

    def to_dict(self):
        return {
            "filename": self.filename,  
            "character_count": dict(self.character_count),
            "bigram_count": dict(self.bigram_count),
            "trigram_count": dict(self.trigram_count),
        }
    
    def load_layout(self):
        try:
            with open(self.layout_filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Caso o layout não exista, retorna um layout padrão (QWERTY)
            return {
                "name": "LAYOUT",
                "matrix": [
                    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ç"],
                    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", ";"]
                ],
                "character_count": {
                    "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0,
                    "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0,
                    "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0, "ç": 0
                },
                "bigram_count": {},
                "trigram_count": {}
            }

    def save_layout(self):
        with open(self.layout_filename, "w", encoding="utf-8") as file:
            json.dump(self.layout, file, indent=4, ensure_ascii=False)

    def get_layout(self):
        return self.layout