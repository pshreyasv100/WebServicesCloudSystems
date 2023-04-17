
#!/usr/bin/env python
import json
from flask import Flask, request, jsonify, redirect, url_for
from authentication import add_new_user, get_jwt, is_valid_jwt, reset_password


# https://stackoverflow.com/questions/59549527/calling-rest-api-of-a-flask-app-from-another-flask-app


app = Flask(__name__)


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


@app.route('/users/validate_jwt/<jwt>', methods=['POST'])
def validate_jwt(jwt):

    # returns if the jwt is valid and username associated with it
    return jsonify(is_valid_jwt(jwt))



if __name__ == '__main__':
    app.run(port=5001, debug=True)