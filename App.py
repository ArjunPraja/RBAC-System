from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

# Initialize Flask app
app = Flask(__name__)

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['RBAC']  # Database name
collection = db['users']  # Collection name

# Decorator to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = collection.find_one({"email": data['email']})
            if not current_user:
                raise Exception('User not found')
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Check if the email already exists
        if collection.find_one({"email": email}):
            return jsonify({"message": "Email already exists!"}), 400

        # Create user document
        user = {
            "name": name,
            "email": email,
            "role": role,
            "password": hashed_password
        }

        # Insert into MongoDB
        collection.insert_one(user)

        # Redirect to login page
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user in MongoDB
        user = collection.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            # Generate JWT token
            token = jwt.encode({
                'email': user['email'],
                'role': user['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            # Set token in cookies
            response = redirect(url_for('dashboard'))
            response.set_cookie('token', token)
            return response

        return jsonify({"message": "Invalid credentials!"}), 401

    return render_template('login.html')

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    # Redirect based on role
    if current_user['role'] == 'employee':
        return render_template('employee.html', user=current_user)
    elif current_user['role'] == 'manager':
        return render_template('manager.html', user=current_user)
    else:
        return jsonify({"message": "Unauthorized role!"}), 403

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('token')
    return response

if __name__ == '__main__':
    app.run(debug=True)