from app.extensions import ma
from app.models import Ticket

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        include_fk = True  # Include foreign keys in the schema

#serialize data to json
service_ticket_schema = TicketSchema()
#serialize multiple objects
service_tickets_schema = TicketSchema(many=True)