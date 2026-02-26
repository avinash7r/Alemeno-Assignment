# Credit Approval System (Backend)

A Django + Django REST Framework based **Credit Approval System** that evaluates loan eligibility using historical customer and loan data.

The entire application is **fully dockerized** and runs using a single `docker compose` command with PostgreSQL as the database.

---

## 🚀 Tech Stack

- **Backend**: Django 4+, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **WSGI Server**: Gunicorn
- **Data Ingestion**: Pandas (Excel files)

---

## 📁 Project Structure

```

credit_system/
├── credit_system/        # Django project
├── customers/            # Customer app
├── loans/                # Loans + credit logic
├── data/                 # customer_data.xlsx, loan_data.xlsx
├── scripts/              # wait_for_db.sh
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── manage.py

````

---

## ⚙️ Setup & Run (One Command)

### Prerequisites
- Docker
- Docker Compose

### Run the application
```bash
docker compose up --build
````

This will automatically:

* Start PostgreSQL
* Apply migrations
* Ingest Excel data (`customer_data.xlsx`, `loan_data.xlsx`)
* Start the Django app using Gunicorn

The server will be available at:

```
http://127.0.0.1:8000
```

---

## 🔐 Environment Variables

Defined in `.env`:

```env
DEBUG=1
SECRET_KEY=secret-key

DB_NAME=credit_system
DB_USER=credit_user
DB_PASSWORD=credit_pass
DB_HOST=db
DB_PORT=5432
```

---

## 📊 Data Ingestion

Historical data is ingested at startup using **Django management commands**:

* `customer_data.xlsx` → `Customer` table
* `loan_data.xlsx` → `Loan` table

This satisfies the requirement of using **background workers** for initialization.

---

## 🔌 API Endpoints

### 1️⃣ Register Customer

**POST** `/api/register`

**Request**

```json
{
  "first_name": "Avi",
  "last_name": "Rajure",
  "age": 22,
  "monthly_income": 500000,
  "phone_number": "9999999999"
}
```

**Response**

```json
{
  "customer_id": 301,
  "name": "Avi Rajure",
  "age": 22,
  "monthly_income": 50000,
  "approved_limit": 1800000,
  "phone_number": "9999999999"
}
```

---

### 2️⃣ Check Loan Eligibility

**POST** `/api/check-eligibility`

**Request**

```json
{
  "customer_id": 1,
  "loan_amount": 50000,
  "interest_rate": 10,
  "tenure": 24
}
```

**Response**

```json
{
  "customer_id": 1,
  "approval": true,
  "interest_rate": 10,
  "corrected_interest_rate": 12,
  "tenure": 24,
  "monthly_installment": 23500.45
}
```

---

### 3️⃣ Create Loan

**POST** `/api/create-loan`

**Request**

```json
{
  "customer_id": 1,
  "loan_amount": 300000,
  "interest_rate": 10,
  "tenure": 12
}
```

**Response**

```json
{
  "loan_id": 15,
  "customer_id": 1,
  "loan_approved": true,
  "message": "Loan approved",
  "monthly_installment": 26498.34
}
```

---

### 4️⃣ View Loan Details

**GET** `/api/view-loan/<loan_id>`

**Response**

```json
{
  "id": 15,
  "customer": {
    "id": 1,
    "first_name": "Avi",
    "last_name": "Rajure",
    "phone_number": "9999999999",
    "age": 22
  },
  "loan_amount": 300000,
  "interest_rate": 12,
  "monthly_installment": 26498.34,
  "tenure": 12
}
```

---

### 5️⃣ View Customer Loans

**GET** `/api/view-loans/<customer_id>`

**Response**

```json
[
  {
    "id": 15,
    "loan_amount": 300000,
    "interest_rate": 12,
    "monthly_installment": 26498.34,
    "repayments_left": 12
  }
]
```

---

## 🧠 Credit Scoring Logic

Credit score (0–100) is calculated using:

* EMIs paid on time
* Number of loans
* Loan activity in current year
* Loan volume vs approved limit
* Hard fail if current debt exceeds approved limit

Eligibility rules are applied exactly as specified in the assignment.

---

## ✅ Assignment Requirements Covered

* ✔ Django 4+ with DRF
* ✔ PostgreSQL database
* ✔ Background data ingestion
* ✔ Dockerized application
* ✔ Single command startup
* ✔ Clean API design & separation of concerns

---


