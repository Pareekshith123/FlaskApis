from flask import Flask, request, jsonify
from pony.orm import Database, Required, db_session, select, PrimaryKey

app = Flask(__name__)
db = Database()

# Set up the database connection
db.bind(provider='postgres', user='postgres', password='root', host='localhost', port='5432', database='lidkhard')

# Define the User entity
class User(db.Entity):
    user_id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Required(str, unique=True)

# Generate the database schema
db.generate_mapping(create_tables=True)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    with db_session:
        new_user = User(username=data['username'], email=data['email'])
        db.commit()
        return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    with db_session:
        users = select(user for user in User)[:]
        result = [{'id': user.user_id, 'username': user.username, 'email': user.email} for user in users]
        return jsonify({'users': result})

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    with db_session:
        user = User.get(user_id=int(user_id))
        if user:
            return jsonify({'id': user.user_id, 'username': user.username, 'email': user.email})
        else:
            return jsonify({'message': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    with db_session:
        user = User.get(user_id=int(user_id))
        if user:
            user.username = data['username']
            user.email = data['email']
            db.commit()
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    with db_session:
        user = User.get(user_id=int(user_id))
        if user:
            user.delete()
            db.commit()
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
