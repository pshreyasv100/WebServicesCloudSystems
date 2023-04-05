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
    return hashlib.sha256(url.encode('utf-8')).hexdigest()[0:10]


records = {}


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_ids():
    ids = list(records.keys())
    return ids

@app.route('/<id>', methods=['GET'])
def get_url(id):
    
    if id not in records:
            return ("No corresponding url found" ,404)
    return (records[id], 301)

# https://www.geeksforgeeks.org/how-to-design-a-tiny-url-or-url-shortener/
# https://www.digitalocean.com/community/tutorials/how-to-make-a-url-shortener-with-flask-and-sqlite

@app.route('/', methods=['POST'])
def add_new_short_url():

    url = request.args['url']
    if not is_valid_url(url):
        return ("Invalid url", 400)

    id = hash_url(url)

    records[id] = url
    host_url = request.base_url
    return (str(id), 201)


@app.route('/<id>', methods=['DELETE'])
def delete_url(id):
    if id not in records:
        return ("Invalid ID provided", 404)
    del records[id]
    return ("Url record Deleted Successfully", 204)


@app.route('/', methods=['PUT'])
def update_record():
    id = request.args['id']
    url = request.args['url']

    if not is_valid_url(url):
        return ("Invalid url", 400)
    
    if id not in records:
        return ("ID does not exist", 404)
    records[id] = url
    return ""



if __name__ == '__main__':
    app.run(debug=True)