import pytest
import json
import jwt
import sys
import os
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app and necessary functions
from app import (
    app,
    JWT_SECRET,
    create_token,
    generate_test_token,
    validate_token_structure,
    extract_token_details,
    MAX_TOKEN_LENGTH,
    MIN_TOKEN_LENGTH,
)


class TestAuthService:
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask application"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_validate_token_structure(self):
        """Test comprehensive token structure validation"""
        # Valid token
        valid_token = create_token(1, "test@example.com", "User")
        is_valid, error = validate_token_structure(valid_token)
        assert is_valid, f"Token validation failed: {error}"

        # Empty token
        is_valid, error = validate_token_structure("")
        assert not is_valid
        assert "Empty token" in error

        # Too long token
        long_token = "x" * (MAX_TOKEN_LENGTH + 1)
        is_valid, error = validate_token_structure(long_token)
        assert not is_valid
        assert "exceeds maximum length" in error

        # Too short token
        short_token = "x" * (MIN_TOKEN_LENGTH - 1)
        is_valid, error = validate_token_structure(short_token)
        assert not is_valid
        assert "shorter than minimum length" in error

    def test_extract_token_details(self):
        """Test token details extraction"""
        token = create_token(42, "user@example.com", "User")
        details = extract_token_details(token)

        assert details["user_id"] == 42
        assert details["email"] == "user@example.com"
        assert details["token_type"] == "User"
        assert "issued_at" in details

    def test_validate_admin_token(self, client):
        """Test token validation for an Admin user"""
        admin_token = create_token(1, "admin@example.com", "Admin")

        response = client.post(
            "/api/auth/validate",
            data=json.dumps({"accessToken": admin_token}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["valid"] is True
        assert data["role"] == "Admin"
        assert "full_access" in data["permissions"]
        assert data["access_level"] == 10

    def test_validate_user_token(self, client):
        """Test token validation for a User"""
        user_token = create_token(2, "user@example.com", "User")

        response = client.post(
            "/api/auth/validate",
            data=json.dumps({"accessToken": user_token}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["valid"] is True
        assert data["role"] == "User"
        assert "read_only" in data["permissions"]
        assert data["access_level"] == 5

    def test_validate_invalid_role_token(self, client):
        """Test token validation with an invalid role"""
        # Generate a token with a non-standard role
        payload = {
            "id": 3,
            "email": "invalid@example.com",
            "type": "InvalidRole",
            "exp": datetime.utcnow().timestamp() + 3600,
        }
        invalid_role_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        response = client.post(
            "/api/auth/validate",
            data=json.dumps({"accessToken": invalid_role_token}),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["valid"] is False
        assert data["error_code"] == "INVALID_ROLE"

    def test_validate_missing_role_token(self, client):
        """Test token validation with a token missing role"""
        # Generate a token without a role
        payload = {
            "id": 4,
            "email": "norole@example.com",
            "exp": datetime.utcnow().timestamp() + 3600,
        }
        no_role_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        response = client.post(
            "/api/auth/validate",
            data=json.dumps({"accessToken": no_role_token}),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["valid"] is False
        assert data["error_code"] == "MISSING_ROLE"

    def test_validate_expired_token(self, client):
        """Test token validation with an expired token"""
        expired_token = generate_test_token("User", expired=True)

        response = client.post(
            "/api/auth/validate",
            data=json.dumps({"accessToken": expired_token}),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["valid"] is False
        assert data["error_code"] == "EXPIRED_TOKEN"

    def test_validate_missing_token(self, client):
        """Test token validation without providing a token"""
        # Test empty JSON
        response = client.post(
            "/api/auth/validate", data=json.dumps({}), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["valid"] is False
        assert data["error_code"] == "NO_TOKEN"

        # Test without JSON data
        response = client.post("/api/auth/validate", content_type="application/json")

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["valid"] is False
        assert data["error_code"] == "INVALID_REQUEST"

    def test_validate_malformed_token(self, client):
        """Test token validation with a malformed token"""
        # Malformed base64
        malformed_token = "invalid.token.here"

        response = client.post(
            "/api/auth/validate",
            data=json.dumps({"accessToken": malformed_token}),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["valid"] is False
        assert data["error_code"] == "INVALID_TOKEN_STRUCTURE"

    def test_validate_long_token(self, client):
        """Test validation with an extremely long token"""
        long_token = "x" * (MAX_TOKEN_LENGTH + 1)

        response = client.post(
            "/api/auth/validate",
            data=json.dumps({"accessToken": long_token}),
            content_type="application/json",
        )

        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["valid"] is False
        assert data["error_code"] == "INVALID_TOKEN_STRUCTURE"


# import pytest
# import json
# from datetime import datetime, timedelta
# import jwt
# import sys
# import os

# # Add the project directory to the Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Import the app and necessary functions
# from app import app, JWT_SECRET, create_token, generate_test_token

# class TestAuthService:
#     @pytest.fixture
#     def client(self):
#         """Create a test client for the Flask application"""
#         app.config['TESTING'] = True
#         with app.test_client() as client:
#             yield client

#     def test_validate_admin_token(self, client):
#         """Test token validation for an Admin user"""
#         admin_token = create_token(1, "admin@example.com", "Admin")

#         response = client.post(
#             "/api/auth/validate",
#             data=json.dumps({"accessToken": admin_token}),
#             content_type='application/json'
#         )

#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data['valid'] is True
#         assert data['role'] == "Admin"
#         assert "full_access" in data['permissions']

#     def test_validate_user_token(self, client):
#         """Test token validation for a User"""
#         user_token = create_token(2, "user@example.com", "User")

#         response = client.post(
#             "/api/auth/validate",
#             data=json.dumps({"accessToken": user_token}),
#             content_type='application/json'
#         )

#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data['valid'] is True
#         assert data['role'] == "User"
#         assert "read_only" in data['permissions']

#     def test_validate_invalid_role_token(self, client):
#         """Test token validation with an invalid role"""
#         # Generate a token with a non-standard role
#         payload = {
#             "id": 3,
#             "email": "invalid@example.com",
#             "type": "InvalidRole",
#             "exp": datetime.utcnow() + timedelta(hours=1)
#         }
#         invalid_role_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

#         response = client.post(
#             "/api/auth/validate",
#             data=json.dumps({"accessToken": invalid_role_token}),
#             content_type='application/json'
#         )

#         assert response.status_code == 401
#         data = json.loads(response.data)
#         assert data['valid'] is False
#         assert "Invalid user role" in data['message']

#     def test_validate_expired_token(self, client):
#         """Test token validation with an expired token"""
#         expired_token = generate_test_token("User", expired=True)

#         response = client.post(
#             "/api/auth/validate",
#             data=json.dumps({"accessToken": expired_token}),
#             content_type='application/json'
#         )

#         assert response.status_code == 401
#         data = json.loads(response.data)
#         assert data['valid'] is False
#         assert data['message'] == "Token has expired"

#     def test_validate_missing_token(self, client):
#         """Test token validation without providing a token"""
#         response = client.post(
#             "/api/auth/validate",
#             data=json.dumps({}),
#             content_type='application/json'
#         )

#         assert response.status_code == 400
#         data = json.loads(response.data)
#         assert data['valid'] is False
#         assert data['message'] == "No access token provided"

#     def test_validate_malformed_token(self, client):
#         """Test token validation with a malformed token"""
#         response = client.post(
#             "/api/auth/validate",
#             data=json.dumps({"accessToken": "invalid_token"}),
#             content_type='application/json'
#         )

#         assert response.status_code == 401
#         data = json.loads(response.data)
#         assert data['valid'] is False
#         assert data['message'] == "Invalid token structure"

#     def test_validate_long_token(self, client):
#         """Test validation with an extremely long token"""
#         long_token = "x" * 1000

#         response = client.post(
#             "/api/auth/validate",
#             data=json.dumps({"accessToken": long_token}),
#             content_type='application/json'
#         )

#         assert response.status_code == 401
#         data = json.loads(response.data)
#         assert data['valid'] is False
#         assert data['message'] == "Token is too long"

#     def test_validate_token_multiple_content_types(self, client):
#         """Test token validation with different content types"""
#         admin_token = create_token(1, "admin@example.com", "Admin")

#         content_types = [
#             'application/json',
#             'application/x-www-form-urlencoded',
#             'multipart/form-data'
#         ]

#         for content_type in content_types:
#             response = client.post(
#                 "/api/auth/validate",
#                 data=json.dumps({"accessToken": admin_token}),
#                 content_type=content_type
#             )

#             assert response.status_code in [200, 400, 401], f"Failed with {content_type}"
