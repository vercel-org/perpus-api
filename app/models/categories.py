from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Categories(db.Model):
    __tablename__ = 'tbl_categories'
    id_category = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    
     
 
