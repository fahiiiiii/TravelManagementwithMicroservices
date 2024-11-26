import os
import re
from typing import Dict, Any, Tuple
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import jwt
import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Configure API with Swagger documentation
api = Api(
    app,
    title="Authentication Service",
    version="1.0",
    description="Comprehensive Token Validation and Authorization Service",
)

# JWT Configuration with additional security measures
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret_key")
TOKEN_EXPIRATION = timedelta(hours=1)
MAX_TOKEN_LENGTH = 500  # Maximum allowed token length
MIN_TOKEN_LENGTH = 10  # Minimum allowed token length

# Token validation model
token_model = api.model(
    "TokenValidation",
    {
        "accessToken": fields.String(
            required=True,
            description="JWT Access Token",
            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        )
    },
)


def validate_token_structure(token: str) -> Tuple[bool, str]:
    """
    Comprehensive token structure validation

    :param token: JWT token to validate
    :return: Tuple of (is_valid, error_message)
    """
    # Check token length
    if not token:
        return False, "Empty token provided"

    if len(token) > MAX_TOKEN_LENGTH:
        return False, f"Token exceeds maximum length of {MAX_TOKEN_LENGTH}"

    if len(token) < MIN_TOKEN_LENGTH:
        return False, f"Token is shorter than minimum length of {MIN_TOKEN_LENGTH}"

    # Check token format (basic JWT structure)
    parts = token.split(".")
    if len(parts) != 3:
        return False, "Invalid token format: must have 3 parts"

    # Validate base64 encoding of token parts
    try:
        for part in parts:
            base64.urlsafe_b64decode(part + "=" * (-len(part) % 4))
    except Exception:
        return False, "Token contains invalid base64 encoding"

    return True, ""


def extract_token_details(token: str) -> Dict[str, Any]:
    """
    Extract additional details from the token

    :param token: JWT token
    :return: Dictionary of token details
    """
    try:
        # Decode without verification to extract payload
        unverified_payload = jwt.decode(token, options={"verify_signature": False})

        # Additional token detail extraction
        return {
            "user_id": unverified_payload.get("id"),
            "email": unverified_payload.get("email"),
            "issued_at": unverified_payload.get("iat"),
            "token_type": unverified_payload.get("type"),
        }
    except Exception:
        return {}


@api.route("/api/auth/validate")
class AuthorizationResource(Resource):
    @api.expect(token_model)
    def post(self):
        """
        Comprehensive token validation endpoint

        Validates JWT token, checks user authorization,
        and provides detailed authorization information
        """
        # Validate request data
        if not request.json:
            return {
                "message": "Invalid request format",
                "valid": False,
                "error_code": "INVALID_REQUEST",
            }, 400

        # Extract access token
        access_token = request.json.get("accessToken")
        if not access_token:
            return {
                "message": "No access token provided",
                "valid": False,
                "error_code": "NO_TOKEN",
            }, 400

        # Validate token structure first
        is_valid_structure, structure_error = validate_token_structure(access_token)
        if not is_valid_structure:
            return {
                "message": structure_error,
                "valid": False,
                "error_code": "INVALID_TOKEN_STRUCTURE",
            }, 401

        try:
            # Decode and verify token
            decoded_token = jwt.decode(access_token, JWT_SECRET, algorithms=["HS256"])

            # Extract user role with comprehensive checks
            user_role = decoded_token.get("type")
            if not user_role:
                return {
                    "message": "Unauthorized: Missing user role",
                    "valid": False,
                    "error_code": "MISSING_ROLE",
                }, 401

            # Comprehensive authorization logic
            role_permissions = {
                "Admin": {
                    "permissions": ["full_access", "modify_destinations"],
                    "access_level": 10,
                },
                "User": {"permissions": ["read_only"], "access_level": 5},
            }

            # Get role-specific permissions
            role_config = role_permissions.get(user_role)
            if not role_config:
                return {
                    "message": f"Unauthorized: Invalid role '{user_role}'",
                    "valid": False,
                    "error_code": "INVALID_ROLE",
                }, 401

            # Additional token details
            token_details = extract_token_details(access_token)

            return {
                "message": "Authorized",
                "valid": True,
                "role": user_role,
                "permissions": role_config["permissions"],
                "access_level": role_config["access_level"],
                "token_details": token_details,
                "expiration": decoded_token.get("exp"),
            }, 200

        except jwt.ExpiredSignatureError:
            return {
                "message": "Token has expired",
                "valid": False,
                "error_code": "EXPIRED_TOKEN",
            }, 401
        except jwt.InvalidTokenError:
            return {
                "message": "Invalid token",
                "valid": False,
                "error_code": "INVALID_TOKEN",
            }, 401
        except Exception as e:
            # Catch-all for any unexpected errors
            return {
                "message": f"Unexpected error: {str(e)}",
                "valid": False,
                "error_code": "UNEXPECTED_ERROR",
            }, 500


def generate_test_token(
    user_id=1, email="test@example.com", role="User", expires_in=1, expired=False
):
    """
    Utility function to generate test tokens with extensive configuration

    :param user_id: User identifier
    :param email: User email
    :param role: User role (Admin/User)
    :param expires_in: Token expiration in hours
    :param expired: Force token expiration
    :return: JWT token
    """
    # Use current time for precise control
    now = datetime.utcnow()

    payload = {
        "id": user_id,
        "email": email,
        "type": role,
        "iat": now.timestamp(),  # Issued at time
        "exp": (
            now - timedelta(hours=1) if expired else now + timedelta(hours=expires_in)
        ).timestamp(),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


# Expose token generation for testing
def create_token(user_id, email, role, expires_in=1):
    return generate_test_token(user_id, email, role, expires_in)


if __name__ == "__main__":
    app.run(port=5001)


# # # auth_service/app.py

# from flask import Flask, request
# from flask_restx import Api, Resource, fields
# import jwt
# import os
# from dotenv import load_dotenv

# app = Flask(__name__)
# load_dotenv()

# # API configuration
# api = Api(
#     app,
#     title="Authentication Service",
#     version="1.0",
#     description="Token Validation and Authorization Service"
# )

# # JWT Secret Key
# JWT_SECRET = os.getenv("JWT_SECRET", "default_secret_key")

# # Authorization model
# token_model = api.model(
#     "TokenValidation",
#     {
#         "accessToken": fields.String(
#             required=True,
#             description="JWT Access Token",
#             example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
#         )
#     }
# )

# @api.route("/api/auth/validate")
# class AuthorizationResource(Resource):
#     @api.expect(token_model)
#     def post(self):
#         """
#         Validate access token and check user authorization

#         Validates the JWT token and provides authorization details.
#         Checks if the user is an Admin or User and their permissions.
#         """
#         data = request.json

#         # Check if token is provided
#         if not data or 'accessToken' not in data:
#             return {"message": "No access token provided"}, 400

#         try:
#             # Decode and verify token
#             decoded_token = jwt.decode(
#                 data['accessToken'],
#                 JWT_SECRET,
#                 algorithms=["HS256"]
#             )

#             # Extract user role
#             user_role = decoded_token.get('type')

#             # Authorization logic
#             if user_role == 'Admin':
#                 return {
#                     "message": "Authorized",
#                     "role": "Admin",
#                     "description": "You have full access to destinations service. All actions are permitted."
#                 }, 200
#             elif user_role == 'User':
#                 return {
#                     "message": "Authorized",
#                     "role": "User",
#                     "description": "You are not authorized to perform admin actions on destinations service."
#                 }, 403
#             else:
#                 return {
#                     "message": "Unauthorized",
#                     "description": "Unknown user"
#                 }, 401

#         except jwt.ExpiredSignatureError:
#             return {"message": "Token has expired"}, 401
#         except jwt.InvalidTokenError:
#             return {"message": "Invalid token"}, 401

# if __name__ == "__main__":
#     app.run(port=5001)
