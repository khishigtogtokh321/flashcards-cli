"""
Flashcard CLI - Командын мөрийн интерфейс.

PDF Даалгавар 1: flashcard <cards-file> [options]
"""
import click
from .parser import parse_cards_file
from .study import study


@click.command()
@click.argument('cards_file', type=click.Path(exists=True))
@click.option('--order', default='random',
              type=click.Choice(['random', 'worst-first', 'recent-mistakes-first']),
              help='Зохион байгуулалтын төрөл (default: random)')
@click.option('--repetitions', default=1, type=int,
              help='Нэг картыг хэдэн удаа зөв хариулахыг тохируулна (default: 1)')
@click.option('--invertcards', is_flag=True, default=False,
              help='Картын асуулт, хариултыг сольж харуулна')
def main(cards_file, order, repetitions, invertcards):
    """
    Flashcard сургах систем - CSA311 Бие даалт.

    CARDS_FILE: Картууд бүхий текст файл (формат: Асуулт | Хариулт)
    """
    # Файлыг уншиж Deck болгох
    deck = parse_cards_file(cards_file)
    if not deck or not deck.cards:
        click.echo("Алдаа: Файлаас картууд уншигдсангүй.")
        return

    click.echo(f"\n📂 '{cards_file}' файлаас {len(deck.cards)} карт уншигдлаа.")

    # Суралцах горимыг эхлүүлнэ
    study(deck, order=order, repetitions=repetitions, invertcards=invertcards)


if __name__ == "__main__":
    main()
