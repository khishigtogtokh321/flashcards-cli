"""
Flashcard CLI - Командын мөрийн интерфейс.

PDF Даалгавар 1: flashcard <cards-file> [options]
"""
import sys

import click

from .parser import ParseCardsError, parse_cards_file
from .study import study


def _configure_stdio_for_unicode():
    """Prevent Windows code-page consoles from crashing on Mongolian help text."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(errors="replace")
        except (OSError, ValueError):
            pass


_configure_stdio_for_unicode()


@click.command()
@click.argument('cards_file', type=click.Path(exists=True))
@click.option('--order', default='random',
              type=click.Choice(['random', 'worst-first', 'recent-mistakes-first']),
              help='Зохион байгуулалтын төрөл (default: random)')
@click.option('--repetitions', default=1, type=int,
              help='Нэг картыг хэдэн удаа зөв хариулахыг тохируулна (default: 1)')
@click.option('--invertCards', '--invertcards', 'invertcards', is_flag=True, default=False,
              help='Картын асуулт, хариултыг сольж харуулна')
def main(cards_file, order, repetitions, invertcards):
    """
    CARDS_FILE: Картууд бүхий текст файл (формат: Асуулт | Хариулт)
    """
    # Файлыг уншиж Deck болгох
    try:
        deck = parse_cards_file(cards_file)
    except ParseCardsError as exc:
        click.echo(f"Алдаа: {exc}", err=True)
        return

    click.echo(f"\n '{cards_file}' файлаас {len(deck.cards)} карт уншигдлаа.")

    # Суралцах горимыг эхлүүлнэ
    study(deck, order=order, repetitions=repetitions, invertcards=invertcards)


if __name__ == "__main__":
    main()
