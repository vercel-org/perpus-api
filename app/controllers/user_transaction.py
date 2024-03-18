import os
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID,uuid4
from app import db, response_handler
from app.models import select_by_id, select_all, filter_by, order_by, meta_data
from app.models.cart import Carts, select_cart, select_carts, cart_all
from app.schema.carts_schema import CartsSchema
from app.schema.books_schema import BooksSchema
from app.models.borrows import Borrows
from app.models.borrow_details import BorrowDetails
from app.models.returns import limit_borrow, Returns
from app.models.books import select_book_id
from app.controllers import auth

@jwt_required()
def create_cart(id):
    try: 
        # Check Auth
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('public'):
            # Check id is UUID or not
            UUID(id)
            # Check Book is exist or not
            books = select_book_id(id)
            if books == None:
                return response_handler.not_found('Book not Found')
            
            data = []
            for i in select_all(Returns):
                data.append(i.id_borrow)
                
            for i in select_all(BorrowDetails):
                if current_user['id_user'] == str(i.borrow.id_user) and i.borrow.status == False and str(i.id_book) == id and i.id_borrow not in data:
                    return response_handler.bad_request("You already request this book, Please contact admin")
            
            for i in select_all(Carts):
                if str(i.id_user) == str(current_user['id_user']) and str(i.id_book) == str(id):
                    return response_handler.conflict("The book already in your cart")
            
            new_cart = Carts(id_user = current_user['id_user'],
                             id_book = id )
                            
            db.session.add(new_cart)
            db.session.commit()
            return response_handler.created("","Book successfull add to cart ")
        else:
            return response_handler.unautorized()
        
    except ValueError:
        return response_handler.bad_request("Invalid Id")
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def borrow(id):
    try:
        current_user = get_jwt_identity()
        if current_user['status'] is False:
            return response_handler.unautorized_array("status","Please activate your account to borrow book")
        elif current_user['id_role'] in auth('public') and current_user['status'] is True:
            # Check id is UUID or not
            UUID(id)
            
            # Check limit book borrowed
            limit = limit_borrow(str(current_user['id_user']))
            limit_book = int(os.getenv('LIMIT_BOOK'))
            if limit == limit_book:
                return response_handler.bad_request(f"You already borrow {limit_book} book, please return the book first")
            
            # Check Book is not borrowed
            data = []
            for i in select_all(Returns):
                data.append(i.id_borrow)
                
            for i in select_all(BorrowDetails):
                if current_user['id_user'] == str(i.borrow.id_user) and i.borrow.status == False and str(i.id_book) == id and i.id_borrow not in data:
                    return response_handler.bad_request("You already request this book, Please contact admin")
                elif current_user['id_user'] == str(i.borrow.id_user) and i.borrow.status == True and str(i.id_book) == id and i.id_borrow not in data:
                    return response_handler.bad_request("You are borrowing this book, please return before you borrow again")
                    
            # Insert to borrow table
            id_borrow = uuid4()
            new_borrow = Borrows(id_borrow = id_borrow,
                                 return_date = None,
                                 status = False,
                                 id_user = current_user['id_user'])
            new_detail = BorrowDetails(id_borrow = id_borrow,
                                       id_book = id)
            
            db.session.add(new_borrow)
            db.session.add(new_detail)
            db.session.commit()
            
            return response_handler.created("","Book successfull add to booking request, please contact Admin")
        else:
            return response_handler.unautorized()
    
    except ValueError:
        return response_handler.bad_request("Invalid Id")
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
@jwt_required()
def co_cart(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('public'):
            # Check id is UUID or not
            UUID(id)
            # Check user co same with user acc
            cart = select_cart(id)
            if cart == None:
                return response_handler.bad_request("Book is not in cart")
            elif str(cart.id_user) != current_user['id_user']:
                return response_handler.unautorized()
            
            # Check limit book borrowed
            limit = limit_borrow(str(current_user['id_user']))
            limit_book = int(os.getenv('LIMIT_BOOK'))
            if limit == limit_book:
                return response_handler.bad_request(f"You already borrow {limit_book} book, please return the book first")
            
            # Check Cart is exist or not
            cart = select_cart(id)
            if cart == None:
                return response_handler.bad_request("Book in cart not found")
            
            # Insert to borrow table
            id_borrow = uuid4()
            new_borrow = Borrows(id_borrow = id_borrow,
                                 return_date = None,
                                 status = False,
                                 id_user = current_user['id_user'])
            new_detail = BorrowDetails(id_borrow = id_borrow,
                                       id_book = cart.id_book)
            
            db.session.add(new_borrow)
            db.session.add(new_detail)
            db.session.commit()
            
            # Delete book from cart
            delete_cart(id)
            
            return response_handler.created("","Book successfull add to booking request, please contact Admin")
        else:
            return response_handler.unautorized()
    
    except ValueError:
        return response_handler.bad_request("Invalid Id")
    
    except KeyError as err:
        return response_handler.bad_request(f'{err.args[0]} field must be filled')

    except Exception as err:
        return response_handler.bad_gateway(str(err))

@jwt_required()
def carts():
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('public'):
            
            # Get param from url
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', int(os.getenv('PER_PAGE')), type=int)
            
            # Check is page exceed or not
            page_exceeded = meta_data(Carts,page,per_page)
            if page_exceeded: 
                return response_handler.not_found("Page Not Found")
            
            # Query data all
            meta = cart_all('page', page, 'per_page', per_page, current_user['id_user'])
            
            data = []
            for i in meta.items:
                data.append({
                    "cart" : CartsSchema().dump(i),
                    "book" : BooksSchema().dump(i.book)

                })
            return response_handler.ok_with_meta(data,meta)
                 
        return response_handler.unautorized() 
    except Exception as err:
        return response_handler.bad_gateway(str(err))
    
@jwt_required()
def delete_cart(id):
    try:
        current_user = get_jwt_identity()
        if current_user['id_role'] in auth('public'):
            UUID(id)
            # Check user co same with user acc
            cart = select_cart(id)
            if cart == None:
                return response_handler.bad_request("Book not found")
            elif str(cart.id_user) != current_user['id_user']:
                return response_handler.unautorized()
            
            db.session.delete(cart)
            db.session.commit()
            return response_handler.ok("","Book is deleted from cart")
        else:
            return response_handler.unautorized()
    except ValueError:
        return response_handler.bad_request("Invalid Id")
    except Exception as err:
        return response_handler.bad_gateway(str(err))