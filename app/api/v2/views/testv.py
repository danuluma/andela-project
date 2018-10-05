import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.validate import Validate


print(Validate().validate_email("@dan.com"))
print(Validate().validate_password("wertyn2."))
print(Validate().validate_phone("5437777434i6"))
print(Validate().validate_username(""))
