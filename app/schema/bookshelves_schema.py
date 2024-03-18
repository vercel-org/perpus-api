from marshmallow import Schema, fields, validate

class BookshelvesSchema(Schema):
    
    id_bookshelf = fields.UUID(dump_only=True)
    bookshelf = fields.Str(required=True,
                           validate=[validate.Length(min=1, error='Bookshelf must be filled'),
                                     validate.Length(min=2, max=100),
                                     validate.Regexp(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d\s]+$',error='Invalid name format. Only letters, space, and at least one number are allowed.')])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)