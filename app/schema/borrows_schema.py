from marshmallow import Schema, fields, validate
from app.schema.user_schema import UserSchema


class BorrowsSchema(Schema):
    
    id_borrow = fields.UUID(dump_only=True)
    return_date = fields.DateTime(dump_only=True)
    status = fields.Boolean()
    id_user = fields.Nested(UserSchema, attribute='tbl_users', many=False, data_key='user')
 
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)