from marshmallow import Schema, fields, validate
from app.schema.user_schema import UserSchema
from app.schema.borrows_schema import BorrowsSchema
from app.schema.books_schema import BooksSchema

class BorrowDetailsSchema(Schema):
    id_borrow_detail = fields.UUID(dump_only=True)
    id_borrow = fields.Nested(BorrowsSchema, attribute='tbl_borrows', many=False, data_key='borrow')
    id_book = fields.Nested(BooksSchema, attribute='tbl_books', many=False, data_key='book')  
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)