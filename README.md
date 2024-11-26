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






----------------------------------------------------------------------------------------

## Overview
This project consists of two independent services:
1. **Users Service**: Manages user authentication, registration, and profile retrieval.
2. **Destinations Service**: Handles CRUD operations for destinations with role-based access control.

Both services use **Flask** as the web framework and **JWT** (JSON Web Tokens) for user authentication.

---

## Features
- **JWT Authentication**: Secure login and user profile management using tokens.
- **Role-Based Access Control**: Only admins can create or delete destinations.
- **CRUD Operations**: Create, read, update, and delete destinations.
- **Test Coverage**: Unit tests with coverage reporting for both services.

---

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/fahiiiiii/TravelManagementwithMicroservices/tree/main
   cd TravelManagementwithMicroservices
Create a virtual environment:

bash
Copy code
python3 -m venv venv
Activate the virtual environment:

On macOS/Linux:
bash
Copy code
source venv/bin/activate
On Windows:
bash
Copy code
venv\Scripts\activate
Install required dependencies:

bash
Copy code
pip install -r requirements.txt
Configuration
JWT Secret: The JWT secret key is defined in the JWT_SECRET variable. Make sure it is set correctly for both services.
Database: The services currently use in-memory databases (users_db for users and destinations_db for destinations). For persistent storage, consider integrating a proper database like SQLite or PostgreSQL.
Running the Services
To run each service, use Flask’s development server.

### Users Service:
Navigate to the users_service directory:

bash
cd users_service
Start the Flask development server:

bash
flask run
The Users Service will run on http://127.0.0.1:5000.


### Destinations Service:
Navigate to the destinations_service directory:
bash
cd destinations_service
Start the Flask development server:

bash
flask run
The Destinations Service will run on http://127.0.0.1:5001.


###  Running Tests
#### Users Service Tests
Run the tests for the Users Service:


pytest --cov=app --maxfail=1 --disable-warnings -v users_service/test_app.py

#### Destinations Service Tests
Run the tests for the Destinations Service:


pytest --cov=app test_destinations_service.py --cov-report=term

### API Documentation
Users Service API
POST /api/users/register: Register a new user.

Request Body: { "name": "John Doe", "email": "john@example.com", "password": "password123", "role": "User" }
Response: { "Message": "Registration successful as User", "User": { "email": "john@example.com" } }
POST /api/users/login: Log in and obtain an access token.

Request Body: { "email": "john@example.com", "password": "password123" }
Response: { "accessToken": "jwt_token_here" }
GET /api/users/profile: Retrieve the logged-in user's profile based on the provided JWT token.

Headers: { "Authorization": "Bearer jwt_token_here" }
Response: { "Message": "Profile retrieved successfully", "User": { "email": "john@example.com" } }
Destinations Service API
GET /api/destinations/all: Get all destinations.

Headers: { "accessToken": "jwt_token_here" }
Response: [ { "id": 1, "name": "Paris", "location": "Europe" }, { "id": 2, "name": "Tokyo", "location": "Asia" } ]
POST /api/destinations/create: Create a new destination (admin only).

Request Body: { "name": "New York", "description": "The Big Apple", "location": "North America" }
Response: { "id": 3, "name": "New York", "description": "The Big Apple", "location": "North America" }
GET /api/destinations/{id}: Get a specific destination by ID.

Response: { "id": 1, "name": "Paris", "description": "Capital of France", "location": "Europe" }
DELETE /api/destinations/{id}/delete: Delete a destination by ID (admin only).

Response: { "Message": "Destination deleted" }
Contributing
We welcome contributions to this project! If you'd like to contribute, follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and write tests for them.
Ensure all tests pass.
Submit a pull request with a description of your changes.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Flask: Web framework used for building the services.
Pytest: Testing framework used for writing and running tests.
JWT: JSON Web Tokens used for authentication.
