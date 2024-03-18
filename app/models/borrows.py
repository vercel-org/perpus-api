from app import db
import uuid, os
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta 

class Borrows(db.Model):
    __tablename__ = 'tbl_borrows'
    id_borrow = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    return_date = db.Column(db.DateTime, onupdate = datetime.now() + timedelta(days = int(os.getenv('RETURN_DATE'))))
    status = db.Column(db.Boolean, default = False)
    user = db.relationship('Users', backref='tbl_borrows', uselist = False)
    id_user = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_users.id_user'))
    
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
     
def select_all(page_name,page_value,per_page_name,per_page_value):
    query = (
        Borrows.query
        .filter_by(status = False)
        .order_by(Borrows.created_at.desc())
        .paginate(**{page_name : page_value, per_page_name : per_page_value})
    )
    return query



 
     