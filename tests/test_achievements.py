from flashcards_cli.achievements import AchievementTracker
from flashcards_cli.model import Card


def test_speed_and_correct_are_calculated_from_current_round_only():
    card = Card("Question", "Answer")
    tracker = AchievementTracker()

    tracker.start_round()
    tracker.record(card, False, 10.0)
    assert tracker.check_achievements([card]) == []

    tracker.start_round()
    tracker.record(card, True, 1.0)
    earned = tracker.check_achievements([card])

    assert any("SPEED" in item for item in earned)
    assert any("CORRECT" in item for item in earned)


def test_repeat_and_confident_use_session_card_stats():
    card = Card("Question", "Answer")
    card.total_tries = 6
    card.success_count = 3
    tracker = AchievementTracker()

    earned = tracker.check_achievements([card])

    assert any("REPEAT" in item for item in earned)
    assert any("CONFIDENT" in item for item in earned)
