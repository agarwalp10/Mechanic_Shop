from app import create_app
from app.models import db, Customer #imports db instance from models to manage the database
from app.utils.util import encode_token
import unittest #imports phython's unittest framework for setting up and running tests

class TestCustomer(unittest.TestCase): #defines a test class inherting from unittest.TestCase
    def setUp(self):
        self.app = create_app('TestingConfig') #creates a test app instance using TestingConfig
        # creating a test customer
        self.customer = Customer(name="test_user", email="test@email.com", phone="123-456-7890", password="test") #creates a test customer instance
        with self.app.app_context():
            #initalizes a test databaes context
            db.drop_all() #clears existing database tables
            db.create_all() #sets up fresh tables for each test
            db.session.add(self.customer) #adds the test customer to the database session
            db.session.commit() #commits the session to save the customer in the database
        self.token = encode_token(1)
        self.client = self.app.test_client() #sets up a test client to simulate requests
    
    # Basic "Create Customer" Test
    # Propose: test that the customer creation endpoint behaves as expected with valid input
    # Implementation
        # utilizeing our test client, make a POST request to create the member endpoint
        # verify that a successful response is returned (status code 201) and correct data are returned
    # Validation
        # Assert the HTTP status and verify the presence of key data fields inther response
    
    def test_create_customer(self):
        customer_payload = { #defines a dictionary containing the data for a new csutomer (name, email, phone, password)
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "301-456-3030",
            "password": "securepassword"
        }
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
    
    def test_invalid_creation(self):
        # Test creating a customer with missing required fields
        customer_payload = {
            "name": "Jane Doe",
            "email": "email@email.com",
            "phone": "987-654-3210"
            # Missing password field
        }
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400) # Expecting a 400 Bad Request
        self.assertEqual(response.json['password'],['Missing data for required field.'])

    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw" 
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Invalid email or password')

    def test_update_customer(self):
        update_payload = {
            "name": "Updated Name",
            "phone": "123-456-7890",
            "email": "test@email.com",
            "password": "test"
        }
        headers = {"Authorization": "Bearer " + self.test_login_customer()}

        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")
        self.assertEqual(response.json['email'], "test@email.com")

    # Test retrieving all customers
    def test_get_all_customers_no_pagination(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


    def test_get_all_customers_with_pagination(self):
        response = self.client.get('/customers/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    # Test retrieving a single customer by ID
    def test_get_customer_by_id(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)
    
    # test deleting a customer
    def test_delete_customer(self):
        headers = {"Authorization": "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Customer id: 1, successfully deleted.')

        

