# app/blueprints/customers/routes.py

from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required


#==========Create Login=================
@customers_bp.route('/login', methods=['POST'])
def login():
    #first recieve payload
    # need to create a schema for this
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # use email to find customer
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        #generate token
        token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
       
       
    

#==========ROUTES for CUSTOMER=================
#POST - create a new customer
@customers_bp.route('/', methods=['POST'])
@limiter.limit("5 per day") # Limit to 5 requests per day per IP address, this is a decorator
def create_customer():
    try: 
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #check if email already exists 
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"message": "Email already associated with account"}), 400
    
    #creating a new customer
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#GET - ALL CUSTOMERS, doesn't need a limit since it's just a get request and we can continue to look at this
@customers_bp.route('/', methods=['GET'])
# cach - for frequently requested data 
# being able to cache this data will improve performance and reduce load on the database
# this is especially useful if the customer data doesn't change frequently and is frequently accessed 
# it doesn't matter if its not the most up-to-date information, as long as it's relatively recent
@cache.cached(timeout=10) # Cache this route for 60 seconds
def get_customers():
    #adding in pagination
    # /customers?page=1&per_page=10
    try: 
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customers = db.paginate(query, page = page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200

#GET SPECIFIC CUSTOMER
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"message": "Customer not found"}), 404


#UPDATE SPECIFIC MEMBER
# can only limit member 5 per month. You don't want someone to update their name too many times or it may not be a real person
@customers_bp.route('/', methods=['PUT'])
@token_required
@limiter.limit("5 per month") # Limit to 5 requests per month per IP address
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #final Stage for updating 
    #loop over customer data
    for key, value in customer_data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200

#DELETE SPECIFIC CUSTOMER
# rate limit of 5 per day, incase someone hacks into this, we don't want them to continue to delete customers
@customers_bp.route('/', methods=['DELETE'])
@token_required
@limiter.limit("5 per day") # Limit to 5 requests per day per IP address
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {customer_id}, successfully deleted.'}), 200
    

