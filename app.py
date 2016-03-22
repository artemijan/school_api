import os
from flask import Flask
import common.db as db
from routes.auth import auth
from routes.users import users
from common.app_config import Config
# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = getattr(Config, 'SECRET_KEY', '!@#$%^*DFHF!@$$())FHF!@#$@#%$$%')

app.register_blueprint(auth)
app.register_blueprint(users)

if __name__ == '__main__':
    db.init_db()
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True, port=9888, host='localhost')
