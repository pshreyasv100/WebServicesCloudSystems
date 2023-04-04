#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify, redirect
import re
from urllib.parse import urlparse
import datetime




def check_url(str1):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, str1) is not None:
        return True
    else:
        return False


records = {}


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_ids():
    return records

@app.route('/<id>', methods=['GET'])
def get_url(id):

    if id is not None:
        if id not in records:
            return ("", 404)
        return (redirect(records[id]),301)
        #return (redirect(records[id]),301)
    else:
        return records

@app.route('/', methods=['PUT'])
def update_record():
    id = request.args['id']
    url = request.args['url']
    if id not in records:
        return ("", 404)
    records[id] = url
    return ""

@app.route('/', methods=['POST'])
def create_short_url():
    date = str(datetime.datetime.now())
    #print(date)
    url = request.args['url']
    id = str(hash(url+date))
    #print(check_url(url))
    if check_url(url) is False:
        return ("Please enter a valid url", 400)
    records[id] = url
    return request.base_url+str(id)

@app.route('/', methods=['DELETE'])
def delete_record():
    id = request.args['id']
    if id not in records:
        return ("", 404)
    del records[id]
    return ('', 204)




if __name__ == '__main__':
    app.run(debug=True)