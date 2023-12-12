from flask import Flask
from flask_mysqldb import MySQL
from .database.db_mysql import db
from flask_cors import CORS
# Routes
from .routes import AuthRoutes, OperativeSystemRoutes, SecurityPoliciesRoutes, RulesRoutes, AssetsRoutes, GroupsRoutes, DiagnosisRoutes

app = Flask(__name__)
CORS(app)
db.init_app(app)

def init_app(config):
    # Configuration
    app.config.from_object(config)

    app.register_blueprint(OperativeSystemRoutes.main, url_prefix='/operative_system')
    app.register_blueprint(SecurityPoliciesRoutes.main, url_prefix='/security_policies')
    app.register_blueprint(RulesRoutes.main, url_prefix='/rules')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(AssetsRoutes.main, url_prefix='/assets')
    app.register_blueprint(GroupsRoutes.main, url_prefix='/groups')
    app.register_blueprint(DiagnosisRoutes.main, url_prefix='/diagnosis')


    return app