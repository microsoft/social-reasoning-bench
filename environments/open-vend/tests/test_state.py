"""Tests for state management."""

import json
import tempfile
from pathlib import Path

from src.simulation.state import (
    Email,
    GameState,
    MachineSlot,
    Order,
    OrderStatus,
    SlotSize,
    WarehouseItem,
)


class TestWarehouseItem:
    def test_create_item(self):
        item = WarehouseItem(
            product_id="test_123",
            name="Test Product",
            quantity=50,
            unit_cost=1.25,
            size=SlotSize.SMALL,
        )
        assert item.product_id == "test_123"
        assert item.quantity == 50
        assert item.unit_cost == 1.25

    def test_to_dict_and_back(self):
        item = WarehouseItem(
            product_id="test_123",
            name="Test Product",
            quantity=50,
            unit_cost=1.25,
            size=SlotSize.SMALL,
        )
        data = item.to_dict()
        restored = WarehouseItem.from_dict(data)
        assert restored.product_id == item.product_id
        assert restored.size == item.size


class TestMachineSlot:
    def test_empty_slot(self):
        slot = MachineSlot(slot_id=0, size=SlotSize.SMALL)
        assert slot.empty
        assert slot.quantity == 0
        assert slot.product_id is None

    def test_filled_slot(self):
        slot = MachineSlot(
            slot_id=0,
            size=SlotSize.SMALL,
            product_id="chips_lays",
            product_name="Lay's Chips",
            quantity=8,
            price=1.75,
        )
        assert not slot.empty
        assert slot.quantity == 8

    def test_capacity_small_vs_large(self):
        small = MachineSlot(slot_id=0, size=SlotSize.SMALL, capacity=10)
        large = MachineSlot(slot_id=6, size=SlotSize.LARGE, capacity=8)
        assert small.capacity == 10
        assert large.capacity == 8


class TestEmail:
    def test_create_email(self):
        email = Email(
            id="test_001",
            from_address="supplier@test.com",
            to_address="charles.paxton@vendingsandstuff.com",
            subject="Product Catalog",
            content="Here are our products...",
            timestamp="Day 1",
        )
        assert email.read is False
        assert email.id == "test_001"

    def test_email_serialization(self):
        email = Email(
            id="test_001",
            from_address="supplier@test.com",
            to_address="charles.paxton@vendingsandstuff.com",
            subject="Test",
            content="Content",
            timestamp="Day 1",
            read=True,
        )
        data = email.to_dict()
        restored = Email.from_dict(data)
        assert restored.read == email.read
        assert restored.id == email.id


class TestOrder:
    def test_order_status_pending(self):
        order = Order(
            order_id="order_001",
            supplier_email="supplier@test.com",
            items=[{"product_id": "chips", "quantity": 24, "unit_cost": 0.75}],
            total_cost=18.0,
            status=OrderStatus.PENDING,
            order_day=1,
            delivery_day=3,
        )
        assert order.status == OrderStatus.PENDING

    def test_order_serialization(self):
        order = Order(
            order_id="order_001",
            supplier_email="supplier@test.com",
            items=[{"product_id": "chips", "quantity": 24, "unit_cost": 0.75}],
            total_cost=18.0,
            status=OrderStatus.PAID,
            order_day=1,
            delivery_day=3,
        )
        data = order.to_dict()
        restored = Order.from_dict(data)
        assert restored.status == OrderStatus.PAID


class TestGameState:
    def test_initial_state(self):
        state = GameState()
        assert state.current_day == 1
        assert state.bank_balance == 500.0
        assert state.machine_cash == 0.0
        assert len(state.machine_slots) == 12

    def test_machine_slot_layout(self):
        state = GameState()
        # First 6 slots should be small
        for i in range(6):
            assert state.machine_slots[i].size == SlotSize.SMALL
        # Last 6 slots should be large
        for i in range(6, 12):
            assert state.machine_slots[i].size == SlotSize.LARGE

    def test_warehouse_total_items(self):
        state = GameState()
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=50,
            unit_cost=0.75,
            size=SlotSize.SMALL,
        )
        state.warehouse["soda"] = WarehouseItem(
            product_id="soda",
            name="Soda",
            quantity=30,
            unit_cost=0.45,
            size=SlotSize.LARGE,
        )
        assert state.get_warehouse_total_items() == 80

    def test_calculate_net_worth(self):
        state = GameState()
        state.bank_balance = 400.0
        state.machine_cash = 50.0
        state.warehouse["chips"] = WarehouseItem(
            product_id="chips",
            name="Chips",
            quantity=100,
            unit_cost=0.50,  # $50 inventory value
            size=SlotSize.SMALL,
        )
        # Net worth = 400 + 50 + 50 = 500
        assert state.calculate_net_worth() == 500.0

    def test_state_save_and_load(self):
        state = GameState()
        state.current_day = 10
        state.bank_balance = 750.25
        state.memory["key1"] = "value1"
        state.warehouse["product"] = WarehouseItem(
            product_id="product",
            name="Test Product",
            quantity=25,
            unit_cost=1.00,
            size=SlotSize.SMALL,
        )

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = Path(f.name)

        try:
            state.save(path)
            loaded = GameState.load(path)

            assert loaded.current_day == 10
            assert loaded.bank_balance == 750.25
            assert loaded.memory["key1"] == "value1"
            assert "product" in loaded.warehouse
            assert loaded.warehouse["product"].quantity == 25
        finally:
            path.unlink()

    def test_state_json_roundtrip(self):
        state = GameState()
        state.emails.append(
            Email(
                id="email_001",
                from_address="test@test.com",
                to_address="agent@test.com",
                subject="Test",
                content="Content",
                timestamp="Day 1",
            )
        )
        state.orders.append(
            Order(
                order_id="order_001",
                supplier_email="supplier@test.com",
                items=[],
                total_cost=100.0,
                status=OrderStatus.PENDING,
                order_day=1,
                delivery_day=3,
            )
        )

        data = state.to_dict()
        json_str = json.dumps(data)
        restored_data = json.loads(json_str)
        restored = GameState.from_dict(restored_data)

        assert len(restored.emails) == 1
        assert len(restored.orders) == 1
        assert restored.orders[0].status == OrderStatus.PENDING
