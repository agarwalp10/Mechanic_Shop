# app/blueprints/customers/__init__.py
# creating the customers blueprint

from flask import Blueprint
customers_bp = Blueprint('customers', __name__)

from . import routes