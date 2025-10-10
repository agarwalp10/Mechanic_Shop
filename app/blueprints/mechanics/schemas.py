from app.extensions import ma
from app.models import Mechanic 

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic

#serialize data to json
mechanic_schema = MechanicSchema()
#serialize multiple objects
mechanics_schema = MechanicSchema(many=True)
