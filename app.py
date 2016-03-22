import os
from flask import Flask
import common.db as db
import pkgutil
import routes
from common.app_config import Config

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = getattr(Config, 'SECRET_KEY', '!@#$%^*DFHF!@$$())FHF!@#$@#%$$%')

"""
Auto registration all routes through Blueprints
"""
package_path = os.path.dirname(routes.__file__)
for name in pkgutil.iter_modules([package_path]):
    moduleName = name[1]
    module = __import__('routes.' + moduleName)
    app.register_blueprint(getattr(getattr(module, moduleName), moduleName))

if __name__ == '__main__':
    db.init_db()
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True, port=9888, host='localhost')
