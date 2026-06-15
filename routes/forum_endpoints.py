from flask import Blueprint, request, session, render_template
from controllers.forum_controller import get_forum_by_slug
from controllers.thread_controller import create_thread, create_slug
from decorators import login_required

from controllers.user_controller import get_user_by_id
from controllers.thread_controller import get_threads_by_forum_id, get_thread_by_id

forum_bp = Blueprint('forum_routes', __name__)

# Open Forum by Slug
@forum_bp.route('/<string:slug>')
@login_required
def forum(slug):
    current_forum = get_forum_by_slug(slug)
    user = get_user_by_id(session['user_id'])
    threads = get_threads_by_forum_id(current_forum['id'])

    if current_forum is None:
        return {
            'success' : False,
            'message' : 'Forum not found'
        }, 404

    return render_template('forum.html',
                           user=user,
                           get_user=get_user_by_id,
                           forum=current_forum,
                           threads=threads
                           )

# Open Thread in /id/slug
@forum_bp.route('/<string:forum_slug>/<int:thread_id>/<string:thread_slug>')
def thread(forum_slug, thread_id, thread_slug):
    try:
        current_thread = get_thread_by_id(thread_id)

        return render_template('thread.html', thread=current_thread, get_user=get_user_by_id)

    except Exception as e:
        print(e)

        return {
            'success': False,
            'message': 'Internal server error'
        }, 500

# Create Thread by Forum Slug
@forum_bp.route('/<string:slug>/create_thread', methods=['POST'])
def create_thread_route(slug):
    try:
        current_forum = get_forum_by_slug(slug)
        current_forum_id = current_forum['id']
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