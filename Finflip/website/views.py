from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime  # Import datetime for unique filenames
from .models import db, Product,Budget,Spending,Category,Expense # Import your database model and db instance
import uuid 


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

import uuid  # Import uuid for unique IDs

# Inside the carpool route where you add a carpool entry
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
        
        # Create a dictionary to store carpool information, including a unique ID
        carpool_info = {
            'id': str(uuid.uuid4()),  # Generate a unique ID for each carpool
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
@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')

tools = Blueprint('tools', __name__)

@views.route('/budget-calculator')
def budget_calculator():
    return render_template('budget_calculator.html')
@views.route('/trackbudget', methods=['POST'])
@login_required
def trackbudget():
    # Get the monthly budget from the form
    monthly_budget = float(request.form.get('monthly_budget'))
    
    # Get expenses from the form and calculate total expenses
    expenses = request.form.get('expenses').split(',')
    total_expenses = 0
    
    # Create and save each expense
    for expense in expenses:
        expense_amount = expense.strip()
        if expense_amount and expense_amount.isdigit():  # Check for valid numeric input
            total_expenses += float(expense_amount)
            # Create an Expense instance (assuming you have an Expense model)
            expense_entry = Expense(user_id=current_user.id, amount=float(expense_amount))
            db.session.add(expense_entry)  # Add to the session

    # Save the monthly budget to the database
    existing_budget = Budget.query.filter_by(user_id=current_user.id).first()
    if existing_budget:
        existing_budget.monthly_budget = monthly_budget
    else:
        existing_budget = Budget(user_id=current_user.id, monthly_budget=monthly_budget)
        db.session.add(existing_budget)  # Add budget if it doesn't exist

    db.session.commit()  # Commit all changes to the database

    flash('Budget and expenses saved successfully!', 'success')
    
    # Render the budget calculator again with the results
    return render_template('budget_calculator.html', budget={"monthly_budget": monthly_budget}, total_expenses=total_expenses)

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
        uploads_dir = os.path.join('website', 'static', 'uploads')  # Update this line
        os.makedirs(uploads_dir, exist_ok=True)

        # Save the image file
        if image:
            try:
                filename = secure_filename(image.filename)
                unique_filename = f"{datetime.utcnow().timestamp()}_{filename}"
                image_path = os.path.join(uploads_dir, unique_filename)
                image.save(image_path)

                # Create and save the product instance
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
@views.route('/delete_carpool/<string:carpool_id>', methods=['POST'])
def delete_carpool(carpool_id):
    global carpools
    carpools = [carpool for carpool in carpools if carpool['id'] != carpool_id]  # Filter out the carpool with the matching ID
    flash('Carpool entry deleted successfully!', 'success')
    return redirect(url_for('views.carpool'))
@views.route('/track_budget', methods=['GET', 'POST'])
@login_required  # Ensure user is logged in
def track_budget():
    if request.method == 'POST':
        monthly_budget = request.form.get('monthly_budget')
        if not monthly_budget:
            flash('Monthly budget is required!', 'danger')
            return redirect(url_for('views.track_budget'))

        user_id = current_user.id  # Use current_user from Flask-Login
        current_month = datetime.utcnow().strftime('%Y-%m')

        # Check if the user has already set a budget for the current month
        existing_budget = Budget.query.filter_by(user_id=user_id, month=current_month).first()
        if existing_budget:
            existing_budget.monthly_budget = float(monthly_budget)
        else:
            budget = Budget(user_id=user_id, monthly_budget=float(monthly_budget), month=current_month)
            db.session.add(budget)

        db.session.commit()
        flash('Monthly budget set successfully!', 'success')
        return redirect(url_for('views.track_budget'))

    return render_template('track_budget.html')
@views.route('/add_spending', methods=['GET', 'POST'])
@login_required
def add_spending():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category_id = request.form.get('category_id')

        print(f"Amount: {amount}, Category ID: {category_id}")  # Debugging line

        if not amount or not category_id:
            flash('Amount and category are required!', 'danger')
            return redirect(url_for('views.add_spending'))

        try:
            amount = float(amount)
        except ValueError:
            flash('Invalid amount format!', 'danger')
            return redirect(url_for('views.add_spending'))

        user_id = current_user.id
        
        # Check category
        category = Category.query.get(category_id)
        if not category:
            flash('Invalid category selected!', 'danger')
            return redirect(url_for('views.add_spending'))

        spending = Spending(user_id=user_id, amount=amount, category_id=category.id, date=datetime.utcnow())
        db.session.add(spending)
        db.session.commit()

        flash('Spending added successfully!', 'success')
        return redirect(url_for('views.add_spending'))

    # If GET request, fetch categories
    categories = Category.query.all()
    transactions_by_category = {}
    total_spending = 0

    for category in categories:
        transactions = Spending.query.filter_by(user_id=current_user.id, category_id=category.id).all()
        transactions_by_category[category.name] = transactions
        total_spending += sum(t.amount for t in transactions)

    current_month = datetime.utcnow().strftime('%Y-%m')
    budget = Budget.query.filter_by(user_id=current_user.id, month=current_month).first()
    budget_exceeded = total_spending > (budget.monthly_budget if budget else 0)

    return render_template('add_spending.html', 
                           transactions_by_category=transactions_by_category, 
                           total_spending=total_spending, 
                           budget=budget, 
                           budget_exceeded=budget_exceeded, 
                           categories=categories)
@views.route('/suggestions')
@login_required  # Ensure user is logged in
def suggestions():
    return render_template('suggestions.html')  # Create a template for financial advice
from flask import render_template

@views.route('/financial-education')
def financial_education():
    return render_template('financial_education.html')
