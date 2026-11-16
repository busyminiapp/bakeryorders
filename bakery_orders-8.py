# === Stage 8: Текстовый поиск ===
# Project: BakeryOrders
def search_orders(orders, query, highlight_char='*'):
    normalized_query = query.strip().lower()
    results = []
    for order in orders:
        if _order_matches(order, normalized_query):
            results.append(_order_with_highlight(order, normalized_query, highlight_char))
    return results


def _order_matches(order, normalized_query):
    if not normalized_query:
        return True
    client = order.get('client', '')
    date = order.get('date', '')
    if normalized_query in client.lower():
        return True
    if normalized_query in date.lower():
        return True
    return False


def _order_with_highlight(order, normalized_query, highlight_char):
    client = order.get('client', '')
    date = order.get('date', '')
    client_display = _highlight(client, normalized_query, highlight_char)
    date_display = _highlight(date, normalized_query, highlight_char)
    return {
        'client': client_display,
        'date': date_display,
        'amount': order.get('amount'),
        'status': order.get('status'),
    }


def _highlight(text, normalized_query, highlight_char):
    if not normalized_query or not text:
        return text
    result = []
    text_lower = text.lower()
    idx = 0
    while True:
        pos = text_lower.find(normalized_query, idx)
        if pos == -1:
            result.append(text[idx:])
            break
        result.append(text[idx:pos])
        result.append(highlight_char * len(normalized_query))
        idx = pos + len(normalized_query)
    return ''.join(result)


if __name__ == '__main__':
    sample_orders = [
        {'client': 'ИП Иванов', 'date': '2025-01-10', 'amount': 1200, 'status': 'готов'},
        {'client': 'Пекарня Ромашка', 'date': '2025-01-11', 'amount': 3400, 'status': 'в работе'},
        {'client': 'Шоколадный мир', 'date': '2025-01-12', 'amount': 850, 'status': 'готов'},
    ]
    for found in search_orders(sample_orders, 'ромашка'):
        print(f"Клиент: {found['client']} | Дата: {found['date']} | Сумма: {found['amount']} | Статус: {found['status']}")
    print()
    for found in search_orders(sample_orders, 'готов'):
        print(f"Клиент: {found['client']} | Дата: {found['date']} | Сумма: {found['amount']} | Статус: {found['status']}")
