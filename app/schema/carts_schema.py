from marshmallow import Schema,validate,fields
from app.schema.user_schema import UserSchema
from app.schema.books_schema import BooksSchema
from app.schema.address_schema import AddressSchema
 
class CartsSchema(Schema):
    
    id_cart = fields.UUID(dump_only = True)
    id_user = fields.Nested(UserSchema, attribute='tbl_users', many=False, data_key='user')
    id_book = fields.Nested(BooksSchema, attribute='tbl_books', many=False, data_key='book')
    
    