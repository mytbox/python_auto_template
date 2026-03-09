"""
Mock API Server for Testing
This is a simple Flask-based mock API server for testing purposes.
It simulates common API endpoints like login, email verification, etc.
"""

from flask import Flask, request, jsonify
import logging
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for verification codes
verification_codes = {}
user_tokens = {}
users = {}


def generate_verification_code(length=6):
    """Generate a random verification code"""
    return ''.join(random.choices(string.digits, k=length))


def generate_token():
    """Generate a random token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/account/send-verify-code', methods=['POST'])
def send_verify_code():
    """
    Send verification code endpoint
    Supports both email and phone number verification
    """
    data = request.get_json()
    login_type = data.get('loginType', 'email')
    number = data.get('number')
    
    if not number:
        return jsonify({
            'code': 400,
            'msg': 'Number is required',
            'ok': False
        }), 400
    
    # Generate verification code
    code = generate_verification_code()
    key = f"{login_type.upper()}:{number}"
    verification_codes[key] = {
        'code': code,
        'timestamp': datetime.now(),
        'expires_at': datetime.now() + timedelta(minutes=5)
    }
    
    logger.info(f"Verification code sent to {login_type}: {number}, code: {code}")
    
    return jsonify({
        'code': 200,
        'msg': f'{login_type} verification code sent successfully',
        'ok': True,
        'data': {
            'code': code  # Return code for testing purposes
        }
    }), 200


@app.route('/account/reg-ai-login', methods=['POST'])
def login_with_code():
    """
    Login with verification code endpoint
    """
    data = request.get_json()
    number = data.get('number')
    auth_code = data.get('authCode')
    login_type = data.get('loginType', 'email')
    device_type = data.get('deviceType', 'unknown')
    language = data.get('language', 'en')
    
    if not number or not auth_code:
        return jsonify({
            'code': 400,
            'msg': 'Number and auth code are required',
            'ok': False
        }), 400
    
    # Verify the code
    key = f"{login_type.upper()}:{number}"
    stored_code = verification_codes.get(key)
    
    if not stored_code:
        return jsonify({
            'code': 400,
            'msg': 'Verification code not found or expired',
            'ok': False
        }), 400
    
    if stored_code['code'] != auth_code:
        return jsonify({
            'code': 400,
            'msg': 'Invalid verification code',
            'ok': False
        }), 400
    
    if datetime.now() > stored_code['expires_at']:
        return jsonify({
            'code': 400,
            'msg': 'Verification code has expired',
            'ok': False
        }), 400
    
    # Generate token and user info
    token = generate_token()
    account_id = ''.join(random.choices(string.digits, k=16))
    
    # Store user session
    user_tokens[token] = {
        'number': number,
        'login_type': login_type,
        'account_id': account_id,
        'device_type': device_type,
        'language': language,
        'created_at': datetime.now()
    }
    
    # Clear used verification code
    del verification_codes[key]
    
    logger.info(f"User logged in successfully: {number}, token: {token[:10]}...")
    
    return jsonify({
        'code': 200,
        'msg': 'Login successful',
        'ok': True,
        'data': {
            'token': token,
            'accountId': account_id,
            'number': number,
            'loginType': login_type
        }
    }), 200


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users endpoint"""
    return jsonify({
        'code': 200,
        'msg': 'Success',
        'ok': True,
        'data': list(users.values())
    }), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID endpoint"""
    user = users.get(str(user_id))
    
    if not user:
        return jsonify({
            'code': 404,
            'msg': 'User not found',
            'ok': False
        }), 404
    
    return jsonify({
        'code': 200,
        'msg': 'Success',
        'ok': True,
        'data': user
    }), 200


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create user endpoint"""
    data = request.get_json()
    
    user_id = len(users) + 1
    user = {
        'id': user_id,
        'name': data.get('name', 'Test User'),
        'email': data.get('email', 'test@example.com'),
        'phone': data.get('phone', '13800138000'),
        'created_at': datetime.now().isoformat()
    }
    
    users[str(user_id)] = user
    
    logger.info(f"User created: {user_id}")
    
    return jsonify({
        'code': 201,
        'msg': 'User created successfully',
        'ok': True,
        'data': user
    }), 201


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts endpoint (JSONPlaceholder compatible)"""
    posts = [
        {
            'userId': 1,
            'id': 1,
            'title': 'Mock Post 1',
            'body': 'This is a mock post for testing purposes'
        },
        {
            'userId': 1,
            'id': 2,
            'title': 'Mock Post 2',
            'body': 'Another mock post for testing'
        }
    ]
    
    return jsonify(posts), 200


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get post by ID endpoint (JSONPlaceholder compatible)"""
    post = {
        'userId': 1,
        'id': post_id,
        'title': f'Mock Post {post_id}',
        'body': f'This is mock post {post_id} for testing purposes'
    }
    
    return jsonify(post), 200


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create post endpoint (JSONPlaceholder compatible)"""
    data = request.get_json()
    
    post_id = random.randint(100, 999)
    post = {
        'id': post_id,
        'title': data.get('title', 'Default Title'),
        'body': data.get('body', 'Default Body'),
        'userId': data.get('userId', 1)
    }
    
    logger.info(f"Post created: {post_id}")
    
    return jsonify(post), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update post endpoint (JSONPlaceholder compatible)"""
    data = request.get_json()
    
    post = {
        'id': post_id,
        'title': data.get('title', 'Updated Title'),
        'body': data.get('body', 'Updated Body'),
        'userId': data.get('userId', 1)
    }
    
    logger.info(f"Post updated: {post_id}")
    
    return jsonify(post), 200


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete post endpoint (JSONPlaceholder compatible)"""
    logger.info(f"Post deleted: {post_id}")
    
    return jsonify({}), 200


@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Get posts by user ID endpoint (JSONPlaceholder compatible)"""
    posts = [
        {
            'userId': user_id,
            'id': 1,
            'title': f'User {user_id} Post 1',
            'body': 'Post content'
        }
    ]
    
    return jsonify(posts), 200


@app.route('/api/comments', methods=['GET'])
def get_comments():
    """Get all comments endpoint (JSONPlaceholder compatible)"""
    comments = [
        {
            'postId': 1,
            'id': 1,
            'name': 'Test Commenter',
            'email': 'test@example.com',
            'body': 'This is a test comment'
        }
    ]
    
    return jsonify(comments), 200


@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Get comments by post ID endpoint (JSONPlaceholder compatible)"""
    comments = [
        {
            'postId': post_id,
            'id': 1,
            'name': 'Test Commenter',
            'email': 'test@example.com',
            'body': f'Comment for post {post_id}'
        }
    ]
    
    return jsonify(comments), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'code': 404,
        'msg': 'Endpoint not found',
        'ok': False
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'code': 500,
        'msg': 'Internal server error',
        'ok': False
    }), 500


if __name__ == '__main__':
    logger.info("Starting Mock API Server...")
    logger.info("Mock API Server is running on http://127.0.0.1:48080")
    app.run(host='127.0.0.1', port=48080, debug=True)
