from flask import Blueprint, request, jsonify
from app.models import User
from app import db, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists!"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# Login a user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Get all users (admin-only)
@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])  # Access the user ID from JWT payload
    if user.role != 'admin': # type: ignore
        return jsonify({"message": "Admin access required"}), 403

    users = User.query.all()
    users_list = [{"id": u.id, "username": u.username, "role": u.role} for u in users]
    return jsonify(users_list), 200

# Get a single user by ID (admin or the user himself)
@auth_bp.route('/user/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    target_user = User.query.get_or_404(id)

    if user.role != 'admin' and user.id != target_user.id: # type: ignore
        return jsonify({"message": "Permission denied"}), 403

    return jsonify({"id": target_user.id, "username": target_user.username, "role": target_user.role}), 200

# Update a user's info (admin or the user himself)
@auth_bp.route('/user/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    target_user = User.query.get_or_404(id)

    if user.role != 'admin' and user.id != target_user.id: # type: ignore
        return jsonify({"message": "Permission denied"}), 403

    data = request.get_json()
    target_user.username = data.get('username', target_user.username)
    if data.get('password'):
        target_user.password_hash = generate_password_hash(data['password'])
    target_user.role = data.get('role', target_user.role)

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

# Delete a user (admin-only)
@auth_bp.route('/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    target_user = User.query.get_or_404(id)

    if user.role != 'admin': # type: ignore
        return jsonify({"message": "Admin access required"}), 403

    db.session.delete(target_user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@jwt.user_lookup_loader
def user_loader_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity["id"])
