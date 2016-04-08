from flask import Blueprint, abort, request
import common.db as db
from common.utils import get_json_key
from common.utils import jsonify
from models.User import User
from security.decorators import is_authorized
import sqlalchemy

users = Blueprint('users', __name__)


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
            serialized = jsonify(user)
            db.session.commit()
            return serialized, 200
        except sqlalchemy.exc.IntegrityError, exc:
            reason = exc.message
            db.session.rollback()
            return jsonify({"message": reason}), 400


@users.route('/api/users/', methods=['GET'])
@is_authorized
def user_list():
    return jsonify(User.query.all()), 200
