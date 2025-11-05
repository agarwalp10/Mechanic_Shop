# contructing application factor 

from flask import Flask
from app.extensions import ma, limiter, cache
from app.models import db
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.parts import parts_bp
from flask_swagger_ui import get_swaggerui_blueprint

# these define the URL paths for SWAGGER UI and API's OpenAPI spec
SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml' # Our API url (can of course be a local resource)


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Mechanic Shop API"
    },
)

#this is our application factory
def create_app(config_name):
    app = Flask(__name__)
    #configure the app
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # register blueprints
    # customers_bp is imported from app/blueprints/customers/__init__.py
    app.register_blueprint(customers_bp, url_prefix='/customers')
    # mechanics_bp is imported from app/blueprints/mechanics/__init__.py
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    # service_tickets_bp is imported from app/blueprints/service_tickets/__init__.py
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    # inventory_bp is imported from app/blueprints/inventory/__init__.py
    app.register_blueprint(parts_bp, url_prefix='/parts')
    # register swagger blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) 

    return app