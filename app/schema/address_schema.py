from marshmallow import Schema, fields, validate, ValidationError

class AddressSchema(Schema):
        
    id_address = fields.UUID(dump_only=True)
    address = fields.Str(required=True, validate=[validate.Length(min=1, error='Address must be filled'),
                                                  validate.Length(min=2, max=100)])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    