from marshmallow import Schema, fields, validate
from app.schema.authors_schema import AuthorsSchema
from app.schema.publishers_schema import PublishersSchema
from app.schema.categories_schema import CategoriesSchema
from app.schema.bookshelves_schema import BookshelvesSchema

class BooksSchema(Schema):
       
    id_book = fields.UUID(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    stock = fields.Int(required=True, validate=validate.Range(min=0))
    picture = fields.Str(validate=validate.Length(max=200)) 
    id_author = fields.UUID(required=True)
    id_publisher = fields.UUID(required=True)
    id_category = fields.UUID(required=True)
    id_bookshelf = fields.UUID(required=True) 
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


 