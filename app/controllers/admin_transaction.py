from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import auth
from uuid import UUID
from flask import request
from app.models.borrows import Borrows
from app.models import meta_data, select_by_id,select_all,filter_by
from app.models.books import Books
import os
from app import response_handler,db
from app.models.borrow_details import BorrowDetails, select_all_detail
from app.schema.borrow_details_schema import BorrowDetailsSchema
from app.schema.user_schema import UserSchema 
from app.schema.books_schema import BooksSchema 
from app.models.returns import select_notin_borrow 
from app.models.returns import Returns
from app.models.return_details import ReturnDetails
from uuid import uuid4
from app.schema.borrows_schema import BorrowsSchema

@jwt_required()
def booked_books():
    try:
        # Check Auth
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            # Get param from url
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', int(os.getenv('PER_PAGE')), type=int)
            
            # Check is page exceed or not
            page_exceeded = meta_data(BorrowDetails,page,per_page)
            if page_exceeded: 
                return response_handler.not_found("Page Not Found")
            from app.schema.borrows_schema import BorrowsSchema
            # Query data all
            meta = select_all_detail('page', page, 'per_page', per_page)
            data = []
            for i in meta.items:
                data.append({
                    "borrow_detail" : BorrowDetailsSchema().dump(i),
                    "borrow" : BorrowsSchema().dump(i.borrow),
                    "book" : BooksSchema().dump(i.book),
                    "user" : UserSchema().dump(i.borrow.user)
                })
            return response_handler.ok_with_meta(data,meta)
                 
        return response_handler.unautorized() 
    except Exception as err:
        return response_handler.bad_gateway(str(err))

# By id_borrow
@jwt_required()
def acc_book(id):
    try:
        # Check Auth
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            UUID(id)
            borrows = select_by_id(Borrows,id)
           
            if borrows == None:
                return response_handler.not_found('Borrows not Found')
            elif borrows.status == True:
                return response_handler.conflict('Borrowed book already acc')
            
            bdetail = filter_by(BorrowDetails,'id_borrow',borrows.id_borrow)
            books = select_by_id(Books,str(bdetail.id_book))
            books.stock = books.stock - 1
            borrows.status = True
            db.session.commit()
            return response_handler.ok("","Book been acc")
        return response_handler.unautorized()
    
    except ValueError:
        return response_handler.bad_request("Invalid Id")
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')
    
    except Exception as err:
        return response_handler.bad_gateway(str(err))    

#needpagination
@jwt_required()
def return_books():
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'): 
        
            # Get param from url
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', int(os.getenv('PER_PAGE')), type=int)
            
            # Check is page exceed or not
            page_exceeded = meta_data(BorrowDetails,page,per_page)
            if page_exceeded: 
                return response_handler.not_found("Page Not Found")
            
            # Query data bookshelves all
            meta = select_notin_borrow('page', page, 'per_page', per_page)
            data = []
            for i in meta.items:
                data.append({
                    "borrow" : BorrowsSchema().dump(i.borrow),
                    "borrow_detail" : BorrowDetailsSchema().dump(i),
                    "id_user" : UserSchema().dump(i.borrow.user) ,
                    "id_book" : BooksSchema().dump(i.book)
                })
            return response_handler.ok_with_meta(data,meta)
        else:
            return response_handler.unautorized()
        
    except Exception as err:
        return response_handler.bad_gateway(err)

@jwt_required()
def create_return():
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('admin'):
            json_body = request.json
            
            # Check id valid or not 
            UUID(json_body['id_user'])
            UUID(json_body['id_borrow'])
            UUID(json_body['id_book'])
            
            # Check the book is already return or not
            for i in select_all(Returns):
                if json_body['id_borrow'] == str(i.id_borrow):
                    return response_handler.conflict("Book already returned")
            
            # Check is there any transaction or not
            data = []
            for i in select_all(BorrowDetails):
                data.append({
                    "id_borrow" : i.id_borrow,
                    "id_book": i.id_book,
                    "id_user": i.borrow.id_user
                })
            match = False
            for i in data:
                if (i['id_borrow'] == json_body['id_borrow'] and
                   i['id_book'] == json_body['id_book'] and
                   i['id_user'] == json_body['id_user']): 
                    match = True
                    break
            if not match:
                return response_handler.not_found("Transaction not found")
            
            id_return = uuid4()
            new_return = Returns(id_return = id_return,
                                id_user = json_body['id_user'],
                                id_borrow = json_body['id_borrow'])
            new_return_detail = ReturnDetails(id_return = id_return,
                                            id_book = json_body['id_book'])
                        
            books = select_by_id(Books, json_body['id_book'])
            books.stock = books.stock + 1
            db.session.add(new_return)
            db.session.add(new_return_detail)
            db.session.commit()
                        
            return response_handler.ok("","Book success returned")
        else:
            return response_handler.unautorized()
    
    except ValueError:
        return response_handler.bad_request("Invalid Id")
    
    except Exception as err:
        return response_handler.bad_gateway(err)