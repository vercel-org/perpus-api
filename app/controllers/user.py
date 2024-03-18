from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import db, secret_key, response_handler
from app.controllers import generate_token, send_email, reset_password_template, activation_account_template, auth
from app.hash import hash_password
from app.models import select_all, meta_data, select_by_id, filter_by
from app.models.addresses import Addresses
from app.models.roles import select_role_id
from app.models.users import Users, user_all, select_user_email
from app.schema.address_schema import AddressSchema
from app.schema.roles_schema import RolesSchema
from app.schema.user_schema import UserSchema
from datetime import datetime
from uuid import uuid4, UUID
import os
import cloudinary


def register():
    try:
        json_body = request.json
        user_schema = UserSchema()
        
        # Checking errors with schema
        errors = user_schema.validate(json_body)
        if errors:
            return response_handler.bad_request(errors)
        else:
            for i in select_all(Users):
                if json_body['username'] == i.username:
                    return response_handler.bad_request_array("username","Username is exist")
                elif json_body['email'] == i.email:
                    return response_handler.bad_request_array("email","Email is exist")
          
        id_address = uuid4()
        address = Addresses(id_address = id_address)
        
        new_user = Users(username = json_body['username'],
                        name = json_body['name'],
                        email = json_body['email'],
                        password = hash_password(json_body['password']),
                        picture = os.getenv('DEFAULT_PROFILE_PICTURE'),
                        id_role = select_role_id(os.getenv('USER_ROLE')),
                        id_address = id_address
                        )
        db.session.add(address)
        db.session.add(new_user)
        db.session.commit()
        
        user_schema = UserSchema(only=('id_user', 'name', 'username', 'email', 'password', 'created_at'))
        data = user_schema.dump(new_user)

        return response_handler.created(data, "User registered successfully")
    
    except KeyError as err:
        return response_handler.bad_request_array(f'"{err.args[0]}"',f"{err.args[0]} field must be filled")
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def profile():
    try:
        current_user = get_jwt_identity()
        if current_user['id_user'] == current_user['id_user']:
            users = select_by_id(Users,current_user['id_user']) 
            
            data = {"user" : UserSchema().dump(users),
                    "address" : AddressSchema().dump(users.address),
                    "role" : RolesSchema().dump(users.role)}
            
            return response_handler.ok(data,"")
        else:
            return response_handler.unautorized() 
        
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def user(id):
    try:
        current_user = get_jwt_identity()
        if current_user['status'] == True or current_user['id_user'] == str(id):
            
            # Check id is UUID or not
            UUID(id)
            # Check user is exist or not 
            users = select_by_id(Users,id)
            if users == None:
                return response_handler.not_found_array("id_user",'User not Found')
            
            data = {"user" : UserSchema(exclude=('password',)).dump(users),
                    "address" : AddressSchema().dump(users.address),
                    "role" : RolesSchema().dump(users.role)}
            
            return response_handler.ok(data,"")
        else:
            return response_handler.unautorized()
        
    except ValueError:
        return response_handler.bad_request_array("id_user","Invalid Id")
        
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()  
def update_user(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_user'] == id:
            # Check  id is UUID or not
            UUID(id)
            form_body = request.form
            
            # Select formbody to check
            user_data = {'username':form_body['username'],
                    'email':form_body['email'],
                    'password':form_body['password'],
                    'name':form_body['name']}
            address_data = {'address': form_body['address']}
            
            # Check error with schemaa
            user_schema = UserSchema(only=['username','name','email','password'])
            address_schema = AddressSchema()

            user_errors = user_schema.validate(user_data)
            address_errors = address_schema.validate(address_data)
            if user_errors: 
                return response_handler.bad_request(user_errors)
            if address_errors:
                return response_handler.bad_request(address_errors)
            
            # Select user by id
            user = select_by_id(Users,id)
            # Select address by id
            address = select_by_id(Addresses,user.id_address) 
              
            # Check username is exist or not
            if form_body['username'] == user.username:
                user.username = form_body['username']
            else:
                existing_user = filter_by(Users,'username',form_body['username'])
                if existing_user:
                    return response_handler.conflict_array("username",'Username already exists')
                
            # Update user
            user.name = form_body['name']
            user.username = form_body['username']
            user.email = form_body['email']
            user.password = hash_password(form_body['password'])
            user.updated_at = datetime.now()

            # Update address
            address.address = form_body['address']
             
            if 'picture' in request.files:
                uploadImage = request.files['picture']
                cloudinary_response = cloudinary.uploader.upload(uploadImage,
                                                    folder = "perpus-api/user-profile-picture/",
                                                    public_id = "user_"+str(user.id_user),
                                                    overwrite = True,
                                                    width = 250,
                                                    height = 250,
                                                    grafity = "face",
                                                    radius = "max",
                                                    crop = "fill"
                                                    ) 
                user.picture = cloudinary_response["url"]
            elif 'picture' not in request.files:
                user.picture = user.picture

            db.session.commit()
            
            user_schema = UserSchema()
            data = user_schema.dump(user)
            data.update({'address':address.address})
            
            return response_handler.ok(data, "Your data is updated")
        else:
            return response_handler.unautorized()

    except ValueError:
        return response_handler.bad_request_array("id_user","Invalid Id")
    
    except KeyError as err: 
        return response_handler.bad_request_array(f'{err.args[0]}', f"{err.args[0]} field must be filled")
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def list_user():
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            # Get param from url
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', int(os.getenv('PER_PAGE')), type=int)
            
            # Check is page exceed or not
            page_exceeded = meta_data(Users,page,per_page)
            if page_exceeded: 
                return response_handler.not_found("Page Not Found")
            # Query data bookshelves all
            meta = user_all('page', page, 'per_page', per_page)
            data = []
            for i in meta.items:
                data.append({
                    "user" : UserSchema(only=('id_user','name','username','picture','last_login','status')).dump(i),
                    #"address" : AddressSchema().dump(i.address),
                    "role" : RolesSchema(only=('id_role','role')).dump(i.role)
                })
                
            return response_handler.ok_with_meta(data,meta)
        else:
            return response_handler.unautorized()
    except Exception as err:
        return response_handler.bad_gateway(str(err))

def reset_password():
    try:
        json_body = request.json
        email = json_body['email']
        errors = UserSchema(only=['email']).validate(json_body)
        if errors:
            return response_handler.bad_request(errors)
        
        user = select_user_email(email)
        if user == None:
            return response_handler.bad_request_array("email","Email not registered to an account")
        
        # Generate Token
        token = generate_token(email)
        # Replace . with | 
        reset_token = token.replace('.','|')
        # Add html url
        reset_url = os.getenv('RESET_PASSWORD_FE')+'/'+reset_token
        reset_body = reset_password_template(reset_url,user.name)
        
        #Send mail
        send_email(email,"Reset Password",reset_body)
        
        return response_handler.ok("","Please check your email to reset your password")
    except Exception as err:
        return response_handler.bad_gateway(str(err))

def change_password(token):
    try:
        json_body = request.json
        serializer = URLSafeTimedSerializer(secret_key)
        reset_token = token.replace('|','.')
        email = serializer.loads(reset_token, max_age=os.getenv('MAX_AGE_MAIL'))  # Token expires after 1 hour (3600 seconds)
        user = select_user_email(email)
        if user:
            errors = UserSchema(only=['password']).validate(json_body)
            if errors:
                return response_handler.bad_request(errors)
            user.password = hash_password(json_body['password'])
            db.session.commit()
            return response_handler.ok("","Your password success to change")
        else:
            return response_handler.not_found("Account not found")
    except SignatureExpired:
        return response_handler.unautorized("Your Token is Expired")
    except BadSignature:
        return response_handler.bad_request("Your Token is Invalid")
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def activation_email():
    try:
        current_user = get_jwt_identity()
        if current_user['status'] == False:
            user = select_by_id(Users,current_user['id_user'])
            token = generate_token(user.email)
            activation_token = token.replace('.','|')
            # Add html url
            activation_url = os.getenv('ACTIVATION_ACC_FE')+'/'+activation_token
            activate_body = activation_account_template(activation_url,user.username)
            #Send mail
            send_email(user.email,"Activation Account",activate_body)
        
            return response_handler.ok("","Please check your email to activate your account")
        elif current_user['status'] == True:
            return response_handler.conflict_array('status','Your account already activated')
    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def activation_account(token):
    try:
        current_user = get_jwt_identity()
        if current_user['status'] == False:
            serializer = URLSafeTimedSerializer(secret_key)
            activation_token = token.replace('|','.')
        
            email = serializer.loads(activation_token, max_age=os.getenv('MAX_AGE_MAIL'))  # Token expires after 1 hour (3600 seconds)
            user = select_user_email(email)
            user.status = True
            db.session.commit()
            return response_handler.ok("","Your Account success to activate")
        elif current_user['status'] == True:
            return response_handler.conflict_array('status','Your account already activated')
    except Exception as err:
        return response_handler.bad_gateway(str(err))
        