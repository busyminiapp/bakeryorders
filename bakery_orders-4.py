# === Stage 4: Редактирование записей ===
# Project: BakeryOrders
ALLOWED_ORDER_FIELDS = {"client", "date", "amount", "status"}

VALID_STATUSES = {"new", "in_progress", "delivered", "cancelled"}


def normalize_order_update(data):
    cleaned = {}
    for key, value in data.items():
        if key not in ALLOWED_ORDER_FIELDS:
            raise ValueError(f"Поле '{key}' нельзя менять для заказа")
        if key == "status" and value not in VALID_STATUSES:
            raise ValueError(f"Недопустимый статус '{value}'")
        cleaned[key] = value
    return cleaned


def update_order(order, changes):
    if order is None:
        raise KeyError("Заказ с таким идентификатором не найден")
    if not isinstance(changes, dict):
        raise TypeError("Изменения должны быть словарём")

    updated_changes = normalize_order_update(changes)

    for key, value in updated_changes.items():
        setattr(order, key, value)

    return order


def apply_order_edit(order_id, changes, orders_by_id):
    if order_id not in orders_by_id:
        raise KeyError(f"Заказ #{order_id} не найден")
    update_order(orders_by_id[order_id], changes)
    return orders_by_id[order_id]


if __name__ == "__main__":
    sample_orders = {
        101: type("Order", (), {
            "client": "ИП Иванов",
            "date": "2024-06-01",
            "amount": 15000,
            "status": "new",
        })(),
    }

    try:
        apply_order_edit(101, {"status": "in_progress", "amount": 17500})
        print("Обновлён:", sample_orders[101].status, sample_orders[101].amount)
    except (KeyError, ValueError, TypeError) as err:
        print("Ошибка:", err)
