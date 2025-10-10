# contructing application factor 

from flask import Flask
from .extensions import ma
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp

#this is our application factory
def create_app(config_name):
    app = Flask(__name__)
    #configure the app
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    ma.init_app(app)
    db.init_app(app)

    # register blueprints
    # customers_bp is imported from app/blueprints/customers/__init__.py
    app.register_blueprint(customers_bp, url_prefix='/customers')
    # mechanics_bp is imported from app/blueprints/mechanics/__init__.py
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    # service_tickets_bp is imported from app/blueprints/service_tickets/__init__.py
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')

    return app