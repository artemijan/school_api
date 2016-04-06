from flask import Blueprint, abort, request
import common.db as db
from common.utils import jsonify
from models.Subject import Teacher
import sqlalchemy

teachers = Blueprint('teachers', __name__)


@teachers.route('/api/teachers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(id):
    teacher = Teacher.query.get(id)
    if not teacher:
        jsonify({"message": "User not found"}), 404
    if request.method == 'GET':
        # teacher.subjects = teacher.subjects
        return jsonify(teacher)
    elif request.method == 'PUT':
        teacher.deserialize(request.json)
        try:
            db.session.commit()
            return jsonify(teacher, expand=('subjects',)), 200
        except sqlalchemy.exc.IntegrityError, exc:
            reason = exc.message
            db.session.rollback()
            return jsonify({"message": reason}), 400


@teachers.route('/api/teachers/', methods=['GET'])
def user_list():
    return jsonify(Teacher.query.all())
