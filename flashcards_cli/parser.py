from .model import Card, Deck


class ParseCardsError(ValueError):
    """Raised when a cards file cannot be parsed into a usable deck."""


def parse_cards_file(file_path):
    """Read a UTF-8 cards file and return a Deck.

    Expected format: one card per line, `Question | Answer`.
    """
    deck = Deck()

    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            text = f.read()
    except FileNotFoundError as exc:
        raise ParseCardsError(f"'{file_path}' файл олдсонгүй.") from exc
    except UnicodeDecodeError as exc:
        raise ParseCardsError(f"'{file_path}' файлыг UTF-8 encoding-оор уншиж чадсангүй.") from exc

    if "\\n" in text and "\n" not in text:
        text = text.replace("\\n", "\n")

    errors = []
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue

        if "|" not in line:
            errors.append(f"{line_number}-р мөр: 'Question | Answer' форматтай байх ёстой.")
            continue

        question, answer = [part.strip() for part in line.split("|", 1)]
        if not question or not answer:
            errors.append(f"{line_number}-р мөр: question болон answer хоёулаа хоосон биш байх ёстой.")
            continue

        deck.add_card(Card(question, answer))

    if errors:
        raise ParseCardsError("Картын файл буруу форматтай:\n" + "\n".join(errors))

    if not deck.cards:
        raise ParseCardsError("Картын файлд унших боломжтой карт алга.")

    return deck
