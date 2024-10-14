from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):     
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(550), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin' or 'user'
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, firstname, lastname, email, role='user'):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = role
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ElectronicProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    model_number = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    def __init__(self, name, description, price, brand, model_number, category, stock=0):
        self.name = name
        self.description = description
        self.price = price
        self.brand = brand
        self.model_number = model_number
        self.category = category
        self.stock = stock
