from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from app.api.v2.db import Db
# from instance.config import app_config
from app.api.v2.models.modeluser import UserModel
import os

mee = []
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    from app import api_bp, api_bp2
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)
    # Db().drops()
    Db().creates()
    app.register_blueprint(api_bp, url_prefix='/dann/api/v1')
    app.register_blueprint(api_bp2, url_prefix='/dann/api/v2')

    # print(app.config.get("DB_URI"))
    # UserModel().add_admin_user()
    return app

# application = create_app("testing")


if __name__ == "__main__":
    # config_name = "testing"
    config_name = os.getenv('APP_SETTINGS')
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
