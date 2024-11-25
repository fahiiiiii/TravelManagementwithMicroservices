# User and Destination Services

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
   git clone https://github.com/yourusername/project-name.git](https://github.com/fahiiiiii/TravelManagementwithMicroservices
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
Users Service Tests
Run the tests for the Users Service:

bash
pytest --cov=app --maxfail=1 --disable-warnings -v users_service/test_app.py
Destinations Service Tests
Run the tests for the Destinations Service:

bash
pytest --cov=app test_destinations_service.py --cov-report=term
API Documentation
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
