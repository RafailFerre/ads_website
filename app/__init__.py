from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Настройки приложения
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Роуты
    from .routes import main
    app.register_blueprint(main)

    return app