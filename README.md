# 📝 FastAPI To-Do App

A secure and modern To-Do List REST API built with **FastAPI**, featuring:

- 🔒 JWT Access and Refresh Token Authentication
- ✅ User Registration & Login
- 🔁 Token Refresh & Logout
- 📋 CRUD Operations for To-Do Tasks
- 🧠 SQLAlchemy + SQLite
- 🔐 Password Hashing (bcrypt)

---

## 🚀 Features

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| User Registration      | Register with a unique username, email, and password                       |
| JWT Authentication     | Secure login system with `access_token` and `refresh_token`                |
| Token Refresh          | Request a new access token using a valid refresh token                     |
| Logout                 | Revoke a refresh token to log out                                           |
| CRUD To-Dos            | Create, Read, Update, and Delete tasks (protected routes)                  |
| ORM Integration        | SQLAlchemy with SQLite database                                             |
| Secure Passwords       | Passwords are hashed using `bcrypt`                                         |
| CORS Enabled           | CORS configured for API access from frontend or Postman                    |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Uvicorn**
- **Passlib + Bcrypt**
- **Python-JOSE** (for JWT)
- **Postman** (for testing)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fastapi-todo-app.git
cd fastapi-todo-app
````

### 2. Create & Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

* API will be running at: `http://127.0.0.1:8000`
* Swagger docs: `http://127.0.0.1:8000/docs`

---

## ⚙️ Configuration (`.env`)

Create a `.env` file in the root directory:

```ini
# JWT secrets
SECRET_KEY=supersecretaccesskey
REFRESH_SECRET_KEY=supersecretrefreshkey
ALGORITHM=HS256

# Token expiry
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database URL
DATABASE_URL=sqlite:///./todo.db
```

---

## 📮 API Endpoints Overview

### 🔐 Authentication

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| POST   | `/register`      | Register a new user      |
| POST   | `/login`         | Login and receive tokens |
| POST   | `/refresh-token` | Get a new access token   |
| POST   | `/logout`        | Revoke refresh token     |

---

### 📋 To-Do Management (Requires Authentication)

| Method | Endpoint      | Description          |
| ------ | ------------- | -------------------- |
| GET    | `/todos/`     | List all to-dos      |
| POST   | `/todos/`     | Create a new to-do   |
| PUT    | `/todos/{id}` | Update a to-do by ID |
| DELETE | `/todos/{id}` | Delete a to-do by ID |

> ✅ Add `Authorization: Bearer <access_token>` header to all To-Do routes.

---

## 🧪 Testing with Postman

A complete Postman testing guide is available in the [Postman Test Guide](postman_test_guide.md).

Or import this sample request manually:

```http
POST /register
Content-Type: application/json

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "strongpassword123"
}
```

---

## 📁 Project Structure

```
todo_api/
├── app/
│   ├── routes/
│   │   ├── todo.py
│   │   └── user.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── venv/
├── .env
├── README.md
├── /gitignore
└── todo.db
```

---

## 🔐 Security Notes

* Passwords are hashed with **bcrypt** using `passlib`.
* Tokens are signed with secure secrets and expiry.
* Refresh tokens are stored in DB and marked as revoked on logout.

---

## 📄 License

[MIT License](LICENSE). Feel free to fork and contribute!

---

Roadmap Project URL: https://roadmap.sh/projects/todo-list-api
