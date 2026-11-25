# === Stage 12: Постраничный вывод ===
# Project: BakeryOrders
"""Paginated access to the bakery order list.

Works with a list of order dicts. Each order has at least the keys:
id, client, date, total, status. Pagination splits the list into pages
of a chosen size and exposes them one at a time.
"""

from typing import Any, Dict, List, Tuple


def paginate(orders: List[Dict[str, Any]], page: int = 1, size: int = 10) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """Return the requested slice of orders together with page metadata.

    The slice contains the orders for the given 1-based page number.
    The metadata dict reports the page index, the requested size, the
    total number of pages and the total number of orders.
    """

    if size <= 0:
        raise ValueError("page size must be a positive integer")

    if page < 1:
        raise ValueError("page number must be at least one")

    total = len(orders)
    total_pages = (total + size - 1) // size
    page = min(page, total_pages)

    start = (page - 1) * size
    end = start + size
    slice_orders = orders[start:end]

    return slice_orders, {
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages,
    }


def page_numbers(total_pages: int, current: int, window: int = 5) -> List[int]:
    """Return the list of page numbers to display around the current page.

    The window controls how many page numbers appear on each side of the
    current page. When the current page is near an edge the list is
    centred on the nearest available boundary so the navigation stays
    useful near the first and last pages.
    """

    if total_pages <= window * 2 + 1:
        return list(range(1, total_pages + 1))

    lower = current - window
    upper = current + window
    lower = max(lower, 1)
    upper = min(upper, total_pages)

    if lower > 1:
        lower = max(1, lower - window)
    if upper < total_pages:
        upper = min(total_pages, upper + window)

    return list(range(lower, upper + 1))
