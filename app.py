from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore
from functools import wraps

app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:/Users/ziyam/vedalert-backend/firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

def verify_firebase_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"error": "Invalid Authorization header"}), 401

        id_token = parts[1]
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            request.user = decoded_token  # Save user info for route usage
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def home():
    return "VedAlert backend is running!"

@app.route('/protected', methods=['GET'])
@verify_firebase_token
def protected():
    user = getattr(request, "user", None)
    uid = user.get('uid')

    # Fetch user role from Firestore
    user_doc = db.collection('users').document(uid).get()
    if user_doc.exists:
        role = user_doc.to_dict().get('role', 'User')
    else:
        role = 'User'  # default role if not found

    return jsonify({
        "message": f"You are authorized! Hello {user.get('email', 'user')}",
        "role": role
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
