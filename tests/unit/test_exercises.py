from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.errors import ConflictError
from app.main import create_app
from app.services.product_service import (
    ProductService,
    calculate_final_price,
    validate_product,
)


# ===============================================================
# แบบฝึกหัดท้ายเล่ม ข้อ 1: ค่าขอบด้วย pytest
# ===============================================================

def test_exercise_1_name_exact_100_chars_valid():
    """1. ชื่อสินค้ายาว 100 ตัวอักษรพอดีต้องผ่าน"""
    data = {"name": "A" * 100, "price": 100, "stock": 10}
    assert validate_product(data) == []


def test_exercise_1_discount_12_5_percent():
    """2. ส่วนลด 12.5% ของ 200 ต้องได้ 175"""
    assert calculate_final_price(200, 12.5) == 175


def test_exercise_1_create_product_without_discount_defaults_to_zero():
    """3. สร้างสินค้าโดยไม่ส่ง discountPercent ต้องบันทึกเป็น 0"""
    repo = Mock()
    repo.create.side_effect = lambda data: {"id": 1, **data}
    service = ProductService(repo)
    result = service.create_product({"name": "Mechanical Keyboard", "price": 1500, "stock": 5})

    repo.create.assert_called_once_with({
        "name": "Mechanical Keyboard",
        "price": 1500,
        "stock": 5,
        "discountPercent": 0,
    })
    assert result["discountPercent"] == 0


# ===============================================================
# แบบฝึกหัดท้ายเล่ม ข้อ 4: TDD PATCH /api/products/{id}/stock
# ===============================================================

def test_exercise_4_adjust_stock_success():
    """ปรับสต็อกปกติ: 12 + (-2) = 10"""
    client = TestClient(create_app())
    # login
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.patch("/api/products/1/stock", json={"quantity": -2}, headers=headers)
    assert res.status_code == 200
    assert res.json()["stock"] == 10


def test_exercise_4_adjust_stock_conflict_409():
    """ปรับสต็อกจนติดลบ: สต็อกเดิม 12 แต่ลด 20 -> ต้องตอบ 409 Conflict"""
    client = TestClient(create_app())
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.patch("/api/products/1/stock", json={"quantity": -20}, headers=headers)
    assert res.status_code == 409
    assert "Stock cannot be negative" in res.json()["error"]
