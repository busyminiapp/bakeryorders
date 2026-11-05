# === Stage 2: Проверка полей ===
# Project: BakeryOrders
from datetime import date


VALID_STATUSES = {"новый", "в работе", "готов", "отменён"}


class OrderValidationError(ValueError):
    pass


def normalize_client(client):
    if client is None:
        return ""
    return str(client).strip()


def normalize_date(raw):
    if raw is None:
        return None
    text = str(raw).strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            parsed = date.fromisoformat(text.replace(".", "/").replace("-", "/"))
            return parsed.isoformat()
        except ValueError:
            continue
    raise OrderValidationError(f"Неверный формат даты: '{raw}'")


def normalize_amount(raw):
    if raw is None:
        return 0
    try:
        value = float(str(raw).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise OrderValidationError(f"Неверная сумма: '{raw}'")
    if value < 0:
        raise OrderValidationError("Сумма не может быть отрицательной")
    return round(value, 2)


def normalize_status(status):
    if status is None:
        return "новый"
    normalized = str(status).strip().lower()
    if normalized not in VALID_STATUSES:
        raise OrderValidationError(
            f"Неверный статус: '{status}'. Допустимые: "
            + ", ".join(sorted(VALID_STATUSES))
        )
    return normalized


def validate_order(order):
    errors = []
    client = normalize_client(order.get("клиент"))
    if not client:
        errors.append("Клиент не указан")

    order_date = normalize_date(order.get("дата"))
    if order_date is None:
        errors.append("Дата не указана")

    amount = normalize_amount(order.get("сумма"))
    if amount == 0:
        errors.append("Сумма не указана")

    status = normalize_status(order.get("статус"))

    if errors:
        message = "Ошибка заказа: " + "; ".join(errors)
        raise OrderValidationError(message)

    return {
        "клиент": client,
        "дата": order_date,
        "сумма": amount,
        "статус": status,
    }
