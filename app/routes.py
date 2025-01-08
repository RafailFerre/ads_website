from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from app.models import db, User, Ad

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return """<h1>Welcome to the Ads Website!</h1> \n 
                <h2>Create a personal account, post ads and much more</h2> \n 
                    <button style="font-size: 80px;">Start</button>""", 200


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
    
    
# Получение информации о пользователе
@main.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    return jsonify(user_data), 200


# Обновление данных пользователя
@main.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    db.session.commit()
    return jsonify({"message": "User updated successfully!"}), 200


# Удаление пользователя
@main.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200


# Создать объявление
@main.route('/ad', methods=['POST'])
def create_ad():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        user_id = data.get('user_id')

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_ad = Ad(title=title, description=description, price=price, user_id=user_id)
        db.session.add(new_ad)
        db.session.commit()

        return jsonify({"message": "Ad created successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500

    
# Получить все объявления
@main.route('/ads', methods=['GET'])
def get_ads():
    ads = Ad.query.all()
    return jsonify([{
        "id": ad.id,
        "title": ad.title,
        "description": ad.description,
        "price": ad.price,
        "user_id": ad.user_id
    } for ad in ads]), 200

# Редактировать объявление
@main.route('/ad/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
    try:
        ad = Ad.query.get(ad_id)
        if not ad:
            return jsonify({"error": "Ad not found"}), 404

        data = request.get_json()
        ad.title = data.get('title', ad.title)
        ad.description = data.get('description', ad.description)
        ad.price = data.get('price', ad.price)

        db.session.commit()
        return jsonify({"message": "Ad updated successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500

# Удалить объявление
@main.route('/ad/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    try:
        ad = Ad.query.get(ad_id)
        if not ad:
            return jsonify({"error": "Ad not found"}), 404

        db.session.delete(ad)
        db.session.commit()
        return jsonify({"message": "Ad deleted successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
    
       
    
# commit 4: Feature-get-update-delete user: created routes get, update, delete user
# from flask import Blueprint, request, jsonify
# from werkzeug.security import generate_password_hash,check_password_hash
# from app.models import db, User

# main = Blueprint('main', __name__)

# @main.route('/', methods=['GET'])
# def home():
#     return """<h1>Welcome to the Ads Website!</h1> \n 
#                 <h2>Create a personal account, post ads and much more</h2> \n 
#                     <button style="font-size: 80px;">Start</button>""", 200


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
    
    
# @main.route('/login', methods=['POST'])
# def login():
#     try:
#         # Получаем данные из запроса
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')

#         # Проверяем, существует ли пользователь
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             return jsonify({"error": "Invalid username or password"}), 401

#         # Проверяем пароль
#         if not check_password_hash(user.password, password):
#             return jsonify({"error": "Invalid username or password"}), 401

#         return jsonify({"message": f"Welcome back, {username}!"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": "An error occurred"}), 500 
    
    
# # Получение информации о пользователе
# @main.route('/user/<int:id>', methods=['GET'])
# def get_user(id):
#     user = User.query.get(id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     user_data = {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email
#     }
#     return jsonify(user_data), 200


# # Обновление данных пользователя
# @main.route('/user/<int:id>', methods=['PUT'])
# def update_user(id):
#     user = User.query.get(id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     data = request.get_json()
#     if 'username' in data:
#         user.username = data['username']
#     if 'email' in data:
#         user.email = data['email']
#     if 'password' in data:
#         user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')

#     db.session.commit()
#     return jsonify({"message": "User updated successfully!"}), 200


# # Удаление пользователя
# @main.route('/user/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     user = User.query.get(id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({"message": "User deleted successfully!"}), 200  
    


# commit 3: Feature-login: created route login with password verification
# from flask import Blueprint, request, jsonify
# from werkzeug.security import generate_password_hash
# from werkzeug.security import check_password_hash
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
    
# @main.route('/login', methods=['POST'])
# def login():
#     try:
#         # Получаем данные из запроса
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')

#         # Проверяем, существует ли пользователь
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             return jsonify({"error": "Invalid username or password"}), 401

#         # Проверяем пароль
#         if not check_password_hash(user.password, password):
#             return jsonify({"error": "Invalid username or password"}), 401

#         return jsonify({"message": f"Welcome back, {username}!"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": "An error occurred"}), 500 


    

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