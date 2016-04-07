import os
from flask.ext.cors import CORS
from flask import Flask, Blueprint
import common.db as db
import pkgutil
import routes
from common.app_config import Config

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = getattr(Config, 'SECRET_KEY', '!@#$%^*DFHF!@$$())FHF!@#$@#%$$%')
CORS(app, recorces={r"/*": {"origins": ["localhost:9002", "sumragen.github.io"]}})
"""
Auto registration all routes through Blueprints
"""
package_path = os.path.dirname(routes.__file__)
for name in pkgutil.iter_modules([package_path]):
    moduleName = name[1]
    module = __import__('routes.' + moduleName)
    blue_print = getattr(getattr(module, moduleName), moduleName)
    if isinstance(blue_print, list):
        for blue_print_item in blue_print:
            if isinstance(blue_print_item, Blueprint):
                app.register_blueprint(blue_print_item)
    elif isinstance(blue_print, Blueprint):
        app.register_blueprint(blue_print)

if __name__ == '__main__':
    db.init_db()
    # if not os.path.exists('db.sqlite'):
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    host = str(os.environ.get('HOST', 'localhost'))
    app.run(host=host, port=port)
