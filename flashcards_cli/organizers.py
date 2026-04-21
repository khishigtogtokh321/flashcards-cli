"""
CardOrganizer интерфейс ба эрэмбэлэгч классууд.

PDF Даалгавар 2: CardOrganizer интерфейсийг тодорхойлж классуудаар хэрэгжүүлэх.
"""
import random
from abc import ABC, abstractmethod


class CardOrganizer(ABC):
    """
    Картуудыг эрэмбэлэх абстракт суурь класс (интерфейс).
    Бүх эрэмбэлэгч классууд энэ интерфейсийг хэрэгжүүлнэ.
    """

    @abstractmethod
    def reorganize(self, cards):
        """
        Картуудыг эрэмбэлж шинэ жагсаалт буцаана.

        Args:
            cards: Card объектуудын жагсаалт

        Returns:
            Эрэмбэлэгдсэн картуудын жагсаалт
        """
        pass


class RandomSorter(CardOrganizer):
    """Картуудыг санамсаргүй дарааллаар эрэмбэлнэ."""

    def reorganize(self, cards):
        shuffled = list(cards)
        random.shuffle(shuffled)
        return shuffled


class WorstFirstSorter(CardOrganizer):
    """
    Хамгийн олон удаа буруу хариулсан картуудыг эхэнд байрлуулна.
    Буруу хариултын тоо ижил бол анхны дарааллыг хадгална.
    """

    def reorganize(self, cards):
        # stable sort: fail_count өндөр байх тусам эхэнд гарна
        return sorted(cards, key=lambda c: c.fail_count, reverse=True)


class RecentMistakesFirstSorter(CardOrganizer):
    """
    PDF-ийн шаардлага: "Өмнөх шатанд буруу хариулсан картууд эхэнд
    гарч ирнэ. Харин зөв, буруу хариулсан картуудын дотоод дараалал
    өөрчлөгдөхгүй."

    Өөрөөр хэлбэл:
    - Сүүлийн тойрогт буруу хариулсан картууд → эхэнд (дотоод дараалал хэвээр)
    - Сүүлийн тойрогт зөв хариулсан эсвэл үзээгүй картууд → дараа нь (дотоод дараалал хэвээр)
    """

    def reorganize(self, cards):
        wrong = [c for c in cards if c.last_result is False]
        rest = [c for c in cards if c.last_result is not False]
        return wrong + rest


def get_organizer(order_name):
    """
    Нэрээр нь эрэмбэлэгч объект буцаана.

    Args:
        order_name: "random", "worst-first", "recent-mistakes-first"

    Returns:
        CardOrganizer объект
    """
    organizers = {
        "random": RandomSorter(),
        "worst-first": WorstFirstSorter(),
        "recent-mistakes-first": RecentMistakesFirstSorter(),
    }
    if order_name not in organizers:
        raise ValueError(f"'{order_name}' гэсэн эрэмбэлэгч олдсонгүй. "
                         f"Боломжит сонголтууд: {list(organizers.keys())}")
    return organizers[order_name]
