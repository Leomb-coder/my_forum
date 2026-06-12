import os

from flask import Flask, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from controllers.user_controller import create_user, delete_user, login_user

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Frontend

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

# API Endpoints

@app.route('/api/register', methods=['POST'])
def register_user_route():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return {
                    'success' : False,
                    'message' : 'Missing required fields'
                }, 400

            hashed_password = generate_password_hash(password)
            user = create_user(username, email, hashed_password)

            if user is None:
                return {
                    'success': False,
                    'message': 'User not found'
                }, 404

            return {
                'success' : True,
                'message' : 'User created',
                'data' : user
            }, 201

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

@app.route('/api/login', methods=['POST'])
def user_login_route():
    try:
        if request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {
                    'success' : False,
                    'message' : 'Missing credentials'
                }, 401

            user = login_user(email, password)

            if user is None:
                return {
                    'success' : False,
                    'message' : 'Invalid email or password'
                }, 401

            session['user_id'] = user['id']

            return {
                'success' : True,
                'message' : 'User was logged in',
                'data' : user
            }, 200

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500


@app.route('/api/logout', methods=['POST'])
def logout_user_route():
    try:
        if request.method == 'POST':
            session.clear()

            return {
                'success' : True,
                'message' : 'User was logged out'
            }, 204 # No content

    except Exception as e:
        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

@app.route('/api/delete_user/<int:id>', methods=['POST'])
def delete_user_route(user_id):
    try:
        if request.method == 'POST':
            user = delete_user(user_id)

            if user is None:
                return {
                    'success' : False,
                    'message' : 'User not found'
                }, 404

            return {
                'success' : True,
                'message' : 'User removed',
                'data' : user
            }, 200

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

if __name__ == '__main__':
    app.run(debug=True)