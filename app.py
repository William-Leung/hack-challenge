from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, get_jwt_identity
from functools import wraps
from datetime import datetime, timedelta
from db import db, User, Location, Post, get_nearest_location, create_locations
import json
import logging
logging.basicConfig(level=logging.DEBUG)


# App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'dev_secret'  
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
CORS(app)

db_filename = "chat.db"
db.init_app(app)
jwt = JWTManager(app)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return failure_response("Invalid or missing token.", 401)
    return decorated

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

@app.route("/")
def base():
    return "hello"

@app.route('/register/', methods=['POST'])
def register():
    """
    Create a new user.
    """
    data = request.json
    username = data.get("username") 
    password = data.get("password") 

    if not username or not password:
        return failure_response("Missing username or password.", 400)
    if User.query.filter_by(username=username).first():
        return failure_response("User already exists.", 400)
    
    hashed_password = generate_password_hash(password)
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return success_response({"message": "User registered successfully."}, 201)

@app.route('/login/', methods=['POST'])
def login():
    """
    Login as an existing user.
    """
    data = request.json
    username = data.get("username") 
    password = data.get("password") 

    if not username or not password:
        return failure_response("Missing username or password.", 400)
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        return success_response({"token": token})
    
    return failure_response("Invalid credentials. Please register as a new user.", 401)

@app.route('/posts/', methods=['GET'])
def get_posts_by_location():
    """
    Get all posts at a certain location.
    """
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if not latitude or not longitude:
        return failure_response("Latitude and longitude are required.", 400)

    # Convert latitude and longitude to float for comparison
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return failure_response("Latitude and longitude must be valid numbers.", 400)

    nearest_location = get_nearest_location(latitude, longitude)
    if not nearest_location:
        return failure_response("No nearby locations found.", 404)

    posts = Post.query.filter_by(location_name=nearest_location.name).all()
    queried_posts = [post.serialize() for post in posts]
    return success_response({"posts": queried_posts})

@app.route('/posts/', methods=['POST'])
# @auth_required
def create_post():
    """
    Create a post.
    """
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    content = data.get("content")
    user_id = data.get("user_id")
 
    if not content or not latitude or not longitude or not user_id:
        return failure_response("Content, latitude, and longitude are required.", 400)

    nearest_location = get_nearest_location(latitude, longitude)
    if not nearest_location:
        return failure_response("No nearby location found.", 404)

    new_post = Post(
        user_id=user_id,  
        location_name=nearest_location.name,
        content=content
    )

    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.serialize(), 201)

@app.route('/posts/<int:post_id>/like/', methods=['POST'])
# @auth_required
def like_post(post_id):
    """
    Like a post.
    """
    post = Post.query.get(post_id)
    if post:
        post.likes += 1
        db.session.commit()
        return success_response(post.serialize(), 200)
    return failure_response("Post not found.", 404)

@app.route('/posts/<int:post_id>/', methods=['DELETE'])
# @auth_required
def delete_post(post_id):
    """
    Delete a post.
    """
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"error": "Post not found."}), 404

    db.session.delete(post)
    db.session.commit()

    return failure_response(post.serialize(), 200)

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_locations()  
    app.run(host="0.0.0.0", port=5000, debug=True)
