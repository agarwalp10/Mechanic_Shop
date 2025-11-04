# app/blueprints/parts/__init__.py

# creating the parts blueprint

from flask import Blueprint
parts_bp = Blueprint('parts', __name__)

from . import routes