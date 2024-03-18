from marshmallow import Schema,validate,fields
from app.schema.roles_schema import RolesSchema
from app.schema.address_schema import AddressSchema
 
class UserSchema(Schema):
    
      id_user = fields.UUID(dump_only = True)
      name = fields.Str(required = True,
                        validate = [validate.Length(min=1, error='Name must be filled'),
                                    validate.Length(min=2, max=100),
                                    validate.Regexp(r'^[a-zA-Z\s]+$', error='Invalid name format, Only letters and space are allowed.')])
      username = fields.Str(required = True,
                        validate = [validate.Length(min=1, error='Username must be filled'),
                                    validate.Length(min=4, max=12, error='Username must be between 4 and 12 characters.'),
                                    validate.Regexp(r'^[a-zA-Z][a-zA-Z0-9._]+$', error='First character must letter(upper or lower case), the next character can use underscore(_) or dot(.) and number')])
      email = fields.Str(required = True,
                        validate = [validate.Length(min=1,error='Email must be filled'),
                                    validate.Email()])
      password = fields.Str(required = True,
                              validate = [validate.Length(min=1, error='Password must be filled'),
                                          validate.Length(min=8),
                                          validate.Regexp(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).*$',error='Password must containat least one lowercase letter, one uppercase latter, one digit, and one special character.')])
      id_role = fields.Nested(RolesSchema, attribute='tbl_roles', many=False, data_key='role')
      id_address = fields.Nested(AddressSchema, attribute='tbl_addresses', many=False, data_key='address')
      picture = fields.Str(validate=validate.Length(max=200))
      status = fields.Boolean()
      created_at = fields.DateTime(dump_only = True)
      updated_at = fields.DateTime(dump_only = True)
      last_login = fields.DateTime(dump_only = True)
    

      
    
        