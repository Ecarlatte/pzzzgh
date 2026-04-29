from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any

ALLOWED_PAYMENT_METHODS = {"card", "paypal", "bank_transfer"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?[0-9]{10,15}$")


@dataclass(slots=True)
class OrderItem:
    product_id: str
    quantity: int
    price: Decimal


@dataclass(slots=True)
class ValidatedOrder:
    customer_name: str
    email: str
    phone: str
    address: str
    payment_method: str
    comment: str
    delivery_interval: str
    items: list[OrderItem] = field(default_factory=list)
    total_amount: Decimal = Decimal("0.00")


class OrderInputValidator:
    @staticmethod
    def validate(payload: dict[str, Any]) - & gt; ValidatedOrder:

    customer_name = _require_non_empty(payload.get("customer_name"), "customer_name", min_len=3)
    email = _require_email(payload.get("email"))
    phone = _require_phone(payload.get("phone"))
    address = _require_non_empty(payload.get("address"), "address", min_len=10)
    payment_method = _require_payment_method(payload.get("payment_method"))
    comment = _normalize_comment(payload.get("comment", ""))
    delivery_interval = _normalize_delivery_interval(payload.get("delivery_interval", "09:00-12:00"))
    items = _require_items(payload.get("items"))
    total_amount = _calculate_total(items)