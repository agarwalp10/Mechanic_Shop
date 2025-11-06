from .schemas import service_ticket_schema, service_tickets_schema, edit_ticket_schema, return_ticket_schema
from app.blueprints.mechanics.schemas import mechanics_schema
from app.blueprints.parts.schemas import parts_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Ticket, Mechanic, Part, db
from . import service_tickets_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required

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

#GET - get all service tickets
@service_tickets_bp.route('/', methods=['GET'])
# adding in cache since its likely to be requested often, not change frequently, and we don't need the most up-to-date information right away
@cache.cached(timeout=60) # Cache this route for 60 seconds
def get_service_tickets():
    query = select(Ticket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

#GET SPECIFIC SERVICE TICKET
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    ticket = db.session.get(Ticket, service_ticket_id)
    if ticket:
        return service_ticket_schema.jsonify(ticket), 200
    return jsonify({"message": "Service Ticket not found"}), 404

#GET SPECIFIC SERVICE TICKET BASED ON CUSTOMER ID
@service_tickets_bp.route('/my-ticket', methods=['GET'])
@token_required
def get_my_ticket(customer_id):
    tickets = db.session.scalars(
        select(Ticket).where(Ticket.customer_id == customer_id)
    ).all()
    return service_tickets_schema.jsonify(tickets), 200

#PUT - adding relationship between service ticket and mechanics
@service_tickets_bp.route('/<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic(service_ticket_id, mechanic_id):
    #get the ticket and mechanic
    ticket = db.session.get(Ticket, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    # checking if both objects are found
    # if either is missing it goes to the final return statement
    if ticket and mechanic:
        # prevents duplicate, ensures mechanic is not already assigned, if assigned jumps to return
        if mechanic not in ticket.mechanics:
            # add the mechanic to the ticket's mechanics list
            ticket.mechanics.append(mechanic)
            db.session.commit()
            # once commited, return success message with updated ticket and mechanics list
            return jsonify({
                "message": "successfully added mechanic to ticket",
                "ticket": service_ticket_schema.dump(ticket),
                "mechanics": mechanics_schema.dump(ticket.mechanics)
            }), 200
        return jsonify({"message": "Mechanic already assigned to this ticket"}), 400
    return jsonify({"message": "Ticket or Mechanic not found"}), 404


#PUT - removing relationship between service ticket and mechanics   
@service_tickets_bp.route('/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(service_ticket_id, mechanic_id):    
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

#DELETE SPECIFIC SERVICE TICKET
# rate limit - we shouldn't need to delete a service ticket unless there was a mistake, so limit to 5 per day
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
@limiter.limit("5 per day") # Limit to 5 requests per day per IP address
def delete_service_ticket(service_ticket_id):
    ticket = db.session.get(Ticket, service_ticket_id)
    if not ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Service Ticket deleted"}), 200

#PUT - updating mechanics in serving ticket 
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    #validate data
    try:
        ticket_edit = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400


    #query that database
    query = select(Ticket).where(Ticket.id == service_ticket_id)
    #grabbing the first result

    ticket = db.session.execute(query).scalars().first()

    #creating a for loop, treating tickets_mechanics as a list
    for mechanic_id in ticket_edit['add_mechanic_ids']:
        # search the mechanics table for that mechanic id
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        # want to make sure you don't add duplicate mechanics to the service ticket
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    #removing mechanics from service ticket
    for mechanic_id in ticket_edit['remove_mechanic_ids']:
        # search the mechanics table for that mechanic id
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return return_ticket_schema.jsonify(ticket), 200


#PUT - adding relationship between service ticket and part 
@service_tickets_bp.route('/<int:service_ticket_id>/assign-part/<int:part_id>', methods=['PUT'])
def add_part(service_ticket_id, part_id):
    #get ticket and part 
    ticket = db.session.get(Ticket, service_ticket_id)
    part = db.session.get(Part, part_id)

    # check if both are there, make sure part is not already assigned to ticket
    if ticket and part: 
        if part not in ticket.parts:
            # add part to the ticket's parts list
            ticket.parts.append(part)
            db.session.commit()
            return jsonify({
                "message": "successfully added part to ticket",
                "ticket": service_ticket_schema.dump(ticket),
                "parts": parts_schema.dump(ticket.parts)
            }), 200
        return jsonify({"message": "Part already assigned to this ticket"}), 400
    return jsonify({"message": "Ticket or Part not found"}), 404

