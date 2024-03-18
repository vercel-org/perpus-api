from flask import Flask
from config import Db_config, Mail_config, Cloudinary_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.prefix_middleware import PrefixMiddleware
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
import os
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


# Load Config from obj
app.config.from_object(Db_config)
app.config.from_object(Mail_config)
app.config.from_object(Cloudinary_config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Setup JWT Config
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# URL prefix
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/perpus-api/v1')



# Secret key for password reset
secret_key = app.config['SECRET_KEY'] = os.getenv('EMAIL_SECRET_KEY')

# Initialize mail sending
mail_config = Mail_config
mail = Mail(app)

CORS(app)


from app.models import roles, users, cart, authors, books, bookshelves, borrows, borrow_details, categories, publishers, returns, return_details

# Create Roles
from app.models.roles import create_roles
create_roles()

# Create Super Admin User
from app.models.users import create_super_admin
create_super_admin()


from app import routes
if __name__ == "__main__":
    app.run()