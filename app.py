import os

from decorators import login_required, admin_required
from flask import Flask, render_template, session

from controllers.user_controller import get_user_by_id, get_all_users
from controllers.forum_controller import get_forum_by_slug, get_all_forums, get_forum_by_id
from controllers.thread_controller import get_forum_threads_count, get_user_threads_count, get_threads_by_user_id, \
    get_all_threads

from routes import auth_bp, user_bp, admin_bp, forum_bp

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth/')
app.register_blueprint(user_bp, url_prefix='/api/user/')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(forum_bp, url_prefix='/forum')

# Template Routes
@app.route('/')
@login_required
def home():
    general_discussion_forum = get_forum_by_slug('general-discussion')

    gen_forums = [
        general_discussion_forum
    ]

    return render_template(
        'index.html',
        user=get_user_by_id(session['user_id']),
        forums=gen_forums,
        threads_count=get_forum_threads_count
    )

@app.route('/latest')
def latest():
    threads = get_all_threads()
    return render_template(
        'latest.html',
        user=get_user_by_id(session['user_id']),
        threads=threads,
        get_forum_by_id=get_forum_by_id
    )

@app.route('/members')
def members():
    users = get_all_users()
    return render_template('members.html', user=get_user_by_id(session['user_id']), members=users)

@app.route('/members/<int:member_id>')
def member_profile(member_id):
    member = get_user_by_id(member_id)
    user_threads = get_threads_by_user_id(member['id'])
    user_threads_count = get_user_threads_count(member['id'])
    return render_template(
        'member_profile.html',
        user=get_user_by_id(session['user_id']),
        member=member,
        threads_count=user_threads_count,
        user_threads=user_threads,
        get_forum_by_id=get_forum_by_id
    )

@app.route('/forums')
@login_required
def forums():
    all_forums = get_all_forums()
    return render_template('forums.html',user=get_user_by_id(session['user_id']) ,forums=all_forums, threads_count=get_forum_threads_count)

@app.route('/profile')
@login_required
def user_profile():
    user_info = get_user_by_id(session['user_id'])
    return render_template(
        'user_profile.html',
                        user=user_info,
                        threads_count=get_user_threads_count
                        )

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