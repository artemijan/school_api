from flask import Blueprint, request
import common.db as db
from security.decorators import is_authorized
from common.utils import jsonify
from models.Subject import Teacher, Subject
import sqlalchemy

teachers = Blueprint('teachers', __name__)


@teachers.route('/api/teachers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@is_authorized
def get_teacher(id):
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


@teachers.route('/api/subjects/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@is_authorized
def get_subjects(id):
    subject = Subject.query.get(id)
    if not subject:
        jsonify({"message": "Subject not found"}), 404
    if request.method == 'GET':
        # teacher.subjects = teacher.subjects
        return jsonify(subject)
    elif request.method == 'PUT':
        subject.deserialize(request.json)
        try:
            db.session.commit()
            return jsonify(subject), 200
        except sqlalchemy.exc.IntegrityError, exc:
            reason = exc.message
            db.session.rollback()
            return jsonify({"message": reason}), 400


@teachers.route('/api/subjects/', methods=['GET'])
@is_authorized
def subject_list():
    return jsonify(Subject.query.all())


@teachers.route('/api/teachers/', methods=['GET'])
@is_authorized
def teacher_list():
    return jsonify(Teacher.query.all())
