from sqlalchemy import Column, Integer, String
from common.db import Base
from models.Serializable import Serializable
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from common.app_config import Config


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

    def generate_auth_token(self, expiration=600):
        if not hasattr(Config, 'SECRET_KEY'):
            Config['SECRET_KEY'] = '!@$#%^^cg#$^^**(#$dhf!@#$@$#%#$'
        s = Serializer(getattr(Config, 'SECRET_KEY'), expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(getattr(Config, 'SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
