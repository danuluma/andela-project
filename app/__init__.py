# weka shit yote hapa
from flask import Blueprint
from flask_restful import Api



# local imports to be last eg
# from instance.config import app_config
from app.api.v1.views import Home, Orders, MyOrder
from app.api.v1.auth import Reg, Login, Test, Refresh


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


# Route
api.add_resource(Home, '/')
api.add_resource(Orders, '/orders')
api.add_resource(MyOrder, '/orders/<int:order_id>')
api.add_resource(Reg, '/reg')
api.add_resource(Login, '/login')
api.add_resource(Refresh, '/refresh')
api.add_resource(Test, '/test')
# api.add_resource(Foods, '/foods')
# api.add_resource(ThisFood, '/foods/<int:food_id>')
