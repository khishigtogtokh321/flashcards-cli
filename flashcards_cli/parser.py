from .model import Card, Deck

def parse_cards_file(file_path):
    """Текст файлыг уншиж Deck объект болгон хувиргах"""
    deck = Deck()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '|' not in line:
                    continue  # Хоосон мөр эсвэл буруу форматыг алгасах
                
                question, answer = line.split('|', 1)
                card = Card(question.strip(), answer.strip())
                deck.add_card(card)
        return deck
    except FileNotFoundError:
        print(f"Error: '{file_path}' файл олдсонгүй.")
        return None
