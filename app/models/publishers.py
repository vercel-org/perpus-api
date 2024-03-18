
from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Publishers(db.Model):
    __tablename__ = 'tbl_publishers'
    id_publisher = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String(100))
    email = db.Column(db.String(250))
    phone_number = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    
     