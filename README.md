# API Spec
## Authentication
All API must use this authentication except books, login, register, forget_password, reset_password
Request:
- Bearer Token
  - access_token : "your_access_token"
- Base URL
All API must use this base url
  - sponge-apparent-satyr.ngrok-free.app/perpus-api/v1
All API must use this header for skip ngrok browser warning
- Headers
  - "ngrok-skip-browser-warning" : "any_value"

## Register User
Request:
- Method : POST
- Endpoint : /register
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{
    "username" : "string",
    "name" : "string",
    "email" : "string",
    "password" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "created_at": "date",
        "email": "string",
        "id_user": "string, unique",
        "name": "string",
        "password": "string",
        "username": "string"
    },
    "message": "string",
    "status": "string"
}
```

## User Login
Request:
- Method : POST
- Endpoint : /login
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{
    "username" : "string",
    "password" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "access_token": "string",
        "id_role": "string, unique",
        "id_user": "string",
        "refresh_token": "string",
        "role": "string",
        "status": bool
    },
    "message": "string,
    "status": "string"
}
```

## User Profile
Request:
- Method : GET
- Endpoint : /profile
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": {
        "address": {
            "address": "string",
            "created_at": "date",
            "id_address": "string",
            "updated_at": "date"
        },
        "role": {
            "created_at": "date",
            "id_role": "string",
            "role": "string",
            "updated_at": "date"
        },
        "user": {
            "created_at": "date",
            "email": "string",
            "id_user": "string",
            "last_login": "date",
            "name": "string",
            "password": "string",
            "picture": "string",
            "status": bool,
            "updated_at": "date",
            "username": "string"
        }
    },
    "message": "string,
    "status": "string"
}
```

## User<id>
Request:
- Method : GET
- Endpoint : /user/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": {
        "address": {
            "address": "string",
            "created_at": "date",
            "id_address": "string",
            "updated_at": "date"
        },
        "role": {
            "created_at": "date",
            "id_role": "string",
            "role": "string",
            "updated_at": "date"
        },
        "user": {
            "created_at": "date",
            "email": "string",
            "id_user": "string",
            "last_login": "date",
            "name": "string",
            "password": "string",
            "picture": "string",
            "status": bool,
            "updated_at": "date",
            "username": "string"
        }
    },
    "message": "string,
    "status": "string"
}
```

## Update User<id>
Request:
- Method : PATCH
- Endpoint : /user/update/<id>
- Header
  - Content-Type : form-data
  - Accept : form-data
- Body
```yaml
{
    "name" : "string",
    "address" : "string",
    "email" : "string",
    "password" : "string",
    "username" : "string",
    "picture" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "address": "string",
        "created_at": "date",
        "email": "string",
        "id_user": "string",
        "last_login": "date",
        "name": "string",
        "password": "string",
        "picture": "string",
        "status": bool,
        "updated_at": "date",
        "username": "string"
    },
    "message": "string,
    "status": "string"
}
```

## User List
Request:
- Method : GET
- Endpoint : /users
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": [
        {
        "role": { 
            "id_role": "string",
            "role": "string" 
        },
        "user": { 
            "id_user": "string",
            "last_login": "date",
            "name": "string", 
            "picture": "string",
            "status": bool, 
            "username": "string"
        }
    }],
    "message": "string,
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Reset Password
Request:
- Method : POST
- Endpoint : /user/reset_password
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "email" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Change Password
Request:
- Method : PATCH
- Endpoint : /user/change_password/<token>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "password" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Activation Email
Request:
- Method : GET
- Endpoint : /user/activation_email
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string",
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Activation Account
Request:
- Method : PATCH
- Endpoint : /user/activation_account/<token>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string",
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Create Role
Request:
- Method : POST
- Endpoint : /role/create
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "role" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_role":"string",
        "role": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Read Role<id>
Request:
- Method : GET
- Endpoint : /role/read/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
 
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_role":"string",
        "role": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Update Role<id>
Request:
- Method : PATCH
- Endpoint : /role/update/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "role" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_role":"string",
        "role": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Roles
Request:
- Method : GET
- Endpoint : /roles
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
     "data": [{
        "id_role":"string",
        "role": "string",
        "created_at":"date",
        "updated_at":"date"
    }],
    "message": "string,
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Create Category
Request:
- Method : POST
- Endpoint : /category/create
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "category" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_category":"string",
        "category": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Read Category<id>
Request:
- Method : GET
- Endpoint : /category/read/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
 
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_category":"string",
        "category": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Update Category<id>
Request:
- Method : PATCH
- Endpoint : /category/update/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "category" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_category":"string",
        "category": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Categories
Request:
- Method : GET
- Endpoint : /categories
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
     "data": [{
        "id_category":"string",
        "category": "string",
        "created_at":"date",
        "updated_at":"date"
    }],
    "message": "string,
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Create Bookshelves
Request:
- Method : POST
- Endpoint : /bookshelf/create
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "bookshelf" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_bookshelf":"string",
        "bookshelf": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Read Bookshelf<id>
Request:
- Method : GET
- Endpoint : /bookshelf/read/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
 
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_bookshelf":"string",
        "bookshelf": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Update Bookshelf<id>
Request:
- Method : PATCH
- Endpoint : /bookshelf/update/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "bookshelf" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_bookshelf":"string",
        "bookshelf": "string",
        "created_at":"date",
        "updated_at":"date"
    },
    "message": "string",
    "status": "string"
}
```

## Bookshelves
Request:
- Method : GET
- Endpoint : /bookshelves
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
     "data": [{
        "id_bookshelf":"string",
        "bookshelf": "string",
        "created_at":"date",
        "updated_at":"date"
    }],
    "message": "string,
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Create Author
Request:
- Method : POST
- Endpoint : /author/create
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "name" : "string",
    "email" : "string",
    "gender" : "string",
    "phone_number" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_author":"string",
        "name": "string",
        "gender" : "string",
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    },
    "message": "string",
    "status": "string"
}
```

## Read Author<id>
Request:
- Method : GET
- Endpoint : /author/read/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
 
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_author":"string",
        "name": "string",
        "gender" : "string",
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    },
    "message": "string",
    "status": "string"
}
```

## Update Author<id>
Request:
- Method : PATCH
- Endpoint : /author/update/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{
    "name" : "string",
    "gender" : "string",
    "email" : "string",
    "phone_number" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_author":"string",
        "name": "string",
        "gender" : "string",
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    },
    "message": "string",
    "status": "string"
}
```

## Authors
Request:
- Method : GET
- Endpoint : /authors
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": [{
        "id_author":"string",
        "name": "string",
        "gender" : "string",
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    }],
    "message": "string,
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Create Publisher
Request:
- Method : POST
- Endpoint : /publisher/create
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "name" : "string",
    "email" : "string", 
    "phone_number" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_publihser":"string",
        "name": "string", 
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    },
    "message": "string",
    "status": "string"
}
```

## Read Publisher<id>
Request:
- Method : GET
- Endpoint : /publisher/read/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
 
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_publisher":"string",
        "name": "string", 
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    },
    "message": "string",
    "status": "string"
}
```

## Update Publisher<id>
Request:
- Method : PATCH
- Endpoint : /publisher/update/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{
    "name" : "string", 
    "email" : "string",
    "phone_number" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "id_publisher":"string",
        "name": "string", 
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    },
    "message": "string",
    "status": "string"
}
```

## Publishers
Request:
- Method : GET
- Endpoint : /publishers
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": [{
        "id_publisher":"string",
        "name": "string", 
        "email" : "string",
        "phone_number" : "string,
        "created_at" : "date",
        "updated_at" : "date"
    }],
    "message": "string,
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Create Books
Request:
- Method : POST
- Endpoint : /author/create
- Header
  - Content-Type : form-data
  - Accept : form-data  
- Body
```yaml
{ 
    "title" : "string",
    "description" : "string",
    "stock" : int,
    "id_author" : "string",
    "id_publisher" : "string",
    "id_category" : "string",
    "id_bookshelf" : "string",
    "picture" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": {
        "title" : "string",
        "description" : "string",
        "stock" : int,
        "id_author" : "string",
        "id_publisher" : "string",
        "id_category" : "string",
        "id_bookshelf" : "string",
        "picture" : "string"
        "created_at" : "date",
        "updated_at" : "date"
    },
    "message": "string",
    "status": "string"
}
```

## Read Book<id>
Request:
- Method : GET
- Endpoint : /book/read/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
 
- Response
```yaml
{
    "code": "string",
    "data": [{
        "author" : {
            "id_author" : "string",
            "name" : "string"
        },
        "book" : {
            "id_book" : "string",
            "picture" : "string",
            "stock" : int,
            "title" : "string"
        },
        "bookshelf" : {
            "id_bookshelf" : "string",
            "bookshelf" : "string"
        },
        "category" : {
            "id_category" : "string",
            "category" : "string"
        },
        "publisher" : {
            "id_publisher" : "string",
            "name" : "string"
        }
    }],
    "message": "string",
    "status": "string"
}
```

## Update Book<id>
Request:
- Method : PATCH
- Endpoint : /book/update/<id>
- Header
  - Content-Type : form-data
  - Accept : form-data
- Body
```yaml
{ 
    "title" : "string",
    "description" : "string",
    "stock" : int,
    "id_author" : "string",
    "id_publisher" : "string",
    "id_category" : "string",
    "id_bookshelf" : "string",
    "picture" : "string"
}
```
- Response
```yaml
{
    "code": "string",
    "data": [{
        "author" : {
            "id_author" : "string",
            "name" : "string"
        },
        "book" : {
            "id_book" : "string",
            "picture" : "string",
            "stock" : int,
            "title" : "string"
        },
        "bookshelf" : {
            "id_bookshelf" : "string",
            "bookshelf" : "string"
        },
        "category" : {
            "id_category" : "string",
            "category" : "string"
        },
        "publisher" : {
            "id_publisher" : "string",
            "name" : "string"
        }
    }],
    "message": "string",
    "status": "string"
}
```

## Books
Request:
- Method : GET
- Endpoint : /books
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": [{
        "author" : {
            "id_author" : "string",
            "name" : "string"
        },
        "book" : {
            "id_book" : "string",
            "picture" : "string",
            "stock" : int,
            "title" : "string"
        },
        "bookshelf" : {
            "id_bookshelf" : "string",
            "bookshelf" : "string"
        },
        "category" : {
            "id_category" : "string",
            "category" : "string"
        },
        "publisher" : {
            "id_publisher" : "string",
            "name" : "string"
        },
        "created_at" : "string",
        "updated_at" : "string"
    }],
    "message": "string,
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Borrow
Request:
- Method : POST
- Endpoint : /borrow/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Add to Cart
Request:
- Method : POST
- Endpoint : /cart/add/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Add to Cart
Request:
- Method : POST
- Endpoint : /cart/add/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Carts
Request:
- Method : POST
- Endpoint : /cart/add/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "string",
    "message": "string",
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Delete Item in Cart
Request:
- Method : DELETE
- Endpoint : /cart/delete/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Checkout Item in Cart
Request:
- Method : POST
- Endpoint : /cart/checkout/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## List Books in Booked Cart
Request:
- Method : GET
- Endpoint : /booked-books
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "data": [{
        "book" : {
            "id_book" : "string",
            "title" : "string",
            "stock" : int,
            "description" : "string",
            "picture" : "string",
            "id_bookshelf" : "string",
            "id_autor" : "string",
            "id_publisher" : "string",
            "id_category" : "string",
            "created_at" : date,
            "updated_at" : date
        },
        "borrow" : {
            "id_borrow" : "string",
            "status" : bool,
            "return_date" : date,
            "created_at" : date,
            "updated_at" : date
        },
        "borrow_detail" : {
            "id_borrow_detail" : "string",
            "created_at" : date,
            "updated_at" : date
        },
        "user" : {
            "id_user" : "string",
            "name" : "string"
        }
    }],
    "message": "string",
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Acc Book in Booked list
Request:
- Method : PATCH
- Endpoint : /acc/booked-books/<id>
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "string",
    "message": "string",
    "status": "string"
}
```

## Books that have not been returned
Request:
- Method : GET
- Endpoint : /returns
- Header
  - Content-Type : application/json
  - Accept : application/json
- Response
```yaml
{
    "code": "string", 
    "data": "data": [{
        "book" : {
            "id_book" : "string",
            "title" : "string",
            "stock" : int,
            "description" : "string",
            "picture" : "string",
            "id_bookshelf" : "string",
            "id_autor" : "string",
            "id_publisher" : "string",
            "id_category" : "string",
            "created_at" : date,
            "updated_at" : date
        },
        "borrow" : {
            "id_borrow" : "string",
            "status" : bool,
            "return_date" : date,
            "created_at" : date,
            "updated_at" : date
        },
        "borrow_detail" : {
            "id_borrow_detail" : "string",
            "created_at" : date,
            "updated_at" : date
        },
        "user" : {
            "id_user" : "string",
            "name" : "string"
        }
    }],
    "message": "string",
    "status": "string",
    "meta": {
        "has_next": bool,
        "has_prev": bool,
        "limit": int,
        "next_page": int,
        "page": int,
        "pages": int,
        "prev_page": int,
        "total_count": int
    },
}
```

## Books return
Request:
- Method : POST
- Endpoint : /return
- Header
  - Content-Type : application/json
  - Accept : application/json
- Body
```yaml
{ 
    "id_user" : "string",
    "id_borrow" : "string",
    "id_book" : "string", 
}
```
- Response
```yaml
{
    "code": "string",
    "data": "string"
    "message": "string",
    "status": "string"
}
```