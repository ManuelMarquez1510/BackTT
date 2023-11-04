from flask import Flask
from flask_mysqldb import MySQL
from .database.db_mysql import db
# Routes
from .routes import AuthRoutes, OperativeSystemRoutes

app = Flask(__name__)
db.init_app(app)

def init_app(config):
    # Configuration
    app.config.from_object(config)

    app.register_blueprint(OperativeSystemRoutes.main, url_prefix='/operative_sytem')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')


    return app