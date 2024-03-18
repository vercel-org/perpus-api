from itsdangerous import URLSafeTimedSerializer
from app import secret_key, os, mail, response_handler,app
from flask_mail import Message
from app.models import select_users_role, meta_data
from flask import render_template


# Get param for pagination
def get_read_param(request):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', int(os.getenv('PER_PAGE')), type=int)
    search = request.args.get('search')
    
    return {
        'page': page,
        'per_page': per_page,
        'search': search
    }

# Paginate, filter, and limit data
def get_paginated_data(model,page,per_page,field,filter=None):
    # Check if page exceeds
    page_exceeded = meta_data(model, page, per_page)
    if page_exceeded: 
        return None  
    
    if filter:
        attribute = getattr(model, field) if hasattr(model, field) else None
        if attribute is not None:
            data = model.query.filter(attribute.like(f'%{filter}%')).paginate(page=page, per_page=per_page)
        else:
            data = model.query.paginate(page=page, per_page=per_page)
    else:
        data = model.query.paginate(page=page, per_page=per_page)
    
    return data

# Gender in user controller
def gender():
    return ['female','male','prefer not say']

# Check update 
def check_update(json_body, data, array):
    return all(json_body[field] == getattr(data, field) for field in array)

# Authentication
def auth(param):
    if param == 'public':
        return str({select_users_role('SUPER_ADMIN_ROLE'), 
                            select_users_role('USER_ROLE'),
                            select_users_role('ADMIN_ROLE')})
    elif param == 'user':
        return str({select_users_role('USER_ROLE')})
    elif param == 'admin':
        return str({select_users_role('SUPER_ADMIN_ROLE'), 
                            select_users_role('ADMIN_ROLE')})
    elif param == 'super':
        return str({select_users_role('SUPER_ADMIN_ROLE')})

# Generate token for email
def generate_token(email):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email)

# Send email
def send_email(email,subjectBody,htmlBody):
    send = Message(
                 subject = subjectBody,
                 sender = os.getenv('MAIL_USERNAME'),
                 recipients = [email], 
                 html=htmlBody
            )
    return mail.send(send)

# render template for reset password email
def reset_password_template(url,user):
    return render_template('reset_password.html',url=url,user=user)

# render template for activation account 
def activation_account_template(url, user):
    return render_template('activation_account.html',url=url,user=user)