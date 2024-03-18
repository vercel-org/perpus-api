from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.borrows import Borrows
from sqlalchemy import select

class Returns(db.Model):
    __tablename__ = 'tbl_returns'
    id_return = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    return_date = db.Column(db.DateTime, default = datetime.now)
    user = db.relationship('Users', backref='tbl_returns', uselist = False)
    id_user = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_users.id_user'))
    borrow = db.relationship('Borrows', backref='tbl_returns', uselist = False)
    id_borrow = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_borrows.id_borrow'))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    
from app.models.borrow_details import BorrowDetails
def select_notin_borrow(page_name,page_value,per_page_name,per_page_value):
    subquery = (
        select(Returns.id_borrow)
        .subquery()
    )
    
    query = (
        BorrowDetails.query
        .join(Borrows, BorrowDetails.id_borrow == Borrows.id_borrow)
        .filter_by(status = True)
        .outerjoin(subquery, BorrowDetails.id_borrow == subquery.c.id_borrow)
        .filter(subquery.c.id_borrow.is_(None)) 
        .paginate(**{page_name : page_value, per_page_name : per_page_value})
    ) 
    return query

def limit_borrow(id): 
    subquery = (
        select(Returns.id_borrow)
        .subquery()
    )
    query = (
        Borrows.query
        .filter_by(status = True, id_user = id)
        .outerjoin(subquery, Borrows.id_borrow == subquery.c.id_borrow)
        .filter(subquery.c.id_borrow.is_(None)) 
    )
    count = query.count()
    return count