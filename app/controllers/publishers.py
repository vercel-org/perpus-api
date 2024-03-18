from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.models import select_all, select_by_id
from app.models.publishers import Publishers
from app.schema.publishers_schema import PublishersSchema
from flask import request
from app import response_handler,db
from uuid import UUID
from app.controllers import auth, check_update, get_paginated_data, get_read_param
import os

@jwt_required()
def create_publisher():
    try:
        # Check Auth
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'): 
            json_body = request.json
            
            # Checking errors with schema
            schema = PublishersSchema() 
            errors = schema.validate(json_body)
            if errors:
                return response_handler.bad_request(errors)
            else:
                for i in select_all(Publishers):
                    if json_body['name'] == i.name:
                       return response_handler.bad_request_array('name','Publisher is Exist')
                    elif json_body['email'] == i.email:
                       return response_handler.bad_request_array('email','Publisher email is Exist')
                                    
            new_publisher = Publishers(name = json_body['name'],
                                       email = json_body['email'], 
                                       phone_number = json_body['phone_number'])

            db.session.add(new_publisher)
            db.session.commit()
        
            data = schema.dump(new_publisher)
            return response_handler.created(data,"Publisher Successfull Created ")
        else:
            return response_handler.unautorized()
    
    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
@jwt_required() 
def publisher(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('public'):
            # Check id is UUID or not
            UUID(id)
            # Check Publisher is exist or not
            publisher = select_by_id(Publishers, id)
            if publisher == None:
                return response_handler.not_found_array('id_publisher','Publisher not Found')
            
            # Add data to response 
            schema = PublishersSchema()
            data = schema.dump(publisher)
            
            return response_handler.ok(data,"")
        else:
            return response_handler.unautorized()
        
    except ValueError:
        return response_handler.bad_request_array('id_publisher','Invalid Id')
    
    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def update_publisher(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            # Check id is UUID or not
            UUID(id)
            json_body = request.json
            
            # Check error with schema
            schema = PublishersSchema()
            errors = schema.validate(json_body) 
            if errors:
                return response_handler.bad_request(errors)
            
            # Check data if not exist
            publishers = select_by_id(Publishers,id)
            if publishers == None:
                return response_handler.not_found_array('publisher','Publisher not Found')
        
            # Check data of publisher same with previous or not 
            array = ['name','email','phone_number']
            if check_update(json_body, publishers, array) == True:
                return response_handler.bad_request_array('publisher','Publisher Already Updated')
            # Check data same with other or not
            else:
                conflict = {}
                for i in select_all(Publishers):
                    if str(i.id_publisher) != id:
                        if json_body['name'] == i.name:
                            conflict.update({'name':['Publisher is Exist']})
                        if json_body['email'] == i.email:
                            conflict.update({'email':['Publisher Email is Exist']})
                        if json_body['phone_number'] == i.phone_number and json_body['phone_number'] != '':
                            conflict.update({'phone_number':['Publisher Phone Number is Exist']})
                if conflict:
                    return response_handler.conflict(conflict)
                else:
                    # Add data to db
                    publishers.name = json_body['name']
                    publishers.email = json_body['email']
                    publishers.phone_number = json_body['phone_number']
                    db.session.commit()
                    
                    data = schema.dump(publishers)
                     
                    return response_handler.ok(data, 'Publisher successfull updated')
        else:
            return response_handler.unautorized()

    except ValueError:
        return response_handler.bad_request_array('id_publisher','Invalid Id')

    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def publishers():
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            
              # Get param from url with get_read_param function in init
            params = get_read_param(request) 
            page, per_page, filter = params.values()
            
            # Get pagination data from get_paginated_data function in init
            publishers_data = get_paginated_data(Publishers,page,per_page,field='name',filter=filter)
            
            # return data
            if publishers_data is not None:
                data = [PublishersSchema(only=('id_publisher','name','email','phone_number')).dump(publisher) for publisher in publishers_data.items]
                return response_handler.ok_with_meta(data, publishers_data)
            else:
                return response_handler.not_found('Page Not Found')
  
        else:
            return response_handler.unautorized()
        
    except Exception as err:
        return response_handler.bad_request(str(err))
            