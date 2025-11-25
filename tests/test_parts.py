from app import create_app
from app.models import db, Part #imports db instance from models to manage the database
from app.utils.util import encode_token
import unittest 

class TestPart(unittest.TestCase): #defines a test class inherting from unittest.TestCase
    def setUp(self):
        self.app = create_app('TestingConfig') #creates a test app instance using TestingConfig
        # creating a test part
        self.part = Part(part_name="test_part", price=19.99) #creates a test part instance
        with self.app.app_context():
            #initalizes a test databaes context
            db.drop_all() #clears existing database tables
            db.create_all() #sets up fresh tables for each test
            db.session.add(self.part) #adds the test part to the database session
            db.session.commit() #commits the session to save the part in the database
        self.token = encode_token(1)
        self.client = self.app.test_client() 

    def test_create_part(self):
        part_payload = { #defines a dictionary containing the data for a new part (part_name, price)
            "part_name": "Brake Pad",
            "price": 29.99
        }
        response = self.client.post('/parts/', json=part_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], "Brake Pad")
    
    def test_invalid_creation(self):
        # Test creating a part with missing required fields
        part_payload = {
            "part_name": "Oil Filter"
            # Missing price field
        }
        response = self.client.post('/parts/', json=part_payload)
        self.assertEqual(response.status_code, 400) # Expecting a 400 Bad Request
        self.assertEqual(response.json['price'],['Missing data for required field.'])
    
    def test_get_all_parts(self):
        response = self.client.get('/parts/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_specific_part(self):
        response = self.client.get(f'/parts/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)    
    
    def test_update_part(self):
        update_payload = {
            "part_name": "Updated Part",
            "price": 24.99
        }
        response = self.client.put(f'/parts/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], "Updated Part")     
    
    def test_delete_part(self):
        response = self.client.delete(f'/parts/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], f'Part id: 1, successfully deleted.')