
# app/blueprints/parts/schemas.py

from app.extensions import ma
from app.models import Part

class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Part

#serialize data to json
part_schema = PartSchema()
#serialize multiple objects
parts_schema = PartSchema(many=True)
