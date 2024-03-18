from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import select_by_id, select_all, filter_by, meta_data, order_by
from flask import request
from app.schema.roles_schema import RolesSchema
from app import response_handler
from app.models.roles import Roles
from app import db 
from app.controllers import auth 
from uuid import UUID
import os
 
@jwt_required()
def create_role():
    try: 
        # Check Auth
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('super'): 
            json_body = request.json
            
            # Checking errors with schema
            schema = RolesSchema() 
            errors = schema.validate(json_body)
            if errors:
                return response_handler.bad_request(errors)
            else:
                for i in select_all(Roles):
                    if json_body['role'] == i.role:
                        return response_handler.conflict_array('role','Role is Exist')
                    
            new_role = Roles(role = json_body['role'])
                    
            db.session.add(new_role)
            db.session.commit()
        
            data = schema.dump(new_role)
            return response_handler.created(data,"Role Successfull Created ")
        else:
            return response_handler.unautorized()
    
    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f"{err.args[0]} field must be filled")

    except Exception as err:
        return response_handler.bad_gateway(str(err))
 
@jwt_required()
def role(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            # Check id is UUID or not
            UUID(id)
            # Check Role is exist or not
            roles = select_by_id(Roles,id)
            if roles == None:
                return response_handler.not_found_array('role','Role not Found')
            
            # Add data to response 
            schema = RolesSchema()
            data = schema.dump(roles)
            
            return response_handler.ok(data,"")
        else:
            return response_handler.unautorized()
        
    except ValueError:
        return response_handler.bad_request_array("id_role","Invalid Id")

    except Exception as err:
        return response_handler.bad_gateway(str(err))
  
@jwt_required()
def update_role(id):
    try: 
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('super'):
            # Check  id is UUID or not
            UUID(id)
            json_body = request.json
            
            # Check error with schema
            schema = RolesSchema()
            errors = schema.validate(json_body) 
            if errors:
                return response_handler.bad_request(errors)
             
            # Check role if not exist
            roles = select_by_id(Roles,id)
            if roles == None:
                return response_handler.not_found_array('role','Role not Found')

            # Check name of role same with previous or not
            if json_body['role'] == roles.role: 
                return response_handler.bad_request_array('role','Your Role Already Updated')
            else:
                current_role = filter_by(Roles, 'role', json_body['role'])
                # Check role same with the others or not
                if current_role != None: 
                    return response_handler.conflict_array('role','Role is exist') 
                
                # Add role to db
                roles.name = json_body['role']  
                db.session.commit()
                
                data = schema.dump(roles)

                return response_handler.ok(data, 'Role successfuly updated')
        else:
            return response_handler.unautorized()

    except ValueError:
        return response_handler.bad_request_array('id_role','Invalid Id')

    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))
 
@jwt_required()
def roles():
    try:
        current_user = get_jwt_identity() 
        
        if current_user['id_role'] in auth('admin'):
            # Get param from url
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', int(os.getenv('PER_PAGE')), type=int)
            # Check is page exceed or not
            page_exceeded = meta_data(Roles,page,per_page)
            if page_exceeded: 
                return response_handler.not_found("Page Not Found") 
            
            # Query data categories all
            roles = order_by(Roles, 'page', page, 'per_page', per_page)
            
            # Iterate to data
            data = []
            for i in select_all(Roles):
                data.append(RolesSchema().dump(i))
 
            return response_handler.ok_with_meta(data, roles)
        else:
            return response_handler.unautorized()
        
    except Exception as err:
        return response_handler.bad_request(str(err))
 

