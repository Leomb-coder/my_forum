from flask import Blueprint, request, session
from controllers.user_controller import change_profile_picture, insert_user_about_me

user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/change_user_picture', methods=['PUT'])
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

@user_bp.route('/change_about_me', methods=['PUT'])
def change_about_me():
    data = request.get_json()
    user_id = session['user_id']
    content = data.get('content')
    try:
        if request.method == 'PUT':
            user = insert_user_about_me(user_id, content)

            if user is None:
                return {
                    'success': False,
                    'message': 'User not found'
                }, 404

            return {
                'success': True,
                'message': 'Changed user about me section'
            }, 200

    except Exception as e:
        print(e)

        return {
            'success' : False,
            'message' : 'Internal server error'
        }, 500