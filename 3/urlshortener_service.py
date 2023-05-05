#!/usr/bin/env python
from flask import Flask, request
import re
import hashlib
import requests
from flask_cors import CORS



# https://uibakery.io/regex-library/url-regex-python
def is_valid_url(url):

    url_pattern  = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

    regex = re.compile(url_pattern, re.IGNORECASE)
    if re.match(regex, url) is not None:
        return True
    return False

# hash url using sha256
# https://datagy.io/python-sha256/
# Hashing with 256 and taking first 10 characters as id
def hash_url(url):
    hash_id = hashlib.sha256(url.encode('utf-8')).hexdigest()
    _first_5 = hash_id[0:5]
    _last_5 = hash_id[(len(hash_id)-5):len(hash_id)]
    return _first_5 + _last_5


records = {}
app = Flask(__name__)
CORS(app)


# service name of authentication , same name specified in docker-compose , nginx.con, service.yml, ingress.yml
AUTH_HOST = 'auth'

# used to access service when run using docker compose 
AUTH_PORT = '5000'
# https://www.geeksforgeeks.org/how-to-design-a-tiny-url-or-url-shortener/
# https://www.digitalocean.com/community/tutorials/how-to-make-a-url-shortener-with-flask-and-sqlite

@app.route('/', methods=['POST', 'DELETE', 'GET'])
def root_path_operations():

    jwt = request.headers.get('Authorization').split(' ')[1]
    response  = requests.post(url=f"http://{AUTH_HOST}:{AUTH_PORT}/users/validate_jwt/{jwt}")
    _is_valid_jwt, username = (response.json())
    
    # Verify if jwt token is valid
    if not _is_valid_jwt:
        return("forbidden", 403)
    

    # POST
    if request.method == 'POST':

        url = request.args['url']
        if not is_valid_url(url):
            return ("error", 400)

        id = hash_url(url)
        if username not in records.keys():
            records[username] = {id:url}
        else:   
            existing = records[username]
            existing.update({id:url})

        return (str(id), 201)

    # GET
    if request.method == 'GET':

        if username not in records.keys():
            return []
        ids = list(records[username].keys())
        return ids
    
    # DELETE
    if request.method == 'DELETE':
        return ("",404)


@app.route('/<id>', methods=['GET'])
def get_url(id):
    
    jwt = request.headers.get('Authorization').split(' ')[1]
    response  = requests.post(url=f"http://{AUTH_HOST}:{AUTH_PORT}/users/validate_jwt/{jwt}")
    _is_valid_jwt, username = (response.json())

    # Verify if jwt token is valid
    if not _is_valid_jwt:
        return("forbidden", 403)

    if username not in records.keys():
        return ("" ,404)
       
    existing = records[username]
    if id not in existing:
            return ("" ,404)
    return (existing[id], 301)

@app.route('/<id>', methods=['DELETE'])
def delete_url(id):

    jwt = request.headers.get('Authorization').split(' ')[1]
    response  = requests.post(url=f"http://{AUTH_HOST}/users/validate_jwt/{jwt}")
    _is_valid_jwt, username = (response.json())


    # Verify if jwt token is valid
    if not _is_valid_jwt:
        return("forbidden", 403)
    

    if username not in records.keys():
        return ("" ,404)
     
    existing = records[username]
    if id not in existing:
            return ("" ,404)
    else:   
        existing = records[username]
        del existing[id]

    return ("", 204)


@app.route('/', methods=['PUT'])
def update_record():
    id = request.args['id']
    url = request.get_json()['url']

    jwt = request.headers.get('Authorization').split(' ')[1]
    response  = requests.post(url=f"http://{AUTH_HOST}:{AUTH_PORT}/users/validate_jwt/{jwt}")
    _is_valid_jwt, username = (response.json())


  
    # Verify if jwt token is valid
    if not _is_valid_jwt:
        return("forbidden", 403)

    if not is_valid_url(url):
        return ("error", 400)
    
  
    if username not in records.keys():
        return ("" ,404)
     
    existing = records[username]
    if id not in existing:
            return ("" ,404)
    else:   
        existing = records[username]
        existing.update({id:url})
    return ""




if __name__ == '__main__':
    app.run(debug=True)