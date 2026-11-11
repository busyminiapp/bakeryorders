# === Stage 5: Удаление и восстановление ===
# Project: BakeryOrders
import uuid


class SoftDeletedOrder:
    """Заказ с возможностью мягкого удаления и восстановления."""

    def __init__(self, order_id=None, client=None, date=None, amount=None, status=None):
        self.order_id = order_id or str(uuid.uuid4())
        self.client = client
        self.date = date
        self.amount = amount
        self.status = status
        self.deleted = False
        self.deleted_at = None

    def delete(self):
        """Мягкое удаление с фиксацией времени."""
        self.deleted = True
        self.deleted_at = _current_timestamp()
        return self

    def restore(self):
        """Восстановление удалённого заказа."""
        self.deleted = False
        self.deleted_at = None
        return self

    def is_deleted(self):
        return self.deleted

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "client": self.client,
            "date": self.date,
            "amount": self.amount,
            "status": self.status,
            "deleted": self.deleted,
            "deleted_at": self.deleted_at,
        }


def _current_timestamp():
    """Текущее время в формате ISO-8601."""
    from datetime import datetime

    return datetime.now().isoformat(timespec="seconds")


class OrderRepository:
    """Репозиторий заказов с поддержкой мягкого удаления."""

    def __init__(self):
        self._orders = {}

    def create(self, client=None, date=None, amount=None, status=None):
        order = SoftDeletedOrder(client=client, date=date, amount=amount, status=status)
        self._orders[order.order_id] = order
        return order

    def get(self, order_id):
        return self._orders.get(order_id)

    def get_active(self, order_id):
        order = self._orders.get(order_id)
        return order if order and not order.is_deleted() else None

    def list_active(self):
        return [o for o in self._orders.values() if not o.is_deleted()]

    def list_deleted(self):
        return [o for o in self._orders.values() if o.is_deleted()]

    def delete(self, order_id):
        order = self.get(order_id)
        if order:
            order.delete()
        return order

    def restore(self, order_id):
        order = self._orders.get(order_id)
        if order and order.is_deleted():
            order.restore()
        return order

    def exists(self, order_id):
        return order_id in self._orders
