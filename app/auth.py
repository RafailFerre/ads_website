import jwt
from functools import wraps
from flask import request, jsonify
from app.models import User

SECRET_KEY = "token_secret_key"  # Замените на надёжный ключ

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except Exception as e:
            print(f"Token decode error: {e}")
            return jsonify({"error": "Invalid token!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated
