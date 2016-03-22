import os
from flask import Flask, abort, request
import common.db as db
from common.utils import get_json_key
from common.utils import jsonify
from models.User import User
from common.app_config import Config
from security.decorators import is_authorized

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = getattr(Config, 'SECRET_KEY', '!@#$%^*DFHF!@$$())FHF!@#$@#%$$%')
SESSION_TOKEN_DURATION = getattr(Config, 'SESSION_TOKEN_DURATION', 1200)


@app.route('/api/users', methods=['POST'])
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


@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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


@app.route('/api/users/', methods=['GET'])
def user_list():
    return jsonify(User.query.all())


@app.route('/api/login', methods=['POST'])
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


if __name__ == '__main__':
    db.init_db()
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True, port=9888, host='localhost')
