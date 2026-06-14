from functools import wraps
from flask import session, render_template, redirect, url_for

from controllers.user_controller import get_user_by_id

# Wrappers
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('login'))

        user = get_user_by_id(user_id)

        if user['banned']:
            session.clear()

            return render_template('banned.html', ban_reason=user['ban_reason'])

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