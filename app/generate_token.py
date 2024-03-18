from flask_jwt_extended import create_access_token, create_refresh_token

def generate_token(identity):
    acces_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity )
    data = {
            "access_token": acces_token,
            "refresh_token": refresh_token,
        }
    return data