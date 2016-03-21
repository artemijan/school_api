from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app_config import Config

"""
Configs
"""
SQLALCHEMY_DATABASE_URI = getattr(Config, 'SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = getattr(Config, 'SQLALCHEMY_COMMIT_ON_TEARDOWN', True)


engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models


def create_all():
    Base.metadata.create_all(bind=engine)
