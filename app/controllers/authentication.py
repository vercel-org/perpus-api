from datetime import datetime
from flask import request
# from flask_jwt_extended import decode_token
from app import db, response_handler
from app.models.users import Users
from app.hash import hash_password
from app.generate_token import generate_token
from app.schema.user_schema import UserSchema

def login():
    try:        
        json_body = request.json   
        errors = UserSchema(only=['username','password']).validate(json_body)
        if errors:
            return response_handler.bad_request(errors)
        
        user = Users.query.filter_by(username = json_body['username']).first()
    
        if not user:
            return response_handler.not_found_array("username","Username not found")
        
        if hash_password(json_body['password']) != user.password:
            return response_handler.unautorized_array("password","Invalid password, please check your password again")
        
        user.last_login = datetime.now()
        db.session.commit()
        data = generate_token({"id_user":user.id_user,
                                "id_role":user.id_role, 
                                "role":user.role.role,
                                "status": user.status}
                              )
        data.update({
            "id_user":user.id_user,
            "id_role":user.id_role, 
            "role":user.role.role,
            "status": user.status
        })
        
        # decode token
        # print(decode_token(token['token']['access_token']))
        # decode = (decode_token(token['token']['access_token']))
        # print(decode['sub']['role'])
        return response_handler.ok(data, message='Login successful, have a nice day')
    
    except KeyError as err:
        return response_handler.bad_request_array(f'{err.args[0]}', f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))