from flask import Blueprint, request
from common.utils import jsonify
from models.User import User
from common.app_config import Config
import common.db as db
import sqlalchemy

SESSION_TOKEN_DURATION = getattr(Config, 'SESSION_TOKEN_DURATION', 1200)

auth = Blueprint('auth', __name__)


@auth.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.verify_auth_token(username)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username).first()
        if user:
            if user.verify_password(password):
                token = user.generate_auth_token(SESSION_TOKEN_DURATION)
                return jsonify({"token": token.decode('ascii'), "duration": SESSION_TOKEN_DURATION})
            else:
                return jsonify({"message": "password is incorrect"}), 401
        else:
            return jsonify({"message": "Can not find this username"}), 401


@auth.route('/api/register', methods=['POST'])
def register():
    user = User(json=request.json)
    if 'password' not in request.json:
        return jsonify({"message": "Password is required"})
    password = request.json['password']
    user.hash_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError, exc:
        reason = exc.message
        db.session.rollback()
        return jsonify({"message": reason}), 400
    return jsonify(user)
