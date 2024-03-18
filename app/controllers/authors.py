from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import select_all, select_by_id, order_by, filter_by, meta_data
from app.models.authors import Authors
from app.schema.authors_schema import AuthorsSchema
from flask import request
from app import response_handler,db
from uuid import UUID
from app.controllers import auth,check_update,get_paginated_data,get_read_param
import os
  
@jwt_required()
def create_author():
    try:
        # Check Auth
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'): 
            json_body = request.json
            
            # Checking errors with schema
            schema = AuthorsSchema() 
            errors = schema.validate(json_body)
            if errors:
                return response_handler.bad_request(errors) 
            else:
                for i in select_all(Authors):
                    if json_body['name'] == i.name:
                        return response_handler.bad_request_array('name',"Author is Exist")
            
            # Create Author object
            new_author = Authors(name = json_body['name'],
                                email = json_body['email'],
                                gender = json_body['gender'],
                                phone_number = json_body['phone_number'],
                                )
            
            # Add author object to db
            db.session.add(new_author)
            db.session.commit()

            # Add object to schema
            data = schema.dump(new_author)
            return response_handler.created(data,"Author Successfull Created ")
        else:
            return response_handler.unautorized()
    
    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
@jwt_required() 
def author(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('public'):
            # Check id is UUID or not
            UUID(id)
            # Check Author is exist or not
            author = select_by_id(Authors, id)
            if author == None:
                return response_handler.not_found_array('id_author','Author not Found')
            
            # Add data to schema 
            schema = AuthorsSchema()
            data = schema.dump(author)
            
            return response_handler.ok(data,"")
        else:
            return response_handler.unautorized()
        
    except ValueError:
        return response_handler.bad_request_array('id_author','Invalid Id')
        
    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def update_author(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            # Check  id is UUID or not
            UUID(id)
            json_body = request.json
            
            # Check error with schema
            schema = AuthorsSchema()
            errors = schema.validate(json_body) 
            if errors:
                return response_handler.bad_request(errors)
            
            # Check Author if not exist
            authors = select_by_id(Authors,id)
            if authors == None:
                return response_handler.not_found_array('name','Author not Found')
            
            # Check data of author same with previous or not 
            array = ['name','email','gender','phone_number']
         
            if check_update(json_body, authors, array) == True:
                return response_handler.bad_request_array('author','Author Already Updated')
            else:
                conflict = {}
                for i in select_all(Authors):
                    if str(i.id_author) != id:
                        if json_body['name'] == i.name:
                            conflict.update({'name':['Author is Exist']})
                        if json_body['email'] == i.email:
                            conflict.update({'email':['Author Email is Exist']})
                        if json_body['phone_number'] == i.phone_number and json_body['phone_number'] != '':
                            conflict.update({'phone_number':['Author Phone Number is Exist']})
                if conflict:
                    return response_handler.conflict(conflict)
                else: 
                    # Add author to db
                    authors.name = json_body['name']
                    authors.email = json_body['email']
                    authors.gender = json_body['gender']
                    authors.phone_number = json_body['phone_number']
                    db.session.commit()
                    
                    # Add author to schema
                    data = schema.dump(authors)
                    
                    return response_handler.ok(data, "Author successfull updated")
        else:
            return response_handler.unautorized()

    except ValueError:
        return response_handler.bad_request_array('id_author',"Invalid Id")
    
    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def authors():
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            # Get param from url with get_read_param function in init
            params = get_read_param(request) 
            page, per_page, filter = params.values()
            
            # Get pagination data from get_paginated_data function in init
            authors_data = get_paginated_data(Authors,page,per_page,field='name',filter=filter)
            
            # return data
            if authors_data is not None:
                data = [AuthorsSchema(only=('id_author','name','email','gender','phone_number')).dump(author) for author in authors_data.items]
                return response_handler.ok_with_meta(data, authors_data)
            else:
                return response_handler.not_found('Page Not Found')
        
    except Exception as err:
        return response_handler.bad_request(str(err))
            