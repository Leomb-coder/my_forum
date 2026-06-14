import os
from functools import wraps

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash

from controllers.user_controller import create_user, delete_user, login_user, get_user_by_id, get_all_users, \
    change_profile_picture

from controllers.forum_controller import create_forum, get_forum_by_slug

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        return func(*args, **kwargs)

    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user = get_user_by_id(session['user_id'])

        if user['role'] != 'admin':
            return {
                'success' : False,
                'message' : 'Forbidden (You shall not pass)'
            }, 403

        return func(*args, **kwargs)

    return wrapper

# Frontend

@app.route('/')
@login_required
def home():
    general_forum = get_forum_by_slug('general')

    return render_template(
        'index.html',
        user=get_user_by_id(session['user_id']),
        general_forum=general_forum
    )

@app.route('/forum/<string:slug>')
def forum(slug):
    current_forum = get_forum_by_slug(slug)

    if current_forum is None:
        return {
            'success' : False,
            'message' : 'Forum not found'
        }, 404

    return render_template('forum.html', forum=current_forum)

@app.route('/profile')
@login_required
def user_profile():
    user_info = get_user_by_id(session['user_id'])
    return render_template('user_profile.html', user=user_info)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
@admin_required
def admin_panel():
    user = get_user_by_id(session['user_id'])
    return render_template('admin/admin_panel.html', user=user)

@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin/admin_users.html', users=get_all_users())

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
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

@app.route('/api/change_user_picture', methods=['PUT'])
def change_user_picture():
    data = request.get_json()
    user_id = session['user_id']
    url = data.get('pfp_url')
    try:
        if request.method == 'PUT':
            user = change_profile_picture(user_id, url)

            if user is None:
                return {
                    'success' : False,
                    'message' : 'User not found'
                }, 404

            return {
                'success' : True,
                'message' : 'Changed profile picture'
            }, 200

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

# Admin Endpoints

@app.route('/api/admin/create_forum', methods=['POST'])
@admin_required
def create_forum_route():
    try:
        if request.method == 'POST':
            data = request.get_json()
            name = data.get('forum-name')
            slug = data.get('forum-slug')
            description = data.get('forum-description')
            icon_url = data.get('forum-icon')
            created_by = session['user_id']

            if not name or not slug or not description or not created_by:
                return {
                    'success' : False,
                    'message' : 'Missing required fields'
                }, 400

            forum_created = create_forum(name, slug, description, icon_url, created_by)

            if forum_created is None:
                return {
                    'success' : False,
                    'message' : 'Forum not found'
                }, 404

            return {
                'success' : True,
                'message' : 'Forum created',
                'data' : forum_created
            }, 201

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

@app.route('/api/admin/delete_user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user_route(user_id):
    try:
        if request.method == 'DELETE':
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