from flask import Blueprint
from flask_restful import Api



# local imports
# from instance.config import app_config
from app.api.v1.views import Home, Orders, MyOrder
from app.api.v1.auth import Reg, Login, Refresh


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


# Routes
api.add_resource(Home, '/home')
api.add_resource(Orders, '/orders')
api.add_resource(MyOrder, '/order/<int:order_id>')
api.add_resource(Reg, '/register')
api.add_resource(Login, '/login')
api.add_resource(Refresh, '/refresh')
