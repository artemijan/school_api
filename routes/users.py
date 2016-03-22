from flask import Blueprint, abort, request
import common.db as db
from common.utils import get_json_key
from common.utils import jsonify
from models.User import User
from security.decorators import is_authorized

users = Blueprint('users', __name__)


@users.route('/api/users', methods=['POST'])
@is_authorized
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "User already exist"}), 400
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({'username': user.username}), 201
    except:
        db.session.rollback()
        return jsonify({"message": "Wrong user data"}), 400


@users.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@is_authorized
def get_user(id):
    user = User.query.get(id)
    if not user:
        jsonify({"message": "User not found"}), 404
    if request.method == 'GET':
        return jsonify(user)
    elif request.method == 'PUT':
        user.name = get_json_key(request.json, 'name')
        user.username = get_json_key(request.json, 'username')
        user.email = get_json_key(request.json, 'email')
        try:
            db.session.commit()
            return jsonify(user)
        except:
            db.session.rollback()
            return jsonify({"message": "Update user failure"}), 400


@users.route('/api/users/', methods=['GET'])
@is_authorized
def user_list():
    return jsonify(User.query.all())
