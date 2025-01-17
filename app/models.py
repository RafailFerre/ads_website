from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_username = db.Column(db.String(80), nullable=False)
    # Указание, что связь основана только на `user_id`
    user = db.relationship('User', backref=db.backref('ads', lazy=True), foreign_keys=[user_id])    
# commit 5
# class Ad(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('ads', lazy=True))

#     def __repr__(self):
#         return f"<Ad {self.title}>"



#commit 2-4: Features registration, login, get, update, delete user
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False, unique=True)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     password = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return f"<User {self.username}>"


# commit 1: Flask project structure and home page route added