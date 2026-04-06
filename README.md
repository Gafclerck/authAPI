# Authentication & Email Verification API

A FastAPI-based authentication API with user registration, login, and email verification.

## 📋 What's Implemented

- **User Registration** - Email validation, password hashing with `pwdlib`
- **Secure Login** - JWT tokens (30-minute expiration)
- **Email Verification** - 6-digit codes with 10-minute expiration
- **User Profile** - Get authenticated user info
- **Account Deletion** - Delete user account
- **CORS Configuration** - Ready for frontend integration
- **SQLite Database** - SQLAlchemy ORM

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
VERIFICATION_CODE_EXPIRE_MINUTES=10
```

**⚠️ Important:** Generate a strong SECRET_KEY:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Run the API

```bash
cd app
uvicorn main:app --reload
```

Visit `http://localhost:8000` - API will be available at this address.

### 4. Interactive Docs

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📡 API Endpoints

### Authentication

| Method | Endpoint    | Description               |
| ------ | ----------- | ------------------------- |
| POST   | `/register` | Register new user         |
| POST   | `/login`    | Login to get access token |

### User (Requires Token)

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| GET    | `/me`             | Get current user profile |
| DELETE | `/delete-account` | Delete user account      |

### Email Verification

| Method | Endpoint     | Description                    |
| ------ | ------------ | ------------------------------ |
| POST   | `/send-code` | Send 6-digit verification code |
| POST   | `/verify`    | Verify email with code         |

## 📝 API Examples

### Register

Requires: `name` (1-100 chars), `email` (valid email), `password` (6-100 chars)

```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

Response:

```json
{
  "message": "Successfully registered",
  "status": 201
}
```

### Login

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepassword123"
```

Response:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Get Profile (with token)

```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "is_verified": false
}
```

### Send Verification Code

```bash
curl -X POST "http://localhost:8000/send-code" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "message": "Verification code sent to john@example.com",
  "code": "123456",
  "status": 200
}
```

### Verify Email

```bash
curl -X POST "http://localhost:8000/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "code": "123456"
  }'
```

### Delete Account

```bash
curl -X DELETE "http://localhost:8000/delete-account" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:

```json
{
  "message": "Your account is successfully deleted",
  "status": 200
}
```

## 📁 Project Structure

```
app/
├── main.py              # FastAPI app with CORS
├── config.py            # Configuration (env variables)
├── database.py          # SQLite setup
├── schema.py            # Pydantic models
├── security.py          # Password hashing & JWT
├── dependecies.py       # Authentication dependency
├── models/
│   ├── user.py          # User model
│   └── verification.py  # Verification code model
└── routes/
    ├── auth.py          # Register & Login
    ├── user.py          # Profile & Delete
    └── verification.py  # Send code & Verify
```

## 🔒 Security Features

- **Password Hashing** - `pwdlib` with salt and iterations
- **JWT Authentication** - HS256 algorithm, 30-minute expiration
- **Email Validation** - RFC 5322 compliant
- **Timing Attack Protection** - Dummy hash verification
- **CORS Support** - Ready for frontend/mobile apps
- **Input Validation** - Pydantic validators on all endpoints

### Validation Rules:

- **Password**: 6-100 characters
- **Name**: 1-100 characters
- **Email**: Valid email format
- **Code**: Exactly 6 digits

## 📦 Dependencies

```
Core:
  - fastapi (0.135.3)
  - uvicorn (0.42.0)
  - SQLAlchemy (2.0.49)

Validation:
  - pydantic (2.12.5)
  - email-validator (2.3.0)

Security:
  - PyJWT (2.12.1)
  - pwdlib (0.3.0)
  - python-multipart (0.0.22)

Utilities:
  - python-dotenv (1.2.2)
  - httptools (0.7.1)
  - watchfiles (1.1.1)
```

## 🌐 Deployment (Vercel)

### Prerequisites:

- GitHub repository
- Vercel account
- PostgreSQL or MongoDB (SQLite won't work on Vercel)

### Steps:

1. **Create `vercel.json`**:

```json
{
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

2. **Set Environment Variables on Vercel**:
   - `SECRET_KEY` (generate strong key)
   - `ALGORITHM=HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES=30`
   - `VERIFICATION_CODE_EXPIRE_MINUTES=10`
   - `DATABASE_URL` (if using PostgreSQL)

3. **Push to GitHub** and connect to Vercel

## 🐳 Docker (Local Testing)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Run:

```bash
docker build -t auth-api .
docker run -p 8000:8000 -e SECRET_KEY=your-key auth-api
```

## ✅ Status

- ✅ Functional
- ✅ Security basics implemented
- ✅ CORS configured
- ✅ Input validation
- ⚠️ SQLite (needs PostgreSQL for production)

**Last Updated**: April 2026  
**Version**: 1.0.0
{
"name": "John Doe",
"email": "john@example.com",
"is_verified": false
}

````

### Send Verification Code

```bash
curl -X POST "http://localhost:8000/send-code" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
````

### Verify Email

```bash
curl -X POST "http://localhost:8000/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "code": "123456"
  }'
```

### Delete Account

```bash
curl -X DELETE "http://localhost:8000/delete-account" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📁 Project Structure

```
app/
├── main.py              # FastAPI app
├── config.py            # Settings
├── database.py          # Database setup
├── schema.py            # Request/Response models
├── security.py          # Password & JWT handling
├── dependecies.py       # Authentication dependency
├── models/
│   ├── user.py          # User model
│   └── verification.py  # Verification code model
└── routes/
    ├── auth.py          # Register & Login
    ├── user.py          # Profile & Delete
    └── verification.py  # Send code & Verify
```

## 🔒 Security Features

- Password hashing with `pwdlib`
- JWT authentication (HS256)
- Email validation (Pydantic EmailStr)
- Timing attack protection in login
- 10-minute code expiration
- SQLite database

## 🌐 Deployment

### Vercel

1. Push to GitHub
2. Connect repo to Vercel
3. Create `vercel.json`:

```json
{
  "builds": [{ "src": "app/main.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "app/main.py" }]
}
```

### Render or Railway

1. Connect GitHub repo
2. Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Deploy

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📦 Dependencies

- fastapi
- uvicorn
- sqlalchemy
- pydantic
- python-jose
- pwdlib
- email-validator
- python-dotenv

---

**Status:** Working
**Last Updated:** April 2026
