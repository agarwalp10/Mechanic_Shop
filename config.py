
# adding in our config classes here

class DevelopmentConfig: 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:bball1007@localhost/mechanic_db'
    DEBUG = True #auto update 

class TestingConfig:
    pass

class ProductionConfig: 
    pass