"""Manage food delivery orders and back up the queue using JSON."""

import json
from datetime import datetime
from math import isfinite

ORDERS = {}
MENU = {}
DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}
VALID_STATUSES = ("placed", "cooking", "out_for_delivery", "delivered")

def create_order(customer, items, order_history=None):
    """Create a valid order; optionally append its ID to a caller's history."""
    if not isinstance(customer, str) or not customer.strip():
        raise ValueError("Customer name must not be blank")
    if not isinstance(items, (list, tuple)) or not items:
        raise ValueError("An order must contain a list of dishes")
    if any(not isinstance(item, str) or item not in MENU for item in items):
        raise ValueError("Order contains an unknown dish")
    if order_history is None:
        order_history = []
    order_id = max(ORDERS, default=0) + 1
    ORDERS[order_id] = {
        "customer": customer.strip(),
        "items": list(items),
        "total": sum(MENU[item] for item in items),
        "status": "placed",
    }
    order_history.append(order_id)
    return order_id

def update_order_status(order_id, status):
    """Set a known status on an existing order, reporting invalid requests."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    if order_id not in ORDERS:
        raise KeyError(f"Unknown order: {order_id}")
    ORDERS[order_id]["status"] = status

def valid_price(value):
    """Return whether a value is a finite, nonnegative JSON number."""
    return (
        type(value) in (int, float)
        and value >= 0
        and (isinstance(value, int) or isfinite(value))
    )

def read_menu_config(file="menu.json"):
    """Load a menu, using defaults only when the file does not exist."""
    try:
        with open(file, encoding="utf-8") as stream:
            loaded = json.load(stream)
    except FileNotFoundError:
        loaded = DEFAULT_MENU.copy()
    if not isinstance(loaded, dict) or not loaded:
        raise ValueError("Menu must be a nonempty object")
    if any(
        not isinstance(dish, str) or not dish.strip() or not valid_price(price)
        for dish, price in loaded.items()
    ):
        raise ValueError("Menu requires named dishes and nonnegative prices")
    MENU.clear()
    MENU.update(loaded)

def daily_revenue():
    """Return the total charged for delivered orders only."""
    return sum(
        order["total"] for order in ORDERS.values()
        if order["status"] == "delivered"
    )

def backup_orders(file="orders.json"):
    """Save the current queue as data, without executable pickle payloads."""
    with open(file, "w", encoding="utf-8") as stream:
        json.dump(ORDERS, stream, indent=2, allow_nan=False)

def validate_saved_order(order):
    """Reject malformed order records before replacing the current queue."""
    if not isinstance(order, dict):
        raise ValueError("Saved order must be an object")
    customer = order.get("customer")
    items = order.get("items")
    if not isinstance(customer, str) or not customer.strip():
        raise ValueError("Saved customer must not be blank")
    if not isinstance(items, list) or not items:
        raise ValueError("Saved items must be a nonempty list")
    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValueError("Saved dishes must be nonempty names")
    if not valid_price(order.get("total")):
        raise ValueError("Saved total must be a nonnegative number")
    if order.get("status") not in VALID_STATUSES:
        raise ValueError("Saved status is invalid")

def restore_orders(file="orders.json"):
    """Load validated JSON with integer IDs; preserve state on failure."""
    with open(file, encoding="utf-8") as stream:
        loaded = json.load(stream)
    if not isinstance(loaded, dict):
        raise ValueError("Backup must be an object")
    restored = {}
    for key, order in loaded.items():
        order_id = int(key)
        if order_id <= 0 or str(order_id) != key:
            raise ValueError("Saved IDs must be canonical positive integers")
        validate_saved_order(order)
        restored[order_id] = order
    ORDERS.clear()
    ORDERS.update(restored)

def print_queue():
    """Print each order's customer, status and total."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in ORDERS.items():
        print(order_id, order["customer"], order["status"], order["total"])

def main():
    """Demonstrate order creation, status changes and a backup round trip."""
    read_menu_config()
    asha_order = create_order("Asha", ["pizza", "coke"])
    ravi_order = create_order("Ravi", ["burger", "fries"])
    update_order_status(asha_order, "delivered")
    update_order_status(ravi_order, "cooking")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()

if __name__ == "__main__":
    main()
