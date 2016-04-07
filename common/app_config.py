class Config(object):
    SECRET_KEY = 'the quick brown fox jumps over the lazy dog'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SESSION_TOKEN_DURATION = 1200
    SQLALCHEMY_ECHO = False
