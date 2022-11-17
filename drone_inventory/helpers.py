from functools import wraps
import secrets
from flask import request, jsonify, json
from drone_inventory.models import User
import decimal

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs): # doing this to check our tokens as a key-value pair
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            # headers = dictionary, x-access-token is the key, and Bearer <token> is the value
            # Bearer <token> is split into a list, where Bearer is the index[0] and <token> is index[1]
            print(token)
        if not token:
            return jsonify({'message': 'Token is Missing!'}), 401 # 401 = 401 error so it won't connect

        try:
            current_user_token = User.query.filter_by(token=token).first()
            # filter_by is similar to LIKE in SQL - only one equal sign because this is a kwarg (note syntax: key=value). we are not looking for equality
            # vs filter which is similar to value equality in Python which uses ==
            print(current_user_token)
            if not current_user_token or current_user_token.token != token:
            # current_user_token is referencing the queried User token in line 19
            # current_user_token.token is referencing the user.token
                return jsonify({'message': 'Token is invalid!'})

        except:
            owner = User.query.filter_by(token=token).first()
            # owner and current_user_token are referencing the same User token, just different variables
            if token != owner.token and secrets.compare_digest(token, owner.token):
            # secrets.compare_digest just checks if the type of a = the type of b so if token type = owner.token type
               return jsonify({'message': 'Token is invalid!'}) 
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated # Remember, need to return the decorator function

# json encoder = takes the typing and makes it a string --> need to do this for our numeric data types which has decimals
# this serializes our types to a string

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances (numerics) into strings so JSON can read it
            return str(obj)
        return super(JSONEncoder, self).default(obj)