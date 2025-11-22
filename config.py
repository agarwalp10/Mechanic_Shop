
# adding in our config classes here
import os # can reach into our development environment variables

class DevelopmentConfig: 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:bball1007@localhost/mechanic_db'
    DEBUG = True #auto update 
    CACHE_TYPE = 'SimpleCache' #caching type
    CACHE_DEFAULT_TIMEOUT = 300 #cache timeout in seconds

# test config to test our routes, we do not affect our development or production databases
class TestingConfig:
    # sqlite:///testing.db is a lightweight database suitable for testing the creation and maniupulation of data
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig: 
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = 'SimpleCache'
    