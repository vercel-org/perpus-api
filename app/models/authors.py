from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Authors(db.Model):
    __tablename__ = 'tbl_authors'
    id_author = db.Column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(10), nullable = False)
    phone_number = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now)

def select_authors():
    select_author = Authors.query.all()
    return select_author