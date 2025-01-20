import jwt
from functools import wraps
from flask import request, jsonify
from app.models import User

SECRET_KEY = "token_secret_key"  # Замените на надёжный ключ

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Извлекаем токен из заголовка Authorization
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  # Убираем 'Bearer'

        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["user_id"])
            if not current_user:
                raise ValueError("User not found.")
        except Exception as e:
            print(f"Token decode error: {e}")
            return jsonify({"error": "Invalid token!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated

# 2nd variant of token_required method for frontend
# import jwt
# from functools import wraps
# from flask import request, jsonify
# from app.models import User

# SECRET_KEY = "token_secret_key"  # Используйте надёжный и уникальный секретный ключ

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         # Извлекаем токен из заголовка Authorization
#         if "Authorization" in request.headers:
#             auth_header = request.headers["Authorization"]
#             if auth_header.startswith("Bearer "):  # Проверяем формат
#                 token = auth_header.split(" ")[1]

#         if not token:
#             return jsonify({"error": "Token is missing!"}), 403

#         try:
#             # Декодируем токен
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             current_user = User.query.get(data.get("user_id"))  # Получаем пользователя
#             if not current_user:
#                 return jsonify({"error": "User not found!"}), 404
#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token has expired!"}), 403
#         except jwt.InvalidTokenError:
#             return jsonify({"error": "Invalid token!"}), 403
#         except Exception as e:
#             print(f"Unexpected token decode error: {e}")
#             return jsonify({"error": "Invalid token!"}), 403

#         # Передаём текущего пользователя в функцию
#         return f(current_user, *args, **kwargs)

#     return decorated





# commit 6: before frontend
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({"error": "Token is missing!"}), 403

#         try:
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             current_user = User.query.get(data['user_id'])
#         except Exception as e:
#             print(f"Token decode error: {e}")
#             return jsonify({"error": "Invalid token!"}), 403

#         return f(current_user, *args, **kwargs)

#     return decorated
