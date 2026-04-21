"""
Суралцах тойрог (Study Loop).

Картуудыг эрэмбэлэгчийн дагуу дараалуулж, хэрэглэгчээс хариултыг авч,
зөв/буруу эсэхийг шалгаж, статистик болон амжилтуудыг хянана.
"""
import time
import click

from .organizers import get_organizer
from .achievements import AchievementTracker


def study(deck, order="random", repetitions=1, invertcards=False):
    """
    Суралцах горимыг эхлүүлнэ.

    Args:
        deck: Deck объект (картуудын цуглуулга)
        order: Эрэмбэлэлтийн горим ("random", "worst-first", "recent-mistakes-first")
        repetitions: Нэг картыг хэдэн удаа зөв хариулахыг шаардах
        invertcards: True бол асуулт, хариултыг сольж харуулна
    """
    if not deck.cards:
        click.echo("Картууд олдсонгүй!")
        return

    organizer = get_organizer(order)
    tracker = AchievementTracker()

    click.echo("\n" + "=" * 40)
    click.echo("  📚 Суралцах горим эхэллээ!")
    click.echo(f"  Нийт карт: {len(deck.cards)}")
    click.echo(f"  Горим: {order}")
    click.echo(f"  Шаардлагатай зөв хариулт: {repetitions}")
    if invertcards:
        click.echo("  ↔ Асуулт/хариулт солигдсон")
    click.echo("=" * 40)
    click.echo("  (Гарахын тулд хоосон хариулт оруулна уу)\n")

    round_number = 0

    while True:
        # Тойрог бүрийн эхэнд картуудыг шинээр эрэмбэлнэ
        round_number += 1

        # Энэ тойрогт суралцах картуудыг шүүнэ:
        # repetitions-ээс бага зөв хариулттай картууд л үлдэнэ
        remaining = [c for c in deck.cards if c.success_count < repetitions]

        if not remaining:
            click.echo("\n🎉 Бүх картуудыг амжилттай дуусгалаа!")
            break

        ordered_cards = organizer.reorganize(remaining)

        click.echo(f"\n--- Тойрог #{round_number} ({len(ordered_cards)} карт үлдсэн) ---")

        for i, card in enumerate(ordered_cards, 1):
            # invertcards: асуулт/хариултыг солих
            if invertcards:
                display_question = card.answer
                correct_answer = card.question
            else:
                display_question = card.question
                correct_answer = card.answer

            click.echo(f"\n  Карт [{i}/{len(ordered_cards)}]")
            start_time = time.time()
            user_answer = click.prompt(f"  {display_question}", default="", show_default=False)
            elapsed = time.time() - start_time

            # Хоосон хариулт = гарах
            if not user_answer.strip():
                click.echo("\n  👋 Баяртай! Дараа уулзъя!")
                _show_stats(deck, tracker)
                return

            card.total_tries += 1

            if user_answer.strip().lower() == correct_answer.lower():
                card.success_count += 1
                card.last_result = True
                tracker.record(card, True, elapsed)
                click.echo(f"  ✅ Зөв! ({elapsed:.1f}с)")
            else:
                card.fail_count += 1
                card.last_result = False
                tracker.record(card, False, elapsed)
                click.echo(f"  ❌ Буруу! Зөв хариулт: {correct_answer} ({elapsed:.1f}с)")

        # Тойрог дууссаны дараа амжилтуудыг шалгана
        new_achievements = tracker.check_achievements(deck.cards)
        if new_achievements:
            click.echo("\n  🏆 Шинэ амжилт(ууд):")
            for a in new_achievements:
                click.echo(f"    {a}")

    # Бүх карт дуусвал
    _show_stats(deck, tracker)


def _show_stats(deck, tracker):
    """Суралцсаны дараах статистик харуулна."""
    click.echo("\n" + "=" * 40)
    click.echo("  📊 Статистик")
    click.echo("=" * 40)

    total_tries = sum(c.total_tries for c in deck.cards)
    total_correct = sum(c.success_count for c in deck.cards)
    total_wrong = sum(c.fail_count for c in deck.cards)

    click.echo(f"  Нийт оролдлого: {total_tries}")
    click.echo(f"  Зөв: {total_correct}")
    click.echo(f"  Буруу: {total_wrong}")

    if total_tries > 0:
        accuracy = (total_correct / total_tries) * 100
        click.echo(f"  Нарийвчлал: {accuracy:.1f}%")

    if tracker.earned:
        click.echo(f"\n  🏆 Авсан амжилтууд: {', '.join(tracker.earned)}")

    click.echo("=" * 40 + "\n")
