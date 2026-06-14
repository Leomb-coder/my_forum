from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash
from controllers.user_controller import create_user, login_user

auth_bp = Blueprint('auth_routes', __name__)

@auth_bp.route('/register', methods=['POST'])
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

@auth_bp.route('/login', methods=['POST'])
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


@auth_bp.route('/logout', methods=['POST'])
def logout_user_route():
    try:
        if request.method == 'POST':
            session.clear()

            return {
                'success' : True,
                'message' : 'User was logged out'
            }, 204

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500