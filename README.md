# User and Destination Services

## Overview

A microservices-based travel management application with robust authentication and destination management capabilities.

## Features

- **Secure Authentication**: JWT-based user authentication
- **Role-Based Access Control**: 
  - Admin and User roles with different permission levels
  - Secure destination management
- **Microservices Architecture**:
  - Users Service
  - Destinations Service
  - Authentication Service
- **Comprehensive Test Coverage**

## 🛠 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/fahiiiiii/TravelManagementwithMicroservices.git
cd TravelManagementwithMicroservices
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running Services

### Users Service
```bash
cd users_service
flask run
# Runs on http://127.0.0.1:5000
```

### Authentication Service
```bash
cd auth_service
flask run
# Runs on http://127.0.0.1:5001
```

### Destinations Service
```bash
cd destinations_service
flask run
# Runs on http://127.0.0.1:5002
```


## Running Tests

### Users Service Tests
```bash
pytest --cov=app --maxfail=1 --disable-warnings -v users_service/test_app.py
```

### Destinations Service Tests
```bash
pytest --cov=app test_destinations_service.py --cov-report=term
```

### Authentication Service Tests
```bash
pytest --cov=. --cov-report=term-missing test_auth_service.py
```

## API Endpoints

### Authentication Service

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/auth/validate` | POST | Validate JWT token | All Roles |

#### Token Validation Request
```json
{
  "accessToken": "jwt_token_here"
}
```

#### Token Validation Response
```json
{
  "valid": true,
  "role": "Admin",
  "permissions": ["full_access"],
  "access_level": 10,
  "token_details": {
    "user_id": 1,
    "email": "admin@example.com",
    "token_type": "Admin"
  }
}
```

### Users Service

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/register` | POST | Register a new user |
| `/api/users/login` | POST | Obtain an access token |
| `/api/users/profile` | GET | Retrieve user profile |

### Destinations Service

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/destinations/all` | GET | Get all destinations |
| `/api/destinations/create` | POST | Create a destination (admin only) |
| `/api/destinations/{id}` | GET | Get a specific destination |
| `/api/destinations/{id}/delete` | DELETE | Delete a destination (admin only) |

## Authentication Mechanism

The system uses JSON Web Tokens (JWT) for authentication with two primary roles:

1. **Admin Role**:
   - Full access to all services
   - Can create, update, and delete destinations
   - Highest access level (10)

2. **User Role**:
   - Read-only access
   - Limited permissions
   - Lower access level (5)

### Token Validation Process
1. Generate JWT token during login
2. Send token to `/api/auth/validate`
3. Validate token structure and expiration
4. Check user role and permissions
5. Return authorization status

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Write tests
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License

## Acknowledgments

- Flask
- Pytest
- JSON Web Tokens (JWT)
- Flask-RESTX

