from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()  # Only define db once
# After initializing SQLAlchemy


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)  # Adjust if longer paths are needed
    buy_price = db.Column(db.Float, nullable=False)
    time_used = db.Column(db.Integer, nullable=False)  # Store time in months or days
    selling_price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Consider restricting it to 1-5 via validation
    contact_info = db.Column(db.String(100), nullable=False)  # Could consider increasing to store more data

    def __repr__(self):
        return f'<Product {self.id}>'

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Assuming a User model exists
    monthly_budget = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Store as 'YYYY-MM'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Spending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # Add this line
    category = db.relationship('Category', backref='spendings')  # This creates a relationship

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)    
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
