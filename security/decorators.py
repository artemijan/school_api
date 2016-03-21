from flask import request
from common.utils import jsonify
from models.User import User


def is_authorized(fn):
    def wrapped_fn(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({"message": "Authorization required"}), 403
        user = User.verify_auth_token(token)
        if user:
            return fn(args, kwargs)
        else:
            return jsonify({"message": "Session token is invalid"}), 403
    wrapped_fn.__name__ = fn.__name__
    return wrapped_fn
