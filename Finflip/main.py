from website import create_app, db


app = create_app()


# Create tables if they don't exist
with app.app_context():
    db.create_all()  # This will create tables based on your models

if __name__ == '__main__':
    app.run(debug=True, port=7000)
