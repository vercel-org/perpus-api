from marshmallow import Schema, fields, validate

class CategoriesSchema(Schema):
    
    id_category = fields.UUID(dump_only=True)
    category = fields.Str(required=True,
                          validate=[validate.Length(min=1, error='Bookshelf must be filled'),
                                    validate.Length(min=2, max=100),
                                    validate.Regexp(r'^[a-zA-Z][a-zA-Z\s]*$',error='Category should only contain letters')])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)