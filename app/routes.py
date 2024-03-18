from app import app
from app.controllers import user, user_transaction, admin_transaction, authentication, authors, bookshelves, categories, publishers, roles, books
@app.route('/')
def home():
    return 'This is Home Page for Perpustakaan App'

app.route('/login', methods = ['POST'])(authentication.login)

# Users
app.route('/register', methods = ['POST'])(user.register)
app.route('/profile', methods = ['GET'])(user.profile)
app.route('/user/<id>', methods = ['GET'])(user.user)
app.route('/user/update/<id>', methods = ['PATCH'])(user.update_user)
app.route('/users', methods = ['GET'])(user.list_user)
app.route('/user/reset_password', methods = ['POST'])(user.reset_password)
app.route('/user/change_password/<token>', methods = ['PATCH'])(user.change_password)
app.route('/user/activation_email', methods = ['GET'])(user.activation_email)
app.route('/user/activation_account/<token>', methods = ['PATCH'])(user.activation_account)


#dropdown
app.route('/dropdown/books', methods = ['GET'])(books.dropdown_books)


# Roles
app.route('/role/create', methods = ['POST'])(roles.create_role)
app.route('/role/<id>', methods = ['GET'])(roles.role)
app.route('/role/update/<id>', methods = ['PATCH'])(roles.update_role)
app.route('/roles', methods = ['GET'])(roles.roles)

# Authors
app.route('/author/create', methods = ['POST'])(authors.create_author)
app.route('/author/<id>', methods = ['GET'])(authors.author)
app.route('/author/update/<id>', methods = ['PATCH'])(authors.update_author)
app.route('/authors', methods = ['GET'])(authors.authors)

# Publishers
app.route('/publisher/create', methods = ['POST'])(publishers.create_publisher)
app.route('/publisher/<id>', methods = ['GET'])(publishers.publisher)
app.route('/publisher/update/<id>', methods = ['PATCH'])(publishers.update_publisher)
app.route('/publishers', methods = ['GET'])(publishers.publishers)

# Bookshelves
app.route('/bookshelf/create', methods = ['POST'])(bookshelves.create_bookshelf)
app.route('/bookshelf/<id>', methods = ['GET'])(bookshelves.bookshelf)
app.route('/bookshelf/update/<id>', methods = ['PATCH'])(bookshelves.update_bookshelf)
app.route('/bookshelves', methods = ['GET'])(bookshelves.bookshelves)

# Categories
app.route('/category/create', methods = ['POST'])(categories.create_category)
app.route('/category/<id>', methods = ['GET'])(categories.category)
app.route('/category/update/<id>', methods = ['PATCH'])(categories.update_category)
app.route('/categories', methods = ['GET'])(categories.categories)

# Books
app.route('/book/create', methods = ['POST'])(books.create_book)
app.route('/book/<id>', methods = ['GET'])(books.book)
app.route('/book/update/<id>', methods = ['PATCH'])(books.update_book)
app.route('/books', methods = ['GET'])(books.books)
app.route('/private_books', methods = ['GET'])(books.private_books)


# Borrow
app.route('/borrow/<id>', methods = ['POST'])(user_transaction.borrow)

# Carts
app.route('/cart/add/<id>', methods = ['POST'])(user_transaction.create_cart)
app.route('/carts', methods = ['GET'])(user_transaction.carts)
app.route('/cart/checkout/<id>', methods = ['POST'])(user_transaction.co_cart)
app.route('/cart/delete/<id>', methods = ['DELETE'])(user_transaction.delete_cart)

# Admin transaction
app.route('/booked-books', methods=['GET'])(admin_transaction.booked_books)
app.route('/acc/booked-books/<id>', methods=['PATCH'])(admin_transaction.acc_book)
app.route('/returns', methods=['GET'])(admin_transaction.return_books)
app.route('/return', methods=['POST'])(admin_transaction.create_return)


 

