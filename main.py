from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'telvin_maina'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# create database models
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)



@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            flash("All fields must be filled!", 'danger')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("Passwords must match!", 'danger')
            return redirect(url_for('signup'))

        # check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists!", 'danger')
            return redirect(url_for('signup'))
    
        # add new user
        # but first generate hashed_password
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # print debug statement
        print("User added successfully")
        
        flash("User added successfully", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    return render_template('login.heml')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
