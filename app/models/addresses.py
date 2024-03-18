from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy import select

class Addresses(db.Model):
    __tablename__ = 'tbl_addresses'
    id_address = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    

def select_user_address(id):
    query = select(Addresses).where(Addresses.id_address == id)
    result = db.session.execute(query)
    id_address = result.scalar()  #return single scalar result
    return id_address