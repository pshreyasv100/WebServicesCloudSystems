#!/usr/bin/env python
import json
from flask import Flask, request, jsonify, redirect
import re
from urllib.parse import urlparse
import datetime
import hashlib

from authentication import add_new_user, get_jwt, is_valid_jwt, reset_password

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


# https://www.geeksforgeeks.org/how-to-design-a-tiny-url-or-url-shortener/
# https://www.digitalocean.com/community/tutorials/how-to-make-a-url-shortener-with-flask-and-sqlite

@app.route('/', methods=['POST', 'DELETE', 'GET'])
def root_path_operations():

    jwt_token = request.headers.get('Authorization').split(' ')[1]
    _is_valid_jwt, username =  is_valid_jwt(jwt_token)

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
    
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    _is_valid_jwt, username =  is_valid_jwt(jwt_token)

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

    jwt_token = request.headers.get('Authorization').split(' ')[1]
    _is_valid_jwt, username =  is_valid_jwt(jwt_token)

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


    jwt_token = request.headers.get('Authorization').split(' ')[1]
    _is_valid_jwt, username =  is_valid_jwt(jwt_token)

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



@app.route('/users', methods=['POST'])
def register():
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

  





if __name__ == '__main__':
    app.run(debug=True)