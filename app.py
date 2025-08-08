from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'users.json'

# Load users from file or return empty dict
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Save users dict to file
def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

users = load_users()

@app.route('/')
def home():
    return "User API is running. Use /users endpoint.", 200

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(str(user_id))
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    required_fields = ('id', 'name', 'email', 'phone', 'address', 'age')
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing or invalid user data'}), 400

    user_id = str(data['id'])
    if user_id in users:
        return jsonify({'message': 'User ID already exists'}), 400

    users[user_id] = {
        'id': int(user_id),
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'address': data['address'],
        'age': data['age']
    }
    save_users(users)
    return jsonify(users[user_id]), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_id_str = str(user_id)
    if user_id_str not in users:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided to update'}), 400

    for field in ['name', 'email', 'phone', 'address', 'age']:
        if field in data:
            users[user_id_str][field] = data[field]
    save_users(users)
    return jsonify(users[user_id_str]), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_id_str = str(user_id)
    if user_id_str in users:
        del users[user_id_str]
        save_users(users)
        return jsonify({'message': f'User {user_id} deleted'}), 200
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
