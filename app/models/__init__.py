from app import db
from sqlalchemy import select
from app.models.roles import Roles
from app.models.authors import Authors
from app.models.publishers import Publishers
from app.models.categories import Categories
from app.models.bookshelves import Bookshelves
from app.models.books import Books

import os

def select_all(model):
    query = model.query.all()
    return query

def select_by_id(model,id):
    query = model.query.get(id)
    return query
 
def select_users_role(role):
    query = select(Roles.id_role).where(Roles.role == os.getenv(role))
    result = db.session.execute(query)
    id_role = result.scalar()
    return id_role

def filter_by(model,field_name, field_value):
    query = model.query.filter_by(**{field_name : field_value}).first()
    return query

def order_by(model, page_name, page_value, per_page_name, per_page_value):
    query = model.query.order_by(model.created_at.desc()).paginate(**{page_name : page_value, per_page_name : per_page_value})
    return query
  
def meta_data(model,page,per_page):
    data = model.query.count()
    total = (data - 1 + per_page)//per_page
    if page <= 0 or page > total:
        return data
    


