# === Stage 1: Каркас модуля ===
# Project: BakeryOrders
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Order:
    client: str
    order_date: date
    amount: float
    status: str = "new"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Сумма заказа не может быть отрицательной")

    def mark_delivered(self):
        self.status = "delivered"


def make_demo_orders():
    return [
        Order("Иванов Иван", date(2024, 5, 10), 1250.0, "new"),
        Order("ООО Ромашка", date(2024, 5, 11), 4800.0, "in_progress"),
        Order("Петрова Анна", date(2024, 5, 9), 640.0, "delivered"),
    ]


def main():
    orders = make_demo_orders()
    print("Заказы пекарни BakeryOrders")
    print("=" * 30)
    for i, order in enumerate(orders, start=1):
        print(f"#{i} | {order.client} | {order.order_date} | "
              f"{order.amount:.2f} ₽ | {order.status}")
    print("=" * 30)
    print(f"Всего заказов: {len(orders)}")
