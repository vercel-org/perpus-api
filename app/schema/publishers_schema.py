from marshmallow import Schema, fields, validate, ValidationError
import re

class PublishersSchema(Schema): 
    
    id_publisher = fields.UUID(dump_only=True)
    name = fields.Str(required=True,
                      validate=[validate.Length(min=1, error='Name must be filled'),
                                validate.Length(min=2, max=100),
                                validate.Regexp(r'^[a-zA-Z][a-zA-Z\s]*$',error='Name should only contain letters.')])
    email = fields.Str(required=True,
                       validate=[validate.Length(min=1, error='Email must be filled'),
                                 validate.Email(error='Invalid email format')])
    phone_number = fields.Str(required=False,
                              allow_none=True,
                              validate=[validate.Regexp(r'^(\+?[1-9]\d{8,14})?$',error='Invalid phone number format. It should start with "+" followed by digits (9-14 digits allowed).')])
     
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    