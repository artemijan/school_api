from sqlalchemy import Column, Integer, String
from common.db import Base
from models.Serializable import Serializable
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired, JSONWebSignatureSerializer, number_types)
from common.app_config import Config


class CustomSerializer(Serializer):
    def loads(self, s, salt=None, return_header=False, renew_session_duration=False):
        payload, header = JSONWebSignatureSerializer.loads(
            self, s, salt, return_header=True)

        if 'exp' not in header:
            raise BadSignature('Missing expiry date', payload=payload)

        if not (isinstance(header['exp'], number_types) and header['exp'] > 0):
            raise BadSignature('expiry date is not an IntDate',
                               payload=payload)

        if header['exp'] < self.now():
            raise SignatureExpired('Signature expired', payload=payload,
                                   date_signed=self.get_issue_date(header))
        elif renew_session_duration:
            header['iat'] = self.now() - self.expires_in
            header['exp'] = self.now()

        if return_header:
            return payload, header
        return payload


SESSION_TOKEN_DURATION = getattr(Config, 'SESSION_TOKEN_DURATION')
serializer = CustomSerializer(getattr(Config, 'SECRET_KEY'), SESSION_TOKEN_DURATION)


class User(Serializable, Base):
    __tablename__ = 'users'
    __plural__ = 'users'
    # is needed for serializable, property wouldn't be in serialized data because it's write only
    __write_only__ = ('password_hash',)
    __exclude__ = ('password',)
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=True)
    first_name = Column(String(50), unique=False, nullable=False)
    last_name = Column(String(50), unique=False, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(64))

    def __repr__(self):
        return '<User %>' % self.name

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        try:
            data = serializer.loads(token, renew_session_duration=True)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
