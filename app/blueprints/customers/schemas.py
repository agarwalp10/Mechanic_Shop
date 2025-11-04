
from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

#serialize data to json
customer_schema = CustomerSchema()
#serialize multiple objects
customers_schema = CustomerSchema(many=True)
#Schema for login
login_schema = CustomerSchema(exclude=['name', 'phone'])