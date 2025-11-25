from app import create_app
from app.models import db, Mechanic #imports db instance from models to manage the database
from app.utils.util import encode_token
import unittest 

class TestMechanic(unittest.TestCase): #defines a test class inherting from unittest.TestCase
    def setUp(self):
        self.app = create_app('TestingConfig') #creates a test app instance using TestingConfig
        # creating a test mechanic
        self.mechanic = Mechanic(name="mech_user", email="mechanic@email.com", phone="123-456-7890", salary=50000) #creates a test mechanic instance
        with self.app.app_context():
            #initalizes a test databaes context
            db.drop_all() #clears existing database tables
            db.create_all() #sets up fresh tables for each test
            db.session.add(self.mechanic) #adds the test mechanic to the database session
            db.session.commit() #commits the session to save the mechanic in the database
        self.token = encode_token(1)
        self.client = self.app.test_client() 

    def test_create_mechanic(self):
        mechanic_payload = { #defines a dictionary containing the data for a new mechanic (name, email, phone, salary)
            "name": "Mike Wazowski",
            "email": "mw@email.com",
            "phone": "301-456-3030",
            "salary": 60000
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Mike Wazowski")

    def test_invalid_creation(self):
        # Test creating a mechanic with missing required fields
        mechanic_payload = {
            "name": "Sulley Smith",
            "email": "smith@email.com",
            "phone": "987-654-3210"
            # Missing salary field
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400) # Expecting a 400 Bad Request
        self.assertEqual(response.json['salary'],['Missing data for required field.'])
    
    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_specific_mechanic(self):
        response = self.client.get(f'/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)

    def test_update_mechanic(self):
        update_payload = {
            "name": "Updated Mechanic",
            "email": "mechanic@email.com",
            "phone": "123-456-7890",
            "salary": 55000
        }
        response = self.client.put(f'/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Mechanic")     
    
    def test_delete_mechanic(self):
        response = self.client.delete(f'/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Mechanic deleted")
    
    def test_popular_mechanics(self):
        response = self.client.get('/mechanics/popular')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_search_mechanics(self):
        response = self.client.get('/mechanics/search?name=mech')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
