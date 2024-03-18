from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.borrows import Borrows

class BorrowDetails(db.Model):
    __tablename__ = 'tbl_borrow_details'
    id_borrow_detail = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    borrow = db.relationship('Borrows', backref='tbl_borrow_details', uselist = False)
    id_borrow = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_borrows.id_borrow'))
    book = db.relationship('Books', backref='tbl_borrow_details', uselist = False)
    id_book = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_books.id_book'))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    
def select_all_detail(page_name,page_value,per_page_name,per_page_value):
    query = (
        BorrowDetails.query
        .join(Borrows, BorrowDetails.id_borrow == Borrows.id_borrow)
        .filter_by(status = False)
        .order_by(BorrowDetails.created_at.desc())
        .paginate(**{page_name : page_value, per_page_name : per_page_value})
    )
    return query
    