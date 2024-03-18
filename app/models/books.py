import os
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.authors import Authors
from app.models.publishers import Publishers
from app.models.categories import Categories
from app.models.bookshelves import Bookshelves
class Books(db.Model):
    __tablename__ = 'tbl_books'
    id_book = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(250), nullable = False)
    stock = db.Column(db.Integer)
    author = db.relationship('Authors', backref='tbl_books', uselist = False)
    id_author = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_authors.id_author'))
    publisher = db.relationship('Publishers', backref='tbl_books', uselist = False)
    id_publisher = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_publishers.id_publisher'))
    category = db.relationship('Categories', backref='tbl_books', uselist = False)
    id_category = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_categories.id_category'))
    bookshelf = db.relationship('Bookshelves', backref='tbl_books', uselist = False)
    id_bookshelf = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_bookshelves.id_bookshelf'))
    picture = db.Column(db.String(200), default = os.getenv('DEFAULT_BOOK_PICTURE'))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    
def books_all(page_name,page_value,per_page_name,per_page_value):
        query = (
            Books.query
            .join(Authors, Books.id_author == Authors.id_author)
            .join(Categories, Books.id_category == Categories.id_category)
            .join(Publishers, Books.id_publisher == Publishers.id_publisher)
            .join(Bookshelves, Books.id_bookshelf == Bookshelves.id_bookshelf)
            .order_by(Books.created_at.desc())
            .paginate(**{page_name : page_value, per_page_name : per_page_value})
        ) 
        return query
    
def select_book_id(id):
    query = (
        Books.query
        .join(Authors, Books.id_author == Authors.id_author)
        .join(Categories, Books.id_category == Categories.id_category)
        .join(Publishers, Books.id_publisher == Publishers.id_publisher)
        .join(Bookshelves, Books.id_bookshelf == Bookshelves.id_bookshelf)
        .filter(Books.id_book == id)
        .first()
    )
    return query
 
 