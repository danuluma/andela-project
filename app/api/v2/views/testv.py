import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.validate import Validate


print(Validate().validate_email("j@dan.com"))
# print(Validate().validate_password("wertyn2."))
# print(Validate().validate_phone("54377774346"))
# print(Validate().validate_username("5434346"))
# if not Validate().validate_name('u'):
# print("bdh")