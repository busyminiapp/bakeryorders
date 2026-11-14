# === Stage 7: Фильтрация записей ===
# Project: BakeryOrders
def filter_orders_by_date(orders, date_value=None, date_range=None):
    """Фильтрует заказы по значению поля 'дата' или по диапазону дат.

    date_value - точное совпадение с датой (строка в формате 'YYYY-MM-DD' или datetime.date).
    date_range - кортеж (start_date, end_date) для диапазона, включительно.
    Совместимы с датами в формате строки 'YYYY-MM-DD' и объектами datetime.date.
    """
    def parse(value):
        if isinstance(value, datetime.date):
            return value
        if isinstance(value, str):
            return datetime.date.fromisoformat(value.strip())
        return value

    def order_date(order):
        if 'date' not in order:
            return None
        return parse(order['date'])

    result = []
    for order in orders:
        order_date_value = order_date(order)
        if order_date_value is None:
            continue
        if date_value is not None:
            if order_date_value != parse(date_value):
                continue
        if date_range is not None:
            start = parse(date_range[0])
            end = parse(date_range[1])
            if not (start <= order_date_value <= end):
                continue
        result.append(order)
    return result


def filter_orders_by_date_range(orders, start_date, end_date):
    """Удобная обёртка для фильтрации по диапазону дат (включительно)."""
    return filter_orders_by_date(orders, date_range=(start_date, end_date))


def filter_orders_by_date_value(orders, date_value):
    """Удобная обёртка для фильтрации по точному значению даты."""
    return filter_orders_by_date(orders, date_value=date_value)
