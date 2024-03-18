import uuid, os
from sqlalchemy.dialects.postgresql import UUID 
from app import db, app
from datetime import datetime
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class Roles(db.Model):
    __tablename__ = 'tbl_roles'
    id_role = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

def select_role_name(role):
    query = Roles.query.filter_by(role = os.getenv(role)).first()
    return query

def select_role_id(role):
    query = db.session.query(Roles.id_role).filter_by(role = role).scalar()
    return query

def super_admin_role():
    query = select(Roles.id_role).where(Roles.role == os.getenv('SUPER_ADMIN_ROLE'))
    result = db.session.execute(query)
    id_role = result.scalar()
    return id_role

def admin_role():
    query = select(Roles.id_role).where(Roles.role == os.getenv('ADMIN_ROLE'))
    result = db.session.execute(query)
    id_role = result.scalar()
    return id_role

# Create Roles for 1st time
def create_roles():
    with app.app_context():
        try:
            super_admin = select_role_name('SUPER_ADMIN_ROLE')
            admin = select_role_name('ADMIN_ROLE')
            user = select_role_name('USER_ROLE')
             
            if not super_admin and not admin and not user:
                super_admin_role = Roles(id_role=uuid4(),role=os.getenv('SUPER_ADMIN_ROLE'))
                admin_role = Roles(id_role=uuid4(),role=os.getenv('ADMIN_ROLE'))
                user_role = Roles(id_role=uuid4(),role=os.getenv('USER_ROLE'))
                
                db.session.add(super_admin_role)
                db.session.add(admin_role)
                db.session.add(user_role)
                db.session.commit() 
           
        except IntegrityError:
            db.session.rollback()
        
        except:
            pass