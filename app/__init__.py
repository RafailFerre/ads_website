import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)

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

    return app





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