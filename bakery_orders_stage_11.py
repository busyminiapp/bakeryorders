# === Stage 11: Группировка ===
# Project: BakeryOrders
from collections import Counter


def group_orders_by_date(orders):
    """Группирует заказы по полю 'дата' и подсчитывает количество в каждой группе.

    Возвращает список кортежей (дата, количество), отсортированный по дате.
    """
    counts = Counter(order["дата"] for order in orders)
    return sorted(counts.items(), key=lambda item: item[0])


def build_date_summary(orders):
    """Построение сводки: дата -> общее число заказов и суммарная сумма."""
    grouped = Counter(order["дата"] for order in orders)
    summary = {}
    for date, quantity in grouped.items():
        total = sum(order["сумма"] for order in orders if order["дата"] == date)
        summary[date] = {"количество": quantity, "сумма": total}
    return summary


def print_date_summary(orders):
    """Выводит сводку заказов по датам в читаемом виде."""
    summary = build_date_summary(orders)
    for date in sorted(summary):
        info = summary[date]
        print(f"Дата: {date}")
        print(f"  Заказов: {info['количество']}")
        print(f"  Сумма: {info['сумма']}")
        print()


if __name__ == "__main__":
    sample_orders = [
        {"клиент": "Иван", "дата": "2024-01-01", "сумма": 120, "статус": "готов"},
        {"клиент": "Мария", "дата": "2024-01-01", "сумма": 90, "статус": "готов"},
        {"клиент": "Ольга", "дата": "2024-01-02", "сумма": 200, "статус": "в работе"},
        {"клиент": "Пётр", "дата": "2024-01-02", "дата": "2024-01-02", "сумма": 150, "статус": "готов"},
    ]
    print_date_summary(sample_orders)
