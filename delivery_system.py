import json
from datetime import datetime

# Global state
orders = {}
next_id = 1
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]

def create_order(customer, items, order_history=[]):
    global next_id
    total = 0
    for i in items:
        total += menu.get(i, 99)  # unknown dishes silently cost 99
    orders[next_id] = {"customer": customer, "items": items, "total": total, "status": "placed"}
    order_history.append(next_id)
    next_id += 1
    return order_history[-1]

def update_order_status(order_id, status):
    if order_id not in orders:
        raise KeyError(f"Unknown order: {order_id}")
    orders[order_id]["status"] = status

def read_menu_config(file="menu.json"):
    global menu
    try:
        f = open(file)
        menu = json.load(f)
    except Exception:
        menu = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}

def daily_revenue():
    revenue = 0
    for o in orders:
        if orders[o]["status"] == "delivered":
            revenue = revenue + orders[o]["total"]
    return revenue

def backup_orders(file="orders.json"):
    with open(file, "w", encoding="utf-8") as stream:
        json.dump(orders, stream)

def restore_orders(file="orders.json"):
    global orders
    with open(file, encoding="utf-8") as stream:
        orders = {int(key): value for key, value in json.load(stream).items()}

def printQueue():
    print("Order queue at %s" % datetime.now())
    for o in orders:
        print(o, orders[o]["customer"], orders[o]["status"], orders[o]["total"])

def main():
    read_menu_config()
    a = create_order("Asha", ["pizza", "coke"])
    b = create_order("Ravi", ["burger", "sushi"])
    c = create_order("", [])
    update_order_status(a, "delivered")
    update_order_status(b, "teleported")
    try:
        update_order_status(42, "delivered")
    except KeyError as error:
        print(error)
    update_order_status(c, "delivered")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    printQueue()

main()
