# Postman Testing Guide for FastAPI To-Do List API

This is a complete, professional **Postman testing guide** for your FastAPI To-Do List API with:
✅ User registration  
✅ Email-based login  
✅ JWT + Refresh tokens  
✅ Logout  
✅ CRUD for to-dos  
✅ Pagination, filtering, and protected routes

---

## 🧪 Postman Collection Setup

### 🔧 Base URL (if using Uvicorn locally):
```http
http://127.0.0.1:8000
```

---

## ✅ 1. Register New User

**POST** `/register`
- **URL:** `POST /register`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "email": "testuser@example.com",
  "username": "testuser",
  "password": "password123"
}
```

✅ **Expected:** 201 Created  
✅ **Returns:** `{ "id": 1, "email": "...", "username": "..." }`

---

## ✅ 2. Login to Get Access and Refresh Tokens

**POST** `/login`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "email": "testuser@example.com",
  "password": "password123"
}
```

✅ **Returns:**
```json
{
  "access_token": "jwt...",
  "refresh_token": "refresh.jwt...",
  "token_type": "bearer"
}
```

📌 Save the `access_token` and `refresh_token` for use in next steps.

---

## ✅ 3. Create a To-Do Item (Authenticated)

**POST** `/todos/`
- **Headers:**
    - `Authorization: Bearer <access_token>`
    - `Content-Type: application/json`
- **Body:**
```json
{
  "title": "Write Postman Guide",
  "description": "Document all endpoints and testing steps",
  "status": "not_done"
}
```

✅ **Returns:** To-do data with `id`, `title`, `owner_id`, etc.

---

## ✅ 4. Get All To-Dos (Authenticated, Paginated)

**GET** `/todos/?skip=0&limit=10`
- **Headers:**
    - `Authorization: Bearer <access_token>`

✅ **Returns:** A list of your todos  
✅ Supports pagination with `skip`, `limit`

---

## ✅ 5. Filter To-Dos by Status

**GET** `/todos/?status=done`  
✅ Returns only done items

---

## ✅ 6. Update a To-Do Item

**PUT** `/todos/{todo_id}`
- **URL:** `/todos/1`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
  "title": "Write API Test Guide",
  "status": "done"
}
```

✅ Updates the title and status

---

## ✅ 7. Delete a To-Do

**DELETE** `/todos/{todo_id}`
- **URL:** `/todos/1`
- **Headers:** `Authorization: Bearer <access_token>`

✅ Returns 204 No Content

---

## ✅ 8. Refresh Access Token

**POST** `/token/refresh`
- **Body:**
```json
{
  "refresh_token": "<your_refresh_token>"
}
```

✅ **Returns new `access_token`**
> Save and use this new `access_token` for future requests.

---

## ✅ 9. Logout

**POST** `/logout`
- **Headers:** `Authorization: Bearer <access_token>`

✅ Invalidates the refresh token stored in the DB (if implemented)  
✅ You'll need to log in again after logout

---

## ✅ 10. Get Current User Profile

**GET** `/users/me`
- **Headers:** `Authorization: Bearer <access_token>`

✅ Returns the currently authenticated user

---

## 🧪 Recommended Postman Organization

Create a collection like this:
```
📁 To-Do API Test Collection
├── 🔐 Register
├── 🔐 Login
├── 🔁 Refresh Token
├── ❌ Logout
├── 📄 Get Profile
├── ✅ Create Todo
├── 📃 Get Todos
├── 🔍 Filter Todos
├── ✏️ Update Todo
└── ❌ Delete Todo
```

You can **set access_token and refresh_token** as Postman environment variables to use in all requests automatically.

---