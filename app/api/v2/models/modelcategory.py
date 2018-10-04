import os, sys
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../../')

from app.api.v2.db import Db


class CategoryModel(Db):
  """docstring for Menu"""
  def __init__(self):
    pass

  def get_all_categories(self):
    return Db().get_query('categories')

  def get_single_category(self, category_id):
    return [row for row in Db().get_query('categories') if row[0]==category_id]

  def add_new_category(self, category_details):
    Db().post_query("""
    INSERT INTO categories (name, description)
    VALUES (%s,%s);
    """, category_details)

  def update_category_details(self, category_id, data):
    updatesql = """UPDATE categories SET name = %s, description = %s WHERE id = {}""".format(category_id)
    return Db().put_query(updatesql, data)

  def delete_category(self, category_id):
    Db().delete_query("""DELETE FROM categories WHERE id = {}""".format(category_id))
