from flask import Blueprint, request
import common.db as db
from sqlalchemy.exc import IntegrityError
from common.utils import jsonify
from models.Subject import Teacher, Subject

other = Blueprint('other', __name__)


@other.route('/api/teachers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_teacher(id):
    user = Teacher.query.get(id)
    if not user:
        jsonify({"message": "User not found"}), 404
    if request.method == 'GET':
        return jsonify(user)
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
    return jsonify(Teacher.query.all())
