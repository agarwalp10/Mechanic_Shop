# app/blueprints/part/routes.py

from .schemas import part_schema, parts_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Part, db
from app.blueprints.parts import parts_bp
#from app.extensions import limiter, cache
#from app.utils.util import encode_token, token_required


#==========ROUTES for part=================
#POST - create a new part
@parts_bp.route('/', methods=['POST'])
def create_part():
    try: 
        part_data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_part = Part(part_name=part_data['part_name'], price=part_data['price'])
    db.session.add(new_part)
    db.session.commit()
    return part_schema.jsonify(new_part), 200

#GET - ALL part PARTS
@parts_bp.route('/', methods=['GET'])
def get_parts():
    query = select(Part)
    result = db.session.execute(query).scalars().all()
    return parts_schema.jsonify(result), 200



#GET SPECIFIC PART
@parts_bp.route('/<int:part_id>', methods=['GET'])
def get_part(part_id):
    part = db.session.get(Part, part_id)
    if part:
        return part_schema.jsonify(part), 200
    return jsonify({"message": "Part not found"}), 404

#UPDATE SPECIFIC PART
@parts_bp.route('/<int:part_id>', methods=['PUT'])
def update_part(part_id):
    query = select(Part).where(Part.id == part_id)
    part = db.session.execute(query).scalars().first()

    if part == None:
        return jsonify({"message": "Part not found"}), 404
    
    try: 
        part_data = part_schema.load(request.json)      
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in part_data.items():
        setattr(part, field, value)
    db.session.commit()
    return part_schema.jsonify(part), 200


#DELETE SPECIFIC PART
@parts_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    query = select(Part).where(Part.id == part_id)
    part = db.session.execute(query).scalars().first()

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f'Part id: {part_id}, successfully deleted.'}), 200

