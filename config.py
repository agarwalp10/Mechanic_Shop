
# adding in our config classes here

class DevelopmentConfig: 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:bball1007@localhost/mechanic_db'
    DEBUG = True #auto update 
    CACHE_TYPE = 'SimpleCache' #caching type
    CACHE_DEFAULT_TIMEOUT = 300 #cache timeout in seconds

class TestingConfig:
    pass

class ProductionConfig: 
    pass