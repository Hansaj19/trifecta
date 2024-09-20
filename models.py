from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # Only define db once

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


