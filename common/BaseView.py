from flask import Blueprint, request
import common.db as db
from common.utils import jsonify
import sqlalchemy

name = __name__


class BaseView:
    __model_class__ = db.Base
    __always_expand__ = ()

    def __init__(self, *args, **kwargs):
        self.__blue_print__ = Blueprint(self.__model_class__, __name__)
        decorators = kwargs.get('decorators', [])
        for dec in decorators:
            self.post = dec(self.post)
            self.delete = dec(self.delete)
            self.put = dec(self.put)
            self.get = dec(self.get)
            self.get_all = dec(self.get_all)
            self.patch = dec(self.patch)
        methods = kwargs.get('methods', ['POST', 'PUT', 'PATCH', 'GET', 'DELETE'])
        base_url = kwargs.get('base_url', '/' + self.__model_class__.__plural__ + '/')
        for method in methods:
            if not (method == 'POST'):
                self.__blue_print__.route(base_url + '<int:id>', methods=[method])(getattr(self, method.lower()))
        if 'POST' in methods:
            self.__blue_print__.route(base_url, methods=['POST'])(self.post)
        if 'GET' in methods:
            self.__blue_print__.route(base_url, methods=['GET'])(self.get_all)

    def get_view(self):
        """
        :return: Blueprint
        """
        return self.__blue_print__

    def post(self):
        instance = self.__model_class__.from_json(request.json)
        db.session.add(instance)
        try:
            db.session.commit()
            db.session.refresh(instance)
            return jsonify(instance, expand=self.__always_expand__), 201
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            db.session.rollback()
            return jsonify({"message": reason}), 400

    def delete(self, id):
        self.__model_class__.query.filter_by(id=id).delete()
        try:
            db.session.commit()
            return jsonify({"id": id}), 200
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            db.session.rollback()
            return jsonify({"message": reason}), 400

    def put(self, id):
        instance = self.__model_class__.query.get(id)
        instance.deserialize(request.json)
        try:
            db.session.commit()
            return jsonify(instance, expand=self.__always_expand__)
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            db.session.rollback()
            return jsonify({"message": reason}), 400

    def get(self, id):

        instance = self.__model_class__.query.get(id)
        if instance is None:
            return jsonify({"message": self.__model_class__.__name__ + " not found"}), 404
        return jsonify(instance, expand=self.__always_expand__)

    def get_all(self):
        return jsonify(self.__model_class__.query.all())

    def patch(self, id_):
        pass
