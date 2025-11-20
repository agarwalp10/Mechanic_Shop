# Part 1: Mechanic Shop Flask API using Aplication Factory Pattern
*	Designed an ERD for a small mechanic shop that includes customers, service_tickets, and mechanic entities. There is a many to many relationship between service_tickets and mechanics, so there is also a junction table 
*	Constructed models for each of these entities based on ERD. Created the database and initialized flask app and sqlalchemy
*	Created Schemas and Routes for entities with blueprint folder. Initialized Marchmallow extension in the beginning. The routes accomplish all four CRUD operations for Create, Read, Update, and Delete customers, service_tickets, and mechanics. Each endpoint was tested as it was created
*	Ensured Application Factory Pattern was used for modularity, scalability, configuration, and testing 
*	Customer: Post (creating a customer), GET (get all or specific customer information), PUT (Update specific customer), DELETE (delete specific customer) 
*	Mechanic: POST (create mechanic), GET (Retrieves all mechanics), PUT (Updates specific mechanic), DELETE (deletes specific mechanic based on the id passed through)
*	Service_ticket: able to assign and remove mechanics 
*	POST (pass in required info for ticket), PUT (assign mechanic), PUT (remove mechanic), and GET (get all service tickets that have been assigned)

# Part 2: Mechanic Shop Flask API Advanced Development 
* added rate limiting and Cache to routes that should have them
* Implemented a token aquired at login, and used for getting, updating, and deleting service tickets for that customer
* Using a PUT endpoint, we are able to add and remove mechanics form a service ticket
* Using a Get endpoint, we are able to sort the most popular mechanics
* Able to search for mechanics using GET
* Using pagination to sort by pages
* Created a new Model: Parts which has a many-to-many relationship with service tickets (junction table was used)
* Using a PUT, we are able to add a part to the Service Ticket

# Part 3: Documentation and Testing
* Testing folder has tests for each model: customers, mechanics, parts, service_tickets
* Each test file tests all routes for each bp
