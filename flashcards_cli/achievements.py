"""
Амжилтын систем (Achievements).

PDF Даалгавар 3: Нэмэлт амжилтууд хэрэгжүүлэх.
- SPEED:     Нэг тойрогт дундаж 5 секундээс доош хугацаанд хариулсан.
- CORRECT:   Сүүлийн тойрогт бүх карт зөв хариулсан.
- REPEAT:    Нэг картад 5-аас олон удаа хариулсан.
- CONFIDENT: Нэг картад дор хаяж 3 удаа зөв хариулсан.
"""


class AchievementTracker:
    """Суралцах горимын статистикийг хянаж, амжилтуудыг шалгана."""

    def __init__(self):
        self.round_results = []      # Тойрог дахь (card, is_correct, time) бүртгэлүүд
        self.earned = []             # Авсан амжилтуудын жагсаалт

    def record(self, card, is_correct, elapsed_time):
        """Нэг хариултын үр дүнг бүртгэх."""
        self.round_results.append({
            "card": card,
            "correct": is_correct,
            "time": elapsed_time,
        })

    def check_achievements(self, cards):
        """
        Тойрог дууссаны дараа бүх амжилтуудыг шалгана.

        Args:
            cards: Бүх картуудын жагсаалт (Deck.cards)

        Returns:
            Шинээр авсан амжилтуудын жагсаалт
        """
        newly_earned = []

        # SPEED: Дундаж хариулах хугацаа < 5 секунд
        if self.round_results:
            avg_time = sum(r["time"] for r in self.round_results) / len(self.round_results)
            if avg_time < 5.0 and "SPEED" not in self.earned:
                self.earned.append("SPEED")
                newly_earned.append(
                    "⚡ SPEED: Дундаж хариулах хугацаа 5 секундээс бага байна!"
                )

        # CORRECT: Сүүлийн тойрогт бүх карт зөв хариулсан
        if self.round_results:
            all_correct = all(r["correct"] for r in self.round_results)
            if all_correct and "CORRECT" not in self.earned:
                self.earned.append("CORRECT")
                newly_earned.append(
                    "✅ CORRECT: Бүх картыг зөв хариуллаа!"
                )

        # REPEAT: Нэг картад 5-аас олон удаа хариулсан
        for card in cards:
            if card.total_tries > 5 and "REPEAT" not in self.earned:
                self.earned.append("REPEAT")
                newly_earned.append(
                    f"🔁 REPEAT: '{card.question}' картыг {card.total_tries} удаа хариуллаа!"
                )
                break

        # CONFIDENT: Нэг картад дор хаяж 3 удаа зөв хариулсан
        for card in cards:
            if card.success_count >= 3 and "CONFIDENT" not in self.earned:
                self.earned.append("CONFIDENT")
                newly_earned.append(
                    f"💪 CONFIDENT: '{card.question}' картыг 3+ удаа зөв хариуллаа!"
                )
                break

        return newly_earned
