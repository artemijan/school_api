from flask import Blueprint, request
from common.utils import jsonify
from models.User import User
from common.app_config import Config

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
        if user and user.verify_password(password):
            token = user.generate_auth_token(SESSION_TOKEN_DURATION)
            return jsonify({"token": token.decode('ascii'), "duration": SESSION_TOKEN_DURATION})
        else:
            return jsonify({"message": "Login failed"}), 401
