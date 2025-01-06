from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app.models import db, User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return "Welcome to the Ads Website!", 200

@main.route('/register', methods=['POST'])
def register():
    try:
        # Получаем данные из запроса
        data = request.get_json()
        print(f"Received data: {data}")  # Лог

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Проверяем обязательные поля
        if not username or not email or not password:
            print("Error: Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        # Хэшируем пароль
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Проверяем уникальность пользователя
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            print("Error: User already exists")
            return jsonify({"error": "User already exists"}), 409

        # Добавляем нового пользователя
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} added to the database")

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        print(f"Error during user registration: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
@main.route('/login', methods=['POST'])
def login():
    try:
        # Получаем данные из запроса
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Проверяем, существует ли пользователь
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

        # Проверяем пароль
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid username or password"}), 401

        return jsonify({"message": f"Welcome back, {username}!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500 
    
    
    

# commit 2: Feature-register: created route /register, database, model class User
# from flask import Blueprint, request, jsonify
# from werkzeug.security import generate_password_hash
# from app.models import db, User

# main = Blueprint('main', __name__)

# @main.route('/', methods=['GET'])
# def home():
#     return "Welcome to the Ads Website!", 200

# @main.route('/register', methods=['POST'])
# def register():
#     try:
#         # Получаем данные из запроса
#         data = request.get_json()
#         print(f"Received data: {data}")  # Лог

#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')

#         # Проверяем обязательные поля
#         if not username or not email or not password:
#             print("Error: Missing required fields")
#             return jsonify({"error": "Missing required fields"}), 400

#         # Хэшируем пароль
#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

#         # Проверяем уникальность пользователя
#         existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
#         if existing_user:
#             print("Error: User already exists")
#             return jsonify({"error": "User already exists"}), 409

#         # Добавляем нового пользователя
#         new_user = User(username=username, email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         print(f"User {username} added to the database")

#         return jsonify({"message": "User registered successfully!"}), 201
#     except Exception as e:
#         print(f"Error during user registration: {e}")
#         return jsonify({"error": "An error occurred"}), 500



# commit 1: Flask project structure and home page route added
# from flask import Blueprint, jsonify

# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     return jsonify({"message": "Welcome to the Ads Website!"})