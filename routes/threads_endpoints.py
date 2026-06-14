from flask import Blueprint, request, session
from controllers.forum_controller import get_forum_by_slug
from controllers.thread_controller import create_thread, create_slug

threads_bp = Blueprint('threads_routes', __name__)

@threads_bp.route('/<string:slug>/create_thread', methods=['POST'])
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