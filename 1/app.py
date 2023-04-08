#!/usr/bin/env python
import json
from flask import Flask, request, jsonify, redirect
import re
from urllib.parse import urlparse
import datetime
import hashlib



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

# @app.route('/', methods=['GET'])
# def get_all_ids():
#     ids = list(records.keys())
#     return ids


# https://www.geeksforgeeks.org/how-to-design-a-tiny-url-or-url-shortener/
# https://www.digitalocean.com/community/tutorials/how-to-make-a-url-shortener-with-flask-and-sqlite

@app.route('/', methods=['POST', 'DELETE', 'GET'])
def root_path_operations():

    if request.method == 'POST':

        url = request.args['url']
        if not is_valid_url(url):
            return ("error", 400)

        id = hash_url(url)
        records[id] = url
        return (str(id), 201)

    if request.method == 'GET':
        ids = list(records.keys())
        return ids
    
    if request.method == 'DELETE':
        return ("",404)


@app.route('/<id>', methods=['GET'])
def get_url(id):
    
    if id not in records:
            return ("" ,404)
    return (records[id], 301)

@app.route('/<id>', methods=['DELETE'])
def delete_url(id):
    if id not in records:
        return ("", 404)
    del records[id]
    return ("", 204)


@app.route('/', methods=['PUT'])
def update_record():
    id = request.args['id']
    url = request.args['url']

    if not is_valid_url(url):
        return ("error", 400)
    
    if id not in records:
        return ("", 404)
    records[id] = url
    return ""



if __name__ == '__main__':
    app.run(debug=True)