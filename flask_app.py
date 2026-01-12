from app import create_app
from app.models import db


# app = create_app('DevelopmentConfig')
app = create_app('ProductionConfig')



# Create the table
with app.app_context():
    db.drop_all()  # Drop all existing tables (for development purposes), commenting out so this doesn't always run
    db.create_all()


# only for development purposes: 
# if __name__ == "__main__":
#     app.run(debug=True)
