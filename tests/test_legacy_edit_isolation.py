import importlib

import pytest


def test_legacy_edit_modules_import_without_flashcards_core():
    edit = importlib.import_module("flashcards_cli.edit")
    cards = importlib.import_module("flashcards_cli.edit.cards")
    decks = importlib.import_module("flashcards_cli.edit.decks")

    assert callable(edit.edit)
    assert callable(cards.edit_cards)
    assert callable(decks.edit_decks)


def test_legacy_edit_functions_fail_with_clear_message():
    cards = importlib.import_module("flashcards_cli.edit.cards")

    with pytest.raises(RuntimeError, match="standalone CLI"):
        cards.edit_cards(None, None)
