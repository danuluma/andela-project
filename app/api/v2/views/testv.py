import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.models.validate import Validate


# print(Validate().validate_email("e@dan.com"))
# print(Validate().validate_pass("wfduvbfehT6"))
# print(Validate().validate_phone("54377774346"))
# print(Validate().validate_username("5434346"))
print(Validate().validate_name("masd"))