#!/usr/bin/env python
import json
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy


# https://github.com/jpadilla/pyjwt/blob/master/jwt/api_jwt.py/
# https://jwt.io/introduction/
# https://vegibit.com/json-web-tokens-in-python/
# https://www.freecodecamp.org/news/how-to-sign-and-validate-json-web-tokens/
# https://pythonbasics.org/flask-sqlalchemy/

from base64 import urlsafe_b64encode, urlsafe_b64decode
import hmac
import hashlib
import json
import time
import os



SECRET_KEY = b"secret"
# _users= {}


DB_NAME = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD').strip()

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


app = Flask(__name__)

cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@dataclass
class Users(db.Model):
    username:str
    password:str

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)



# users = users.query.all()
# for user in users:
#     _users[user.key] = user.value



#-------- Authentication utils -------#

# https://lindevs.com/code-snippets/base64url-encode-and-decode-using-python
def _base64_url_encode(data):
    return urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

# https://lindevs.com/code-snippets/base64url-encode-and-decode-using-python
def _base64_url_decode(base64Url):
    padding = '=' * (4 - (len(base64Url) % 4))
    return urlsafe_b64decode(base64Url + padding).decode('utf-8')


# https://stackoverflow.com/questions/53910845/generate-hmac-sha256-signature-python
def _generate_hmac_signature(data):

    # encoding string to bytes
    encoded_data = data.encode('utf-8')
    signature = hmac.new(SECRET_KEY, encoded_data, hashlib.sha256).hexdigest()
    return signature


def is_valid_jwt(jwt):
    
    jwt_segments = jwt.split('.')
    header =  jwt_segments[0]
    payload = jwt_segments[1]
    signature = jwt_segments[2]


    generated_signature  = _base64_url_encode(_generate_hmac_signature(header+ '.' + payload).encode('utf-8'))

    # verifying if the signature of provided jwt is valid by recomputing the signature
    if signature == generated_signature:

        decoded_payload = json.loads(_base64_url_decode(payload))
        username = decoded_payload['sub']
        expiry_of_token = decoded_payload['exp']
       
        # check if user is valid existing user
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            # check if token has not expired yet
            if expiry_of_token > int(time.time()):
                return (True, username)

    return (False, None)


def _generate_jwt(payload):

    header = json.dumps({"alg": "HS256", "typ": "JWT"}).encode('utf-8')
    payload = json.dumps(payload).encode('utf-8')

    # base64_urlsafe expects data in byte format
    _jwt = _base64_url_encode(header) + '.' + _base64_url_encode(payload)
    signature = _base64_url_encode(_generate_hmac_signature(_jwt).encode('utf-8'))
    jwt = _jwt + '.' + signature
    return jwt



def get_jwt(username, password):

    # checks if user exists and password matches
    if not _is_valid_user(username, password):
        return (403, "forbidden")

   
    # token expires after 90 seconds
    exp_seconds = 90
    payload = { 
        "iss": "authentication.com",
        "sub": username,  
        "aud": "urlshortener.com",
        "exp": int(time.time()) + exp_seconds,
        "iat": int(time.time()) 
    }

    jwt = _generate_jwt(payload)
    return (200, jwt)



def _is_valid_user(username, password):

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        if existing_user.password == password:
            return True
    return False


def add_new_user(username, password):
    
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return ("duplicate", 409)
    
    else:
        user = Users(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return("success", 201)


def reset_password(username, old_password, new_password):

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        if existing_user.password == old_password:
            existing_user.password = new_password
            db.session.commit()
            return (200, "success")
    
    return (403, "forbidden")





# ------ Authentication service -----------#


@app.route('/users', methods=['POST'])
def register():
    print('inside authentication creation')
    username = request.args['username']
    password = request.args['password']

    status,msg = add_new_user(username, password)
    if status == 201:   
        return("",201)
    
    return ("duplicate", 409)
    

@app.route('/users', methods=['PUT'])
def update_password():
    username = request.args['username']
    old_password = request.args['old_password']
    new_password = request.args['new_password']

    status,msg = reset_password(username, old_password, new_password)
    return(msg,status)


@app.route('/users/login', methods=['POST'])
def login():
    username = request.args['username']
    password = request.args['password']

    status, jwt = get_jwt(username, password)
    if status == 403:
        return ("forbidden", 403)
    
    return (jwt, 200)


@app.route('/users/validate_jwt/<jwt>', methods=['POST'])
def validate_jwt(jwt):

    # returns if the jwt is valid and username associated with it
    return jsonify(is_valid_jwt(jwt))



if __name__ == '__main__':
    app.run(debug=True)