# app/utils/util.py
#creating the token

import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
import os
# we need request because when we sit this wrapper on one of the functions, it needs to be able to access the request
# that is triggering that route
# we will imbedde that token into that request
#going to be one of my authorization headers

#for siging the token, will be needed for decoding
#for production level, keep it in environment variable
SECRET_KEY = os.environ.get('SECRET_KEY') or "super secret secrets"

def encode_token(customer_id):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)

    }

    #create token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #scramble alogrithm, embedd all this information from payload into token
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs): #args and kwargs to allow this decorator to work with any route function and any key word arguments
        token = None #placeholder for token
        #check if token is passed in the request header
        if 'Authorization' in request.headers: #then proceed to look for that token
            token = request.headers['Authorization'].split(" ")[1] #Bearer <token>, splitting up bearer and token
        
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            
            try:
                #decode the token
                print("Raw token received:", token)
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                print("Decoded token data:", data)
                print(data)
                customer_id = data['sub']

            # checking for errors
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except Exception as e:
                print("Decode error:", e)
                return jsonify({'message': f'Decode failed: {e}'}), 401
            # except jwt.InvalidTokenError:
            #     return jsonify({'message': 'Invalid token!'}), 401

            return f(customer_id, *args, **kwargs) #passing customer_id to the route function
        
        else:
            return jsonify({'message': 'you must be logged in to access this.'}), 401
        
    return decorated