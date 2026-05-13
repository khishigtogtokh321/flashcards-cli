import importlib

from click.testing import CliRunner

main_module = importlib.import_module("flashcards_cli.main")


def test_cli_help_shows_pdf_command_and_invertcards_alias():
    result = CliRunner().invoke(main_module.main, ["--help"])

    assert result.exit_code == 0
    assert "CARDS_FILE" in result.output
    assert "--invertCards" in result.output
    assert "--invertcards" in result.output


def test_cli_accepts_camelcase_invertcards_alias(monkeypatch, tmp_path):
    calls = {}
    cards_file = tmp_path / "cards.txt"
    cards_file.write_text("Question | Answer\n", encoding="utf-8")
    deck = type("Deck", (), {"cards": [object()]})()

    monkeypatch.setattr(main_module, "parse_cards_file", lambda path: deck)
    monkeypatch.setattr(main_module, "study", lambda deck, **kwargs: calls.update(kwargs))

    result = CliRunner().invoke(main_module.main, [str(cards_file), "--invertCards"])

    assert result.exit_code == 0
    assert calls["invertcards"] is True


def test_cli_reports_parser_errors(monkeypatch, tmp_path):
    cards_file = tmp_path / "cards.txt"
    cards_file.write_text("Question | Answer\n", encoding="utf-8")
    monkeypatch.setattr(
        main_module,
        "parse_cards_file",
        lambda path: (_ for _ in ()).throw(main_module.ParseCardsError("bad file")),
    )

    result = CliRunner().invoke(main_module.main, [str(cards_file)])

    assert result.exit_code == 0
    assert "Алдаа: bad file" in result.output
