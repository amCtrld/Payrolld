from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'error': 'Missing email or password'}, 400
    
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email already exists'}, 400
    
    user = User(
        email=data['email'],
        role=data.get('role', 'employee')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return {'message': 'User created successfully', 'user': user.to_dict()}, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    print(f"DEBUG: Received login data: {data}")  # Debug line
    
    if not data or not data.get('email') or not data.get('password'):
        print("DEBUG: Missing email or password")  # Debug line
        return {'error': 'Missing email or password'}, 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        print(f"DEBUG: User not found for email: {data['email']}")  # Debug line
        return {'error': 'Invalid email or password'}, 401
    
    if not user.check_password(data['password']):
        print(f"DEBUG: Password check failed for user: {data['email']}")  # Debug line
        return {'error': 'Invalid email or password'}, 401
    
    access_token = create_access_token(identity=str(user.id))  # Convert to string
    
    print(f"DEBUG: Login successful for user: {data['email']}, token created with identity: {str(user.id)}")  # Debug line
    return {
        'access_token': access_token,
        'user': user.to_dict()
    }, 200

@auth_bp.route('/test', methods=['GET'])
@jwt_required()
def test_jwt():
    """Test JWT token"""
    try:
        current_user_id = int(get_jwt_identity())  # Convert back to int
        user = User.query.get(current_user_id)
        
        return {
            'message': 'JWT token is valid',
            'user_id': current_user_id,
            'user': user.to_dict() if user else None
        }, 200
    except Exception as e:
        return {'error': f'JWT error: {str(e)}'}, 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    current_user_id = int(get_jwt_identity())  # Convert back to int
    user = User.query.get(current_user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return user.to_dict(), 200
