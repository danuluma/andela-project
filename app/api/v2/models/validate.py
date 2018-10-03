import re

class Validate(object):
  """docstring for Validate"""
  def __init__(self):
    pass

  def validate_email(self, email):
    return True if re.match("^\w+(\.|\w)*@\w+(\.\w)*(\.\w{2,4})$", email) else False

  def validate_password(self, passw):
    return True if re.match("", passw) else False

  def validate_phone(self, phone):
    return True if re.match("^[0-9]{10,12}$", phone) else False

  def validate_username(self, username):
    return True if re.match("^[\.|[0-9]|\w]{5,10}$", username) else False

  def validate_name(self, name):
    return True if re.match("^([a-z]|[A-Z]){3,20}$", name) else False
