from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import os

def create_app():
    app = Flask(__name__)
    # app.config.from_object(configfile)
    from app import api_bp
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    app.register_blueprint(api_bp, url_prefix='/dann/api/v1')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
