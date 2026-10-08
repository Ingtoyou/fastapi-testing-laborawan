from fastapi.testclient import TestClient

from app.main import create_app


# ===============================================================
# แบบฝึกหัดท้ายเล่ม ข้อ 2: Negative tests
# ===============================================================

def test_exercise_2_negative_update_not_found():
    """แก้ไขสินค้า id 999999 ต้องได้ 404"""
    client = TestClient(create_app())
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.put("/api/products/999999", json={"price": 100}, headers=headers)
    assert res.status_code == 404
    assert res.json()["error"] == "Product 999999 not found"


def test_exercise_2_negative_delete_without_token():
    """ลบสินค้าโดยไม่มี token ต้องได้ 401"""
    client = TestClient(create_app())
    res = client.delete("/api/products/1")
    assert res.status_code == 401
    assert res.json()["error"] == "Unauthorized"


def test_exercise_2_negative_login_empty_body():
    """login ด้วย body {} ต้องได้ 401"""
    client = TestClient(create_app())
    res = client.post("/api/auth/login", json={})
    assert res.status_code == 401
    assert res.json()["error"] == "Invalid username or password"


# ===============================================================
# แบบฝึกหัดท้ายเล่ม ข้อ 3: Integration flow S4x and S6b
# ===============================================================

def test_exercise_3_integration_s4x_and_s6b():
    client = TestClient(create_app())
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # S2: Create
    created = client.post(
        "/api/products",
        json={"name": "Gaming Chair", "price": 4500, "stock": 10, "discountPercent": 0},
        headers=headers,
    )
    assert created.status_code == 201
    prod_id = created.json()["id"]

    # S4x: Update stock to -5 -> Expect 400
    res_s4x = client.put(f"/api/products/{prod_id}", json={"stock": -5}, headers=headers)
    assert res_s4x.status_code == 400
    assert "stock must be an integer >= 0" in res_s4x.json()["details"]

    # S5: Verify stock is still 10
    res_s5 = client.get(f"/api/products/{prod_id}")
    assert res_s5.status_code == 200
    assert res_s5.json()["stock"] == 10

    # S6: Delete
    res_s6 = client.delete(f"/api/products/{prod_id}", headers=headers)
    assert res_s6.status_code == 204

    # S6b: Delete again -> Expect 404
    res_s6b = client.delete(f"/api/products/{prod_id}", headers=headers)
    assert res_s6b.status_code == 404
