# === Stage 6: Связи между сущностями ===
# Project: BakeryOrders
from datetime import datetime
from typing import List, Optional, Tuple


class Order:
    """Заказ небольшой пекарни."""

    def __init__(self, client: str, date: datetime, amount: float, status: str):
        self.client = client
        self.date = date
        self.amount = amount
        self.status = status


class Position:
    """Позиция заказа: одна единица товара в составе партии."""

    def __init__(self, order_id: int, product: str, qty: int, batch: str):
        self.order_id = order_id
        self.product = product
        self.qty = qty
        self.batch = batch


def fetch_positions(order: Order) -> List[Position]:
    """Получить все позиции для переданного заказа и проверить целостность связи.

    Возвращает список позиций, отсортированный по id продукта, либо пустой список
    вместе с флагом ошибки, если заказ не найден или связь повреждена.
    """
    if order is None:
        return [], True

    try:
        positions = _query_positions(order)
    except KeyError:
        return [], True

    _check_integrity(order, positions)
    return sorted(positions, key=lambda p: p.order_id), False


def _query_positions(order: Order) -> List[Position]:
    """Симуляция загрузки позиций из хранилища по идентификатору заказа."""
    registry: dict[int, List[Position]] = {
        1001: [
            Position(1001, "Хлеб белый", 50, "B-001"),
            Position(1001, "Булки", 30, "B-002"),
        ],
        1002: [
            Position(1002, "Круассаны", 40, "C-005"),
        ],
        1003: [
            Position(1003, "Сдоба", 25, "S-010"),
            Position(1003, "Пирожки", 60, "P-007"),
        ],
    }
    return registry.get(order.order_id, [])


def _check_integrity(order: Order, positions: List[Position]) -> None:
    """Проверить целостность связи между заказом и его позициями.

    Проверки:
      * заказ не должен быть пустым;
      * каждая позиция должна ссылаться на тот же заказ;
      * суммы количеств в позициях должны воспроизводить общую сумму заказа.
    """
    if not positions:
        raise KeyError("Заказ не содержит позиций")

    for position in positions:
        if position.order_id != order.order_id:
            raise KeyError("Несоответствие идентификатора позиции заказу")

    total_qty = sum(position.qty for position in positions)
    if total_qty != order.amount:
        raise KeyError(
            f"Сумма количеств ({total_qty}) не совпадает со суммой заказа ({order.amount})"
        )
