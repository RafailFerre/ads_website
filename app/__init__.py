import os
from flask import Flask
from .models import db


def create_app():
    app = Flask(__name__)

    # Установите секретный ключ
    app.secret_key = os.urandom(24)  # Генерация случайного ключа
    # Или установите вручную (рекомендуется для продакшена):
    # app.secret_key = "your-very-secure-secret-key"

    # Настройка базы данных
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)

    # Создание базы данных
    with app.app_context():
        db.create_all()
        print("Database and tables created!")
    # Роуты
    from .routes import main, ads
    app.register_blueprint(main)
    app.register_blueprint(ads)
    
    
    # Путь для сохранения аватаров
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Ограничение на размер файла (2MB)

    return app


# import os
# from flask import Flask
# from .models import db

# def create_app():
#     app = Flask(__name__)

#     # Настройка базы данных
#     BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)

#     # Создание базы данных
#     with app.app_context():
#         db.create_all()
#         print("Database and tables created!")

#     # Роуты
#     from .routes import main, ads
#     app.register_blueprint(main)
#     app.register_blueprint(ads)

#     return app





# commit 1: Flask project structure and home page route added
# from flask import Flask

# def create_app():
#     app = Flask(__name__)
    
#     # Настройки приложения
#     app.config['SECRET_KEY'] = 'your_secret_key'

#     # Роуты
#     from .routes import main
#     app.register_blueprint(main)

#     return app