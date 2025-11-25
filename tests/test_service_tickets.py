from app import create_app
from app.models import db, Ticket, Mechanic, Part #imports db instance from models to manage the database
from app.utils.util import encode_token
from datetime import date
import unittest 

class TestTicket(unittest.TestCase): #defines a test class inherting from unittest.TestCase
    def setUp(self):
        self.app = create_app('TestingConfig') #creates a test app instance using TestingConfig
        # creating a test ticket
        self.ticket = Ticket(VIN="1HGCM82633A123456", service_date=date(2023, 10, 1), service_desc="Oil Change", customer_id=1) #creates a test ticket instance
        self.mechanic = Mechanic(name="mech_user", email="mech@email.com", phone="123-456-7890", salary=50000)
        self.part = Part(part_name="Brake Pad", price=29.99)
        with self.app.app_context():
            #initalizes a test databaes context
            db.drop_all() #clears existing database tables
            db.create_all() #sets up fresh tables for each test
            db.session.add(self.ticket) #adds the test ticket to the database session
            db.session.add(self.mechanic)
            db.session.add(self.part)
            db.session.commit() #commits the session to save the ticket in the database
        self.token = encode_token(1)
        self.client = self.app.test_client() 

    def test_create_ticket(self):
        ticket_payload = { #defines a dictionary containing the data for a new ticket (VIN, service_date, service_desc, customer_id)
            "VIN": "2FTRX18W1XCA12345",
            "service_date": "2023-11-15",
            "service_desc": "Tire Rotation",
            "customer_id": 1
        }
        response = self.client.post('/service_tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.json['VIN'], "2FTRX18W1XCA12345")
    
    def test_invalid_creation(self):
        # Test creating a ticket with missing required fields
        ticket_payload = {
            "VIN": "3GNEK18R5XG123456",
            "service_date": "2023-12-01"
            # Missing service_desc and customer_id fields
        }
        response = self.client.post('/service_tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 400) # Expecting a 400 Bad Request
        self.assertEqual(response.json['service_desc'],['Missing data for required field.'])
        self.assertEqual(response.json['customer_id'],['Missing data for required field.'])
    
    def test_get_all_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_get_specific_ticket(self):
        response = self.client.get(f'/service_tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)    
    
    def test_get_my_tickets(self):
        # headers = {"x-access-token": self.token}
        headers = {"Authorization": "Bearer " + self.token}

        response = self.client.get('/service_tickets/my-ticket', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_add_mechanic_to_ticket(self):
        response = self.client.put(f'/service_tickets/1/assign-mechanic/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('successfully added mechanic to ticket', response.json['message']) 
    
    def test_remove_mechanic_from_ticket(self):
        # First, add the mechanic to ensure they are assigned
        self.client.put(f'/service_tickets/1/assign-mechanic/1')
        # Now, remove the mechanic
        response = self.client.put(f'/service_tickets/1/remove-mechanic/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_ticket(self):
        response = self.client.delete(f'/service_tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Service Ticket deleted")

    def test_update_ticket_mechanics(self):
        # First, add a mechanic to ensure the ticket has one
        self.client.put(f'/service_tickets/1/assign-mechanic/1')
        # Now, update the ticket to remove the mechanic
        update_payload = {
            "add_mechanic_ids": [],
            "remove_mechanic_ids": [1]
        }
        response = self.client.put(f'/service_tickets/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
    
    def test_add_part_to_ticket(self):
        response = self.client.put(f'/service_tickets/1/assign-part/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "successfully added part to ticket")
