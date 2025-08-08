A REST API exposes endpoints (URLs) that allow clients to perform operations via HTTP methods:

GET to retrieve data

POST to create data

PUT to update data

DELETE to remove data

The API server responds with data (usually in JSON format).

Flask App Example :
Store users in a JSON file (users.json) for persistence.

Support these endpoints and methods:

GET /users — Get all users

GET /users/<user_id> — Get a user by ID

POST /users — Create a new user

PUT /users/<user_id> — Update a user by ID

DELETE /users/<user_id> — Delete a user by ID
