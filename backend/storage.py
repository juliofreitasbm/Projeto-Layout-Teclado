import json
import unicodedata
from collections import defaultdict

class InputStorage:
    def __init__(self, filename="inputs.json"):
        self.filename = filename
        self.inputs = self.load_inputs()

    def load_inputs(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_input(self, text_input):
        self.inputs.append(text_input.to_dict())
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.inputs, file, indent=4, ensure_ascii=False)

    def get_inputs(self):
        return self.inputs

class LayoutStorage:
    def __init__(self, layout_filename="layout.json"):
        self.layout_filename = layout_filename
        self.layout = self.load_layout()

    def load_layout(self):
        try:
            with open(self.layout_filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
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
        try:
            with open(self.layout_filename, "w", encoding="utf-8") as file:
                json.dump(self.layout, file, indent=4, ensure_ascii=False)
            print("Layout salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar layout: {e}")

    def update_character_count(self, character_counts):
        for char, count in character_counts.items():
            if char in self.layout['character_count']:
                self.layout['character_count'][char] += count
        
        self.save_layout()

    def update_bigram_count(self, bigram_counts):
        for bigram, count in bigram_counts.items():
            if bigram not in self.layout['bigram_count']:
                self.layout['bigram_count'][bigram] = 0
            self.layout['bigram_count'][bigram] += count 

    def update_trigram_count(self, trigram_counts):
        for trigram, count in trigram_counts.items():
            if trigram not in self.layout['trigram_count']:
                self.layout['trigram_count'][trigram] = 0
            self.layout['trigram_count'][trigram] += count

    def update_matrix(self):
        total_character_count = self.layout["character_count"]

        total_character_count = {char.upper(): count for char, count in total_character_count.items()}

        valid_chars = set("QWERTYUIOPASDFGHJKLÇVBNM")
        vowels = ["A", "E", "I", "O", "U"]

        # Normalizar os caracteres: transformar tudo em maiusculo e remover acentos
        normalized_count = defaultdict(int)
        for char, count in total_character_count.items():
            normalized_char = unicodedata.normalize("NFD", char).encode("ascii", "ignore").decode("utf-8").upper()

            if normalized_char in valid_chars:
                normalized_count[normalized_char] += count

        # Ordenar as vogais (A, E, I, O, U) pela contagem de caracteres
        vowel_counts = {vowel: normalized_count[vowel] for vowel in vowels}
        sorted_vowels = sorted(vowels, key=lambda x: vowel_counts[x])

        # Preencher a linha do meio com as vogais em ordem de contagem
        self.layout['matrix'][1][0] = sorted_vowels[0]  
        self.layout['matrix'][1][1] = sorted_vowels[1]  
        self.layout['matrix'][1][2] = sorted_vowels[2]  
        self.layout['matrix'][1][3] = sorted_vowels[3]  
        self.layout['matrix'][1][4] = sorted_vowels[4]  

        # Preencher as consoantes com a ordem de prioridade, sem alterar posições fixas (como ZXC,.;)
        consonant_positions = [
            [1, 6], [1, 7], [1, 8], [1, 9], [1, 5], [2, 6], [2, 3], [0, 6], [0, 3], [0, 7],
            [0, 2], [0, 8], [0, 1], [0, 5], [0, 4], [2, 5], [2, 4], [0, 9], [0, 0]
        ]

        
        consonants_sorted = sorted(
            (char for char in normalized_count if char not in vowels), 
            key=lambda x: normalized_count[x]
        )
        print("consoantes:", consonants_sorted)

        # Preencher a matriz com as consoantes
        consonant_idx = 0
        for position in consonant_positions:
            # Verificar se ainda há consoantes para adicionar
            if consonant_idx < len(consonants_sorted):
                    self.layout['matrix'][position[0]][position[1]] = consonants_sorted[consonant_idx]
                    consonant_idx += 1
            else:
                break

        print(self.layout['matrix'])
        self.save_layout()

    def get_layout(self):
        return self.layout