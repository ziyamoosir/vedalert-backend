import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("C:/Users/ziyam/vedalert-backend/firebase/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
