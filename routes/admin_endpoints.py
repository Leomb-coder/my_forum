from flask import Blueprint, request, session
from decorators import admin_required

from controllers.user_controller import delete_user, ban_user, unban_user
from controllers.forum_controller import create_forum

admin_bp = Blueprint('admin_routes', __name__)

# Admin Endpoints

@admin_bp.route('/create_forum', methods=['POST'])
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

@admin_bp.route('/ban_user', methods=['PUT'])
@admin_required
def ban_user_route():
    try:
        if request.method == 'PUT':
            data = request.get_json()
            username = data.get('ban-username')
            ban_reason = data.get('ban-reason')

            if username is None or ban_reason is None:
                return {
                    'success' : False,
                    'message' : 'Missing required fields'
                }, 401

            banned_user = ban_user(username, ban_reason)

            if banned_user is None:
                return {
                    'success' : False,
                    'message' : 'User not found'
                }, 404

            return {
                'success' : True,
                'Message' : 'User was banned'
            }, 200

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

@admin_bp.route('/unban_user', methods=['PUT'])
@admin_required
def unban_user_route():
    try:
        if request.method == 'PUT':
            data = request.get_json()
            username = data.get('unban-username')

            if username is None:
                return {
                    'success' : False,
                    'message' : 'Missing required fields'
                }, 401

            unbanned_user = unban_user(username)

            if unbanned_user is None:
                return {
                    'success' : False,
                    'message' : 'User not found'
                }, 404

            return {
                'success' : True,
                'Message' : 'User was unbanned'
            }, 200

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500

@admin_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
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