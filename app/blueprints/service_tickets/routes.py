from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Ticket, Mechanic, db
from . import service_tickets_bp

#==========ROUTES for SERVICE TICKET=================
#POST - create a new service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():   
    try: 
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400

    # create a new service ticket
    new_ticket = Ticket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

#PUT - adding relationship between service ticket and mechanics
@service_tickets_bp.route('/<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic_to_service_ticket(service_ticket_id, mechanic_id):
    #get the ticket
    ticket = db.session.get(Ticket, service_ticket_id)
    if not ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    #get the mechanic
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404


    # Check if the mechanic is already assigned to the ticket
    # ticket.mechancis is a list of Mechanic objects assigned to this ticket
    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned to this ticket"}), 400
    
    # Assign the mechanic to the ticket
    ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200

#PUT - removing relationship between service ticket and mechanics   
@service_tickets_bp.route('/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic_from_service_ticket(service_ticket_id, mechanic_id):    
    #get the ticket
    ticket = db.session.get(Ticket, service_ticket_id)
    if not ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    #get the mechanic
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404

    # Check if the mechanic is assigned to the ticket
    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic not assigned to this ticket"}), 400
    
    # Remove the mechanic from the ticket
    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200

#GET - get all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(Ticket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

