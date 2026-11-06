# === Stage 3: Хранилище в памяти ===
# Project: BakeryOrders
memory_store.py

from typing import Dict, List, Optional, TypeVar, Generic

T = TypeVar("T")


class MemoryStore(Generic[T]):
    """Хранилище сущностей в оперативной памяти.

    Поддерживает добавление объектов с уникальными идентификаторами,
    получение объекта по идентификатору и извлечение полного списка.
    """

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}

    def add(self, identifier: str, item: T) -> None:
        if identifier in self._items:
            raise ValueError(f"Позиция с идентификатором '{identifier}' уже существует")
        self._items[identifier] = item

    def get(self, identifier: str) -> Optional[T]:
        return self._items.get(identifier)

    def list_all(self) -> List[T]:
        return list(self._items.values())

    def delete(self, identifier: str) -> bool:
        removed = self._items.pop(identifier, None)
        return removed is not None


class Order:
    """Заказ небольшой пекарни.

    Поля:
        identifier - уникальный идентификатор заказа
        client - имя клиента
        date - дата создания заказа
        amount - сумма заказа
        status - текущий статус заказа
    """

    def __init__(self, identifier: str, client: str, date: str,
                 amount: float, status: str) -> None:
        self.identifier = identifier
        self.client = client
        self.date = date
        self.amount = amount
        self.status = status

    def update_status(self, status: str) -> None:
        self.status = status

    def __repr__(self) -> str:
        return (f"Order(identifier={self.identifier!r}, client={self.client!r}, "
                f"date={self.date!r}, amount={self.amount!r}, "
                f"status={self.status!r})")


def demo() -> None:
    store = MemoryStore[Order]()

    store.add("1", Order("1", "Иванов", "2025-01-10", 1500.0, "new"))
    store.add("2", Order("2", "Петров", "2025-01-11", 800.0, "new"))
    store.add("3", Order("3", "Сидоров", "2025-01-12", 2300.0, "new"))

    for order in store.list_all():
        print(order)

    target = store.get("2")
    if target is not None:
        target.update_status("in_progress")
        print("Обновлён заказ:", store.get("2"))

    store.delete("1")
    print("Оставшиеся заказы:", len(store.list_all()))


if __name__ == "__main__":
    demo()
