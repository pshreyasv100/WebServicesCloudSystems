# https://github.com/jpadilla/pyjwt/blob/master/jwt/api_jwt.py/
# https://jwt.io/introduction/
# https://vegibit.com/json-web-tokens-in-python/
# https://www.freecodecamp.org/news/how-to-sign-and-validate-json-web-tokens/

from base64 import urlsafe_b64encode, urlsafe_b64decode
import hmac
import hashlib
import json
import time

SECRET_KEY = b"secret"


# In memory record of existing users
_users= {}


# https://lindevs.com/code-snippets/base64url-encode-and-decode-using-python
def _base64_url_encode(data):
    return urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


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
        if username in _users.keys():
            # check if token has not expired yet
            if expiry_of_token > time.time():
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
    if not _is_existing_user(username, password):
        return (403, "forbidden")

   
    # token expires after 5 seconds
    exp_seconds = 10000
    payload = {"sub": username,  "exp": int(time.time()) + exp_seconds}

    jwt = _generate_jwt(payload)
    return (200, jwt)



def _is_existing_user(username,password):
    
    if username in _users.keys() and _users[username] == password:
        return True
    return False


def add_new_user(username, password):
    
    if not _is_existing_user(username, password):
        _users[username] = password
        return (201,"")
    return (409, "duplicate")


