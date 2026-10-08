# FastAPI Testing Lab 🧪
## คู่มือปฏิบัติการ Unit Testing และ Integration Testing สำหรับ FastAPI

![API Tests](https://github.com/Ingtoyou/fastapi-testing-laborawan/actions/workflows/api-tests.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688)
![pytest](https://img.shields.io/badge/pytest-9.1.1-success)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Newman](https://img.shields.io/badge/newman-6.2.2-orange)

คลังโค้ดนี้จัดทำขึ้นเพื่อการเรียนรู้และฝึกปฏิบัติการทดสอบซอฟต์แวร์ตามหลักการวิศวกรรมซอฟต์แวร์ (Software Engineering) ครอบคลุมการทดสอบแบบ **Unit Testing, Integration Testing, Data-Driven Testing, Automated API Testing (Newman)** และการสร้างระบบ **Continuous Integration (GitHub Actions)**

---

## 🏛️ สถาปัตยกรรมระบบ (System Architecture)

ระบบออกแบบตามแนวคิด **Layered Architecture & Separation of Concerns**:

```
[ Client / TestClient / Postman ]
               │ (HTTP Request / JSON)
               ▼
   [ Router Layer: app/routers/ ]
   - รับ HTTP Request / ตรวจสอบ Authorization Token (Dependency)
   - แปลงและ Validate Path / Query Parameters (parse_id)
               │ (Service Call)
               ▼
   [ Service Layer: app/services/ ]
   - กฎทางธุรกิจ (Business Rules) & การคำนวณราคา (calculate_final_price)
   - ตรวจสอบความถูกต้องของข้อมูล (validate_product)
   - ไม่ขึ้นกับ HTTP Framework (Pure Functions เหมาะกับการทำ Unit Test)
               │ (Data Access)
               ▼
   [ Repository Layer: app/repositories/ ]
   - จัดการเก็บข้อมูล (InMemoryProductRepository)
   - ส่งผ่านเข้ามาใน Service แบบ Dependency Injection (DI)
```

---

## 📊 สรุปผลการปฏิบัติการ (Lab 0 – Lab 8)

| Lab | หัวข้อ | ผลงานที่ตรวจได้ | สถานะ |
|:---:|:---|:---|:---:|
| **0** | เตรียมเครื่องมือและโปรเจกต์ | Commit `Lab 0: project setup` พร้อมตั้งค่า `.venv`, `pytest.ini`, `.gitignore` | ✅ ผ่าน |
| **1** | สร้าง Product API ด้วย FastAPI | API ครบ 3 ชั้น, Exception Handlers สำหรับ `400, 401, 404`, ทดสอบผ่าน `/docs` | ✅ ผ่าน |
| **2** | Unit Test ด้วย pytest | 20 passed, Coverage Service `94%` (สูงกว่าเกณฑ์ 90%) | ✅ ผ่าน |
| **3** | Unit API Test ด้วย Postman | Postman Collection `01-Unit-API-Tests` ผ่าน 19 assertions | ✅ ผ่าน |
| **4** | Integration Test ด้วย Postman | Postman Collection `02-Integration-Flow` (S1–S7) ผ่าน 12 assertions | ✅ ผ่าน |
| **5** | Data-Driven Testing | Postman Collection `03-Data-Driven` ร่วมกับ `products.csv` ผ่านครบทุก Iteration | ✅ ผ่าน |
| **6** | Integration Test ด้วย TestClient | ทดสอบ Integration แบบ In-Process (25 passed, Coverage รวม `94%`) | ✅ ผ่าน |
| **7** | รันอัตโนมัติด้วย Newman | สคริปต์ `scripts/run_postman.py` สั่งเปิด Server ยิง Newman และปิด Server อัตโนมัติ (Exit code 0) | ✅ ผ่าน |
| **8** | CI ด้วย GitHub Actions | ไฟล์ `.github/workflows/api-tests.yml` รันผ่านสมบูรณ์ พร้อม Artifact `postman-report` | ✅ ผ่าน |

---

## 📝 บันทึกผลและเฉลยแบบฝึกหัดท้ายเล่ม (Exercise Solutions & Logs)

### 1. แบบฝึกหัดข้อ 1: ค่าขอบด้วย pytest (Boundary Value Testing)
* **โจทย์:**
  1. ชื่อสินค้ายาว 100 ตัวอักษรพอดีต้องผ่าน
  2. ส่วนลด 12.5% ของ 200 ต้องได้ 175
  3. สร้างสินค้าโดยไม่ส่ง `discountPercent` ต้องบันทึกเป็น 0
* **ไฟล์ทดสอบ:** [`tests/unit/test_exercises.py`](tests/unit/test_exercises.py)
* **ผลการทดสอบ:** ✅ ผ่านทั้งหมด 3 เคส

### 2. แบบฝึกหัดข้อ 2: Negative Test ใน API
* **โจทย์:**
  1. แก้ไขสินค้า `id: 999999` ต้องตอบกลับ `404 Not Found`
  2. ลบสินค้าโดยไม่มี Token ต้องตอบกลับ `401 Unauthorized`
  3. Login ด้วย body `{}` ต้องตอบกลับ `401 Unauthorized`
* **ไฟล์ทดสอบ:** [`tests/integration/test_exercises_api.py`](tests/integration/test_exercises_api.py)
* **ผลการทดสอบ:** ✅ ผ่านทั้งหมด 3 เคส

### 3. แบบฝึกหัดข้อ 3: Integration Flow (S4x & S6b)
* **โจทย์:**
  1. เพิ่มขั้น `S4x` ส่ง `{"stock": -5}` ต้องได้ `400 Bad Request`
  2. ขั้น `S5` ตรวจสอบยังต้องเห็น stock เป็น 10 เท่าเดิม
  3. เพิ่มขั้น `S6b` ลบซ้ำหลังจากลบไปแล้ว ต้องได้ `404 Not Found`
* **ไฟล์ทดสอบ:** [`tests/integration/test_exercises_api.py`](tests/integration/test_exercises_api.py)
* **ผลการทดสอบ:** ✅ ผ่านการจำลองการทำงานต่อเนื่องสมบูรณ์

### 4. แบบฝึกหัดข้อ 4: TDD (Test-Driven Development)
* **โจทย์:** เพิ่ม Endpoint `PATCH /api/products/{product_id}/stock` รับ `{"quantity": int}` เพื่อปรับจำนวนสต็อก หากสต็อกติดลบต้องตอบ `409 Conflict`
* **การพัฒนา:**
  1. เพิ่ม Exception `ConflictError` (status code 409) ใน `app/errors.py`
  2. เพิ่มเมธอด `adjust_stock` ใน `app/services/product_service.py`
  3. เพิ่ม Route `PATCH /{product_id}/stock` ใน `app/routers/products.py`
  4. เขียนเทสต์ตรวจสอบใน `tests/unit/test_exercises.py`
* **ผลการทดสอบ:** ✅ ผ่านทั้งกรณีปรับปกติ (status 200) และกรณีติดลบ (status 409)

### 5. แบบฝึกหัดข้อ 5: Data-Driven CSV Extension
* **โจทย์:** เพิ่มแถวใน `postman/data/products.csv` ครอบคลุม:
  - `valid-zero-stock`: สินค้าราคา 500, stock=0 (บันทึกสำเร็จ status 201)
  - `invalid-zero-price`: สินค้าราคา 0 (ล้มเหลว status 400)
  - `invalid-decimal-stock`: สินค้า stock=2.5 เป็นทศนิยม (ล้มเหลว status 400)
* **ผลการทดสอบด้วย Newman:** ✅ รัน 10 Iterations ผ่านครบ 100%

---

## 📋 บันทึกผลการรันจริง (Execution Logs)

### 🧪 1. Pytest Full Execution Log (34 Passed / Coverage 95%)

```text
============================= test session starts =============================
platform win32 -- Python 3.10.0, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Api\fastapi-testing-lab
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.15.1, cov-7.1.0
collected 34 items

tests/integration/test_exercises_api.py ....                             [ 11%]
tests/integration/test_products_api.py .....                             [ 26%]
tests/unit/test_exercises.py .....                                       [ 41%]
tests/unit/test_product_service.py ....................                  [100%]

=============================== tests coverage ================================
Name                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------
app\__init__.py                              0      0   100%
app\auth.py                                  9      0   100%
app\errors.py                               21      0   100%
app\main.py                                 42      6    86%   51-54, 58-59
app\repositories\__init__.py                 0      0   100%
app\repositories\product_repository.py      29      1    97%   17
app\routers\__init__.py                      0      0   100%
app\routers\auth.py                         17      0   100%
app\routers\products.py                     31      2    94%   12, 21
app\services\__init__.py                     0      0   100%
app\services\product_service.py             73      2    97%   68, 107
----------------------------------------------------------------------
TOTAL                                      222     11    95%
============================= 34 passed in 0.97s ==============================
```

---

### 🚀 2. Newman Automation Test Log (Suite 1 & Suite 2)

```text
┌─────────────────────────┬─────────────────┬─────────────────┐
│                         │        executed │          failed │
├─────────────────────────┼─────────────────┼─────────────────┤
│              iterations │               1 │               0 │
│                requests │              16 │               0 │
│            test-scripts │              15 │               0 │
│      prerequest-scripts │              16 │               0 │
│              assertions │              31 │               0 │
├─────────────────────────┴─────────────────┴─────────────────┤
│ total run duration: 1394ms                                  │
│ average response time: 5ms                                  │
└─────────────────────────────────────────────────────────────┘

Data-Driven Suite (10 Iterations):
┌─────────────────────────┬─────────────────┬─────────────────┐
│                         │        executed │          failed │
├─────────────────────────┼─────────────────┼─────────────────┤
│              iterations │              10 │               0 │
│                requests │              15 │               0 │
│            test-scripts │              10 │               0 │
│      prerequest-scripts │              10 │               0 │
│              assertions │              20 │               0 │
├─────────────────────────┴─────────────────┴─────────────────┤
│ total run duration: 894ms                                   │
│ average response time: 5ms                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ วิธีการรันโปรเจกต์และการทดสอบในเครื่อง

### 1. เปิดใช้งาน Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. รัน Unit Test & Integration Test (Pytest)
```powershell
pytest -v
pytest --cov=app --cov-report=term-missing
```

### 3. รัน Newman Automated Test (รันทั้งระบบแบบอัตโนมัติ)
```powershell
python scripts/run_postman.py
```
*(เมื่อรันจบจะสร้างรายงาน HTML ที่ `reports/postman-report.html`)*

### 4. รัน Web Server สำหรับทดลองเรียก API / Swagger UI
```powershell
uvicorn app.main:app --reload --port 8000
```
เปิดดูเอกสาร API ได้ที่: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
