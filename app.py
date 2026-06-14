import os
from decorators import login_required, admin_required

from flask import Flask, render_template, session, request

from controllers.user_controller import get_user_by_id, get_all_users
from controllers.forum_controller import get_forum_by_slug, get_all_forums
from controllers.thread_controller import create_thread, create_slug

from routes import auth_bp, user_bp, admin_bp

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth/')
app.register_blueprint(user_bp, url_prefix='/api/user/')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Template Routes
@app.route('/')
@login_required
def home():
    general_forum = get_forum_by_slug('general')

    return render_template(
        'index.html',
        user=get_user_by_id(session['user_id']),
        general_forum=general_forum
    )

@app.route('/forums')
@login_required
def forums():
    all_forums = get_all_forums()
    return render_template('forums.html', forums=all_forums)

@app.route('/forum/<string:slug>/create_thread', methods=['POST'])
def create_thread_route(slug):
    try:
        current_forum_id = get_forum_by_slug(slug)['id']
        data = request.get_json()
        title = data.get('thread-title')
        thread_slug = create_slug(title)
        content = data.get('thread-content')

        created_thread = create_thread(current_forum_id, session['user_id'], title, thread_slug, content)

        if created_thread is None:
            return {
                'success' : False,
                'message' : 'Thread was not found'
            }, 404

        return {
            'success' : True,
            'message' : 'Thread created',
            'data' : created_thread
        }, 201

    except Exception as e:
        print(e)

        return {
            'success': False,
            'message': 'Internal server error'
        }, 500

@app.route('/forum/<string:slug>')
@login_required
def forum(slug):
    current_forum = get_forum_by_slug(slug)
    user = get_user_by_id(session['user_id'])

    if current_forum is None:
        return {
            'success' : False,
            'message' : 'Forum not found'
        }, 404

    return render_template('forum.html', user=user, get_user=get_user_by_id, forum=current_forum)

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

if __name__ == '__main__':
    app.run(debug=True)