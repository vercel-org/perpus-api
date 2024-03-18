from marshmallow import Schema, fields, validate

class RolesSchema(Schema):
    
    id_role = fields.UUID(dump_only=True)
    role = fields.Str(required=True,
                      validate=[validate.Length(min=1, error='Name must be filled'),
                                validate.Length(min=2, max=100),
                                validate.Regexp(r'^[a-zA-Z][a-zA-Z\s]*$',error='Name should only contain letters.')])
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)