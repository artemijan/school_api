from flask import Flask
from utils import jsonify
from db import init_db, db_session
from models import User as UserDao
# init data base


# init flask app
app = Flask(__name__)


@app.route('/')
def index():
    list_all = UserDao.User.query.all()
    if len(list_all) == 0:
        user = UserDao.User(name='artem', email='line@artem.com')
        db_session.add(user)
        db_session.commit()
    return jsonify(list_all, props={"email": None})

if __name__ == '__main__':
    init_db()
    # user = UserDao.User(name='artem2', email='line2@artem.com')
    # db_session.add(user)
    # db_session.commit()
    app.run(debug=False, use_reloader=False, port=9888, host='localhost')
