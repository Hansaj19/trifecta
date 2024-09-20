from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime  # Import datetime for unique filenames
from .models import db, Product  # Import your database model and db instance

carpools = []  # In-memory list to store carpool information

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/features')
def features():
    return render_template('features.html')

@views.route('/marketplace', methods=['GET'])
def marketplace():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('marketplace.html', products=products)

@views.route('/carpool', methods=['GET', 'POST'])
def carpool():
    if request.method == 'POST':
        # Handle adding a new carpool
        destination = request.form['destination']
        date_time = request.form['date_time']
        contact_info = request.form['contact_info']
        vehicle_type = request.form['vehicle_type']
        price = request.form['price']
        total_members_needed = request.form['total_members_needed']
        
        # Create a dictionary to store carpool information
        carpool_info = {
            'destination': destination,
            'date_time': date_time,
            'contact_info': contact_info,
            'vehicle_type': vehicle_type,
            'price': price,
            'total_members_needed': total_members_needed
        }
        
        carpools.append(carpool_info)  # Append to the in-memory list
        flash('Carpool added successfully!', 'success')  # Flash message for success
        return redirect(url_for('views.carpool'))  # Redirect to the carpool view

    return render_template('carpool.html', carpools=carpools)  # Render with the current carpools

@views.route('/education')
def education():
    return render_template('education.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')

@views.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        image = request.files.get('image')
        buy_price = request.form.get('buy_price')
        time_used = request.form.get('time_used')
        selling_price = request.form.get('selling_price')
        rating = request.form.get('rating')
        contact_info = request.form.get('contact_info')

        # Validate required fields
        if not all([image, buy_price, time_used, selling_price, rating, contact_info]):
            flash('All fields are required!', 'danger')
            return render_template('add_product.html')  # Render the template again

        # Ensure the uploads directory exists
        uploads_dir = os.path.join('static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        # Save the image file
        if image:
            try:
                filename = secure_filename(image.filename)
                unique_filename = f"{datetime.utcnow().timestamp()}_{filename}"
                image.save(os.path.join(uploads_dir, unique_filename))

                product = Product(
                    image=unique_filename,
                    buy_price=float(buy_price),
                    time_used=int(time_used),
                    selling_price=float(selling_price),
                    rating=float(rating),
                    contact_info=contact_info
                )
                db.session.add(product)
                db.session.commit()

                flash('Product added successfully!', 'success')
                return redirect(url_for('views.marketplace'))

            except Exception as e:
                flash(f'An error occurred while saving the product: {str(e)}', 'danger')
                return render_template('add_product.html')  # Render on error

    return render_template('add_product.html')

@views.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)  # Get the product or return 404 if not found
    db.session.delete(product)  # Delete the product from the session
    db.session.commit()  # Commit the transaction
    flash('Product removed successfully!', 'success')
    return redirect(url_for('views.marketplace'))
