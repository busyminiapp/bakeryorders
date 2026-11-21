# === Stage 10: Теги ===
# Project: BakeryOrders
from typing import List, Optional, Dict


class Tag:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Tag({self.name!r})"


class Order:
    def __init__(self, client: str, date: str, amount: float, status: str):
        self.client = client
        self.date = date
        self.amount = amount
        self.status = status
        self.tags: List[Tag] = []

    def add_tag(self, name: str) -> Tag:
        tag = Tag(name)
        if tag not in self.tags:
            self.tags.append(tag)
        return tag

    def remove_tag(self, name: str) -> bool:
        for tag in self.tags:
            if tag.name == name:
                self.tags.remove(tag)
                return True
        return False

    def has_tag(self, name: str) -> bool:
        return any(tag.name == name for tag in self.tags)

    def tag_names(self) -> List[str]:
        return [tag.name for tag in self.tags]


def find_by_tag(orders: List[Order], name: str) -> List[Order]:
    return [order for order in orders if order.has_tag(name)]


if __name__ == "__main__":
    orders = [
        Order("Иванов", "2025-01-10", 1500.0, "new"),
        Order("Петров", "2025-01-11", 800.0, "processing"),
    ]

    orders[0].add_tag("vip")
    orders[1].add_tag("vip")
    orders[1].add_tag("urgent")

    print(orders[0].tags)
    print(orders[1].tags)

    print(orders[0].remove_tag("vip"))
    print(orders[0].tags)

    print(find_by_tag(orders, "vip"))
