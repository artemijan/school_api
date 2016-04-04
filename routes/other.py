from flask import Blueprint, request
import common.db as db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import lazyload
from common.utils import jsonify
from models.Subject import Teacher, Subject

other = Blueprint('other', __name__)


@other.route('/api/teachers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_teacher(id):
    user = Teacher.query.get(id)
    if not user:
        jsonify({"message": "User not found"}), 404
    if request.method == 'GET':
        user.subjects = user.subjects
        return jsonify({"user": user}, props=('username', 'email'))
    elif request.method == 'PUT':
        user.deserialize(request.json)
        try:
            db.session.commit()
            return jsonify(user)
        except IntegrityError, exc:
            reason = exc.message
            db.session.rollback()
            return jsonify({"message": reason}), 400


@other.route('/api/teachers/', methods=['GET'])
def user_list():
    return jsonify(db.session.query(Teacher).all(), expand=('subjects', ))
