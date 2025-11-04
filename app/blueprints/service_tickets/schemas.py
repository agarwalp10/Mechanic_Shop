from app.extensions import ma
from app.models import Ticket
from marshmallow import fields

class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested("MechanicSchema", many=True)  # if you want to include mechanics details
    customer = fields.Nested("CustomerSchema")  # if you want to include customer details
    class Meta:
        model = Ticket
        include_fk = True  # Include foreign keys in the schema
        #i hope i have the right fields 
        fields = ('id', 'VIN', 'service_date', 'service_desc', 'customer_id', 'mechanics', 'customer')


class EditTicketSchema(ma.Schema):
    #edit, remove or add multiple mechanics to a service ticket
    add_mechanic_ids = fields.List(fields.Int(), required=True) #this validates payload
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ('add_mechanic_ids', 'remove_mechanic_ids')


#serialize data to json
service_ticket_schema = TicketSchema()
#serialize multiple objects
service_tickets_schema = TicketSchema(many=True)
return_ticket_schema = TicketSchema(exclude=['customer_id'])
edit_ticket_schema = EditTicketSchema()