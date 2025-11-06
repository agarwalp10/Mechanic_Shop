from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanics_bp
from app.extensions import limiter, cache

#==========ROUTES for MECHANIC=================
#POST - create a new mechanic
# rate limit of 10 per day, there will not be more than 10 mechanics hired in one day and added to their database
@mechanics_bp.route('/', methods=['POST'])
@limiter.limit("10 per day") # Limit to 10 requests per day per IP address
def create_mechanic():   
    try: 
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400

    # check if email already exists
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({"message": "Email already associated with account"}), 400
    
    #creating a new mechanic           
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

#GET - get all mechanics
@mechanics_bp.route('/', methods=['GET'])
# adding in cache since its likely to be requested often, not change frequently, and we don't need the most up-to-date information right away
@cache.cached(timeout=60) # Cache this route for 60 seconds
def get_mechanics():
    #adding in pagination
    # /mechanics?page=1&per_page=10
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanic)
        mechanics = db.paginate(query, page=page, per_page=per_page)
        return mechanics_schema.jsonify(mechanics), 200
    except:
        #default 
    #original code without pagination
        query = select(Mechanic)
        mechanics = db.session.execute(query).scalars().all()
        return mechanics_schema.jsonify(mechanics), 200

#GET SPECIFIC MECHANIC
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"message": "Mechanic not found"}), 404 

#UPDATE SPECIFIC MECHANIC
# can only update 5 times per month, don't want someone to change their name or email too many times. Salaries may change, but not too many times
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
@limiter.limit("5 per month") # Limit to 5 requests per month per IP address
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #final Stage for updating 
    #loop over mechanic data
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

#DELETE SPECIFIC MECHANIC
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200

#GET - getting information about popular mechanics, based on number of service tickets they have worked on
# most popular mechanics first
@mechanics_bp.route('/popular', methods=['GET'])
def popular_mechanics():
    #pagination can be added here if needed
    # /popular?page=1&per_page=10
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanic)
        mechanics = db.paginate(query, page=page, per_page=per_page)

        #sort
        mechanics.items.sort(key= lambda mechanic: len(mechanic.service_tickets), reverse=True)

        return mechanics_schema.jsonify(mechanics), 200
    except: 
        #capitalize on relationships
        # we have this mechanics to service ticket relationship
        # get all mechanics, and go through and sort based on how many service tickets they have been a apart of 
        # mechanic.service_tickets is a list
        # based on length of that list 

        #this will get all of the mechanics
        query = select(Mechanic)
        mechanics = db.session.execute(query).scalars().all()

        #sort
        # key = lambda params: expression). the expression for us will be len(mechanic.service_tickets), length of that list
        #using this lambda function on every individual mechanic object in the list of mechanics
        # reverse allows us to sort in descending order
        mechanics.sort(key= lambda mechanic: len(mechanic.service_tickets), reverse=True)


        return mechanics_schema.jsonify(mechanics), 200
        # #go through list 
        # for mechanic in mechanics:
        #     print(mechanic.name, len(mechanic.service_tickets))


#GET - Query parameter to refine our searching
# search our database for mechanics
# /mechanics/search?name=John
@mechanics_bp.route('/search', methods=['GET'])
def search_mechanics():
    name = request.args.get('name')
    
    #partial match
    query = select(Mechanic).where(Mechanic.name.like(f'%{name}%'))
    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200



