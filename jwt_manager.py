import jwt

secret_key = 'mi_clave_secreta'
payload = {'email': 'admin@admin.com', 'password': 'admin'}

def create_token(payload, secret_key='mi_clave_secreta'):
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token



def validate_token(token, secret_key='mi_clave_secreta'):
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
