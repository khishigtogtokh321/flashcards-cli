import pytest

from flashcards_cli.parser import ParseCardsError, parse_cards_file


def test_parse_cards_file_reads_utf8_cards(tmp_path):
    cards_file = tmp_path / "cards.txt"
    cards_file.write_text("Асуулт 1 | Хариулт 1\nQuestion 2 | Answer 2\n", encoding="utf-8")

    deck = parse_cards_file(cards_file)

    assert [card.question for card in deck.cards] == ["Асуулт 1", "Question 2"]
    assert [card.answer for card in deck.cards] == ["Хариулт 1", "Answer 2"]


def test_parse_cards_file_reports_bad_lines(tmp_path):
    cards_file = tmp_path / "bad.txt"
    cards_file.write_text("Missing separator\nQuestion only |\n", encoding="utf-8")

    with pytest.raises(ParseCardsError) as excinfo:
        parse_cards_file(cards_file)

    message = str(excinfo.value)
    assert "1-р мөр" in message
    assert "2-р мөр" in message


def test_parse_cards_file_rejects_non_utf8(tmp_path):
    cards_file = tmp_path / "utf16.txt"
    cards_file.write_text("Question | Answer\n", encoding="utf-16")

    with pytest.raises(ParseCardsError, match="UTF-8"):
        parse_cards_file(cards_file)


def test_parse_cards_file_accepts_legacy_literal_newlines(tmp_path):
    cards_file = tmp_path / "literal.txt"
    cards_file.write_text("Question 1 | Answer 1\\nQuestion 2 | Answer 2", encoding="utf-8")

    deck = parse_cards_file(cards_file)

    assert len(deck.cards) == 2
