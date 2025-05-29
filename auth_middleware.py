from flask import request, jsonify
from functools import wraps
from firebase_admin import auth as firebase_auth

def verify_firebase_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        # The token should be in the format "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"error": "Invalid Authorization header"}), 401

        id_token = parts[1]
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            request.user = decoded_token  # Optionally save user info to request for later use
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return f(*args, **kwargs)
    return wrapper
