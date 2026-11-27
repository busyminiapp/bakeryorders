# === Stage 13: Быстрые фильтры ===
# Project: BakeryOrders
date_filter.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Iterable, List

__all__ = ("today_orders", "this_week_orders", "overdue_orders")


@dataclass(frozen=True)
class Order:
    client: str
    order_date: date
    amount: float
    status: str

    @property
    def is_overdue(self) -> bool:
        return self.status == "pending" and self.order_date < date.today()


def today_orders(orders: Iterable[Order]) -> List[Order]:
    return [order for order in orders if order.order_date == date.today()]


def this_week_orders(orders: Iterable[Order], monday: date | None = None) -> List[Order]:
    if monday is None:
        today = date.today()
        monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return [order for order in orders if monday <= order.order_date <= sunday]


def overdue_orders(orders: Iterable[Order]) -> List[Order]:
    return [order for order in orders if order.is_overdue]
