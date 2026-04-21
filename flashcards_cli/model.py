class Card:
    """Нэг ширхэг флаш картыг төлөөлөх класс"""
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.success_count = 0  
        self.fail_count = 0     
        self.total_tries = 0    
        self.last_result = None 

class Deck:
    """Картуудын цуглуулгыг төлөөлөх класс"""
    def __init__(self, cards=None):
        self.cards = cards or []

    def add_card(self, card):
        self.cards.append(card)
