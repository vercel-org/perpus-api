from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid,os
from datetime import datetime
from app.models.books import Books

class Carts(db.Model):
    __tablename__ = 'tbl_carts'
    id_cart = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    user = db.relationship('Users', backref='tbl_carts', uselist=False)
    id_user = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_users.id_user'))
    book = db.relationship('Books', backref='tbl_carts', uselist=False)
    id_book = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_books.id_book'))
    
def select_cart(id):
    query = Carts.query.filter_by(id_cart=id).first()
    return query

def select_carts(id):
    query = Carts.query.filter_by(id_user=id).all()
    return query

def cart_all(page_name,page_value,per_page_name,per_page_value,id):
        query = (
            Carts.query
            .filter_by(id_user = id)
            .join(Books, Carts.id_book == Books.id_book)
            .order_by(Books.created_at.desc())
            .paginate(**{page_name : page_value, per_page_name : per_page_value})
        ) 
        return query