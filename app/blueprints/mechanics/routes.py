from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanics_bp

#==========ROUTES for MECHANIC=================
#POST - create a new mechanic
@mechanics_bp.route('/', methods=['POST'])
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
def get_mechanics():
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
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
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

