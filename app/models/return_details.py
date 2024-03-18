from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class ReturnDetails(db.Model):
    __tablename__ = 'tbl_return_details'
    id_return_detail = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    returns = db.relationship('Returns', backref='tbl_return_details', uselist = False)
    id_return = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_returns.id_return'))
    book = db.relationship('Books', backref='tbl_return_details', uselist = False)
    id_book = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_books.id_book'))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    