from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
class Bookshelves(db.Model):
    __tablename__ = 'tbl_bookshelves'
    id_bookshelf = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    bookshelf = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)
    
     