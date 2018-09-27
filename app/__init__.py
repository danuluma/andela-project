from flask import Blueprint
from flask_restful import Api



# local imports
# from instance.config import app_config
from app.api.v1.views import Home, Orders, MyOrder
from app.api.v1.auth import Reg, Login, Refresh
from app.api.v2.menu_view import Menu, TestMe


api_bp = Blueprint('api', __name__)
api_bp2 = Blueprint('api2', __name__)
api = Api(api_bp)
api2 = Api(api_bp2)


# Routes
api.add_resource(Home, '/home')
api.add_resource(Orders, '/orders')
api.add_resource(MyOrder, '/order/<int:order_id>')
api.add_resource(Reg, '/reg')
api.add_resource(Login, '/login')
api.add_resource(Refresh, '/refresh')
api2.add_resource(Menu, '/menu')
api2.add_resource(TestMe, '/hey')
