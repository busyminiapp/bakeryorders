# === Stage 9: Поиск по нескольким словам ===
# Project: BakeryOrders
def parse_search_query(text):
    """
    Разбирает строку поиска: извлекает искомые слова и слова-исключения.
    Слова-исключения начинаются с дефиса.
    Возвращает кортеж (words, exclusions).
    """
    words = []
    exclusions = []
    for token in text.split():
        if token.startswith('-'):
            exclusions.append(token[1:].strip())
        else:
            words.append(token)
    return words, exclusions


def matches_query(order, words, exclusions):
    """
    Проверяет, соответствует ли заказ строке поиска.
    Все искомые слова должны присутствовать в каком-либо поле заказа,
    и ни одно слово-исключение не должно совпадать.
    """
    if not words:
        return True

    haystack = ' '.join(str(order.get(field, '')) for field in order.keys())

    for word in words:
        if word.lower() not in haystack.lower():
            return False

    for exclusion in exclusions:
        if exclusion.lower() in haystack.lower():
            return False

    return True


def search_orders(orders, query):
    """
    Поиск заказов по нескольким словам с поддержкой исключений.
    """
    words, exclusions = parse_search_query(query)
    results = [order for order in orders if matches_query(order, words, exclusions)]
    return results


def demo():
    orders = [
        {'client': 'Иванов', 'date': '2024-05-01', 'total': 1200, 'status': 'new'},
        {'client': 'Пекарня Свет', 'date': '2024-05-02', 'total': 3400, 'status': 'ready'},
        {'client': 'Офис Плюс', 'date': '2024-05-03', 'total': 800, 'status': 'ready'},
        {'client': 'Семья Петровых', 'date': '2024-05-04', 'total': 500, 'status': 'new'},
    ]
    print(search_orders(orders, 'Иванов'))
    print(search_orders(orders, 'готов'))
    print(search_orders(orders, 'Свет -Офис'))
    print(search_orders(orders, 'Офис'))


if __name__ == '__main__':
    demo()
