"""Regression checks for the lab fixes."""

import contextlib
import copy
import importlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import delivery_system as app


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        app.ORDERS.clear()
        app.MENU.clear()
        app.MENU.update(app.DEFAULT_MENU)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "data.json"

    def test_order_total_and_item_copy(self):
        items = ["pizza", "coke"]
        order = app.create_order(" Asha ", items)
        items.append("fries")
        self.assertEqual(app.ORDERS[order]["total"], 290)
        self.assertEqual(app.ORDERS[order]["items"], ["pizza", "coke"])
        self.assertEqual(app.ORDERS[order]["customer"], "Asha")

    def test_reject_invalid_orders_without_mutation(self):
        for customer, items in [("", ["pizza"]), ("A", []),
                                ("A", ["sushi"]), ("A", "pizza")]:
            with self.subTest(customer=customer, items=items):
                with self.assertRaises(ValueError):
                    app.create_order(customer, items)
                self.assertEqual(app.ORDERS, {})

    def test_optional_history(self):
        first, second = [], []
        app.create_order("A", ["pizza"], first)
        app.create_order("B", ["burger"], second)
        app.create_order("C", ["fries"])
        self.assertEqual(first, [1])
        self.assertEqual(second, [2])
        self.assertEqual(app.create_order.__defaults__, (None,))

    def test_invalid_status_preserves_order(self):
        order = app.create_order("A", ["pizza"])
        with self.assertRaises(ValueError):
            app.update_order_status(order, "teleported")
        self.assertEqual(app.ORDERS[order]["status"], "placed")

    def test_missing_order_is_reported(self):
        with self.assertRaises(KeyError):
            app.update_order_status(42, "delivered")

    def test_revenue_counts_only_delivered_orders(self):
        first = app.create_order("A", ["pizza", "coke"])
        app.create_order("B", ["burger"])
        app.update_order_status(first, "delivered")
        self.assertEqual(app.daily_revenue(), 290)

    def test_backup_roundtrip_and_next_id(self):
        app.create_order("A", ["pizza"])
        expected = copy.deepcopy(app.ORDERS)
        app.backup_orders(self.path)
        app.ORDERS.clear()
        app.restore_orders(self.path)
        self.assertEqual(app.ORDERS, expected)
        self.assertEqual(app.create_order("B", ["burger"]), 2)
        self.assertEqual(app.ORDERS[1], expected[1])

    def test_invalid_backup_preserves_state(self):
        app.create_order("A", ["pizza"])
        expected = copy.deepcopy(app.ORDERS)
        for payload in [[], {"1": {}}, {"01": expected[1]}]:
            self.path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                app.restore_orders(self.path)
            self.assertEqual(app.ORDERS, expected)

    def test_missing_menu_uses_defaults(self):
        app.MENU.clear()
        app.read_menu_config(self.path)
        self.assertEqual(app.MENU, app.DEFAULT_MENU)

    def test_custom_menu(self):
        self.path.write_text('{"rice": 100}', encoding="utf-8")
        app.read_menu_config(self.path)
        self.assertEqual(app.MENU, {"rice": 100})

    def test_invalid_menu_is_reported_without_state_loss(self):
        for text in ['{', '[]', '{"rice": -1}', '{"rice": true}',
                     '{"rice": NaN}']:
            self.path.write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                app.read_menu_config(self.path)
            self.assertEqual(app.MENU, app.DEFAULT_MENU)

    def test_import_has_no_demo_output(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            importlib.reload(app)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(app.ORDERS, {})


if __name__ == "__main__":
    unittest.main()
