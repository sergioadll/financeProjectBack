"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#user
@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    all_people = list(map(lambda x: x.serialize(), users))

    return jsonify(all_people), 200

@app.route('/user', methods=['POST'])
def create_users():
    request_user=request.get_json()
    user1 = User(email=request_user["email"], password=request_user["password"])
    db.session.add(user1)
    db.session.commit()

    return jsonify("User: "+ user1.email+", created"), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_users(user_id):
    request_user=request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found, bro', status_code=404)

    if "email" in request_user:
        user1.email = request_user["email"]
    if "password" in request_user:
        user1.password = request_user["password"]

    db.session.commit()
    return jsonify("User Updated"), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    request_user=request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found, bro', status_code=404)
    db.session.delete(user1)
    db.session.commit()

##WatchList

@app.route('/watchlist', methods=['GET'])
def get_users():

    users = User.query.all()
    all_people = list(map(lambda x: x.serialize(), users))

    return jsonify(all_people), 200

@app.route('/watchlist', methods=['POST'])
def create_users():
    request_user=request.get_json()
    user1 = User(email=request_user["email"], password=request_user["password"])
    db.session.add(user1)
    db.session.commit()

    return jsonify("User: "+ user1.email+", created"), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_users(user_id):
    request_user=request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found, bro', status_code=404)

    if "email" in request_user:
        user1.email = request_user["email"]
    if "password" in request_user:
        user1.password = request_user["password"]

    db.session.commit()
    return jsonify("User Updated"), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    request_user=request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found, bro', status_code=404)
    db.session.delete(user1)
    db.session.commit()

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
