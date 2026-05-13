import pytest

from flashcards_cli.model import Card
from flashcards_cli.organizers import RecentMistakesFirstSorter, WorstFirstSorter, get_organizer


def test_worst_first_sorter_orders_by_fail_count_descending():
    easy = Card("easy", "answer")
    hard = Card("hard", "answer")
    medium = Card("medium", "answer")
    easy.fail_count = 0
    hard.fail_count = 3
    medium.fail_count = 1

    ordered = WorstFirstSorter().reorganize([easy, hard, medium])

    assert ordered == [hard, medium, easy]


def test_recent_mistakes_first_moves_only_last_wrong_cards_to_front():
    first = Card("first", "answer")
    wrong = Card("wrong", "answer")
    unseen = Card("unseen", "answer")
    second_wrong = Card("second wrong", "answer")
    first.last_result = True
    wrong.last_result = False
    second_wrong.last_result = False

    ordered = RecentMistakesFirstSorter().reorganize([first, wrong, unseen, second_wrong])

    assert ordered == [wrong, second_wrong, first, unseen]


def test_get_organizer_rejects_unknown_order():
    with pytest.raises(ValueError):
        get_organizer("missing")
