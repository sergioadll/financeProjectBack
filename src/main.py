"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for, make_response 
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
#Token and login
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import jwt
import datetime
from functools import wraps
#
from utils import APIException, generate_sitemap
from admin import setup_admin
# Import models
from models import db, User, WatchList, Stock, SeedData
#
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #cambiar a true
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
    SeedData.generate_data()
    return generate_sitemap(app)

# DEFINE DECORATOR TO USE WHERE LOGIN IS REQUIRED

def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):

       token = None 
       if 'x-access-tokens' in request.headers:  
          token = request.headers['x-access-tokens'] 

       if not token:  
          return jsonify({'message': 'a valid token is missing'})   

       try:  
          data = jwt.decode(token, app.config["SECRET_KEY"]) 
          current_user = User.query.filter_by(public_id=data['public_id']).first() ##preguntar
          #print("CURRENT USER",current_user.watchlists, "                 end")
       except: 
          return jsonify({'message': 'token is invalid'})  

       return f(current_user, *args,  **kwargs)  
    return decorator 


# USER AUTHENTICATION METHODS

@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
    data = request.get_json()  
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),email=str(data["email"]),password=hashed_password,name=str(data["name"]),last_name=str(data["last_name"]), admin=False) 
    db.session.add(new_user) 
    db.session.commit()    
    watchlist1 = WatchList(user_id=new_user.id, name="Your First Watchlist",default=True)
    db.session.add(watchlist1) 
    db.session.commit()    
    
    print("user id: ",new_user.id)

    return jsonify({'message': 'registered successfully'})   


@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    auth = request.authorization  
    print("print authorization",auth)
    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = User.query.filter_by(email=auth.username).first()   
     
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1200)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token.decode('UTF-8')}) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

# USER CRUD
# USER CRUD
# USER CRUD
   

# ADMIN TRAE TODOS LOS USUARIOS
@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    all_people = list(map(lambda x: x.serialize(), users))

    return jsonify(all_people), 200

# ADMIN TRAE UN USUARIO ESPECÍFICO

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):

    user = User.query.get(user_id)
    User_ID = user.serialize()

    return jsonify(User_ID), 200

# ADMIN CREA UN NUEVO USUARIO
@app.route('/user', methods=['POST'])
def create_users():
    request_user=request.get_json()
    user1 = User(email=request_user["email"], password=request_user["password"], name=request_user["name"])
    db.session.add(user1)
    db.session.commit()

    return jsonify("User: "+ user1.email+", created"), 200

# MODIFICA UN USUARIO
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_users(user_id):
    request_user=request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)

    if "email" in request_user:
        user1.email = request_user["email"]
    if "password" in request_user:
        user1.password = request_user["password"]

    db.session.commit()
    return jsonify("User Updated"), 200

# ELIMINA UN USUARIO
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    request_user=request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()

    db.session.commit()
    return jsonify("User deleted"), 200

# TRADER ENDPOINTS

# TRAE TODOS LOS WATCHLISTS DE UN TRADER
# LOGGED IN
@app.route('/user/watchlist', methods=['GET'])
@token_required
def get_watchlists_from_user(current_user):
    user_watchlists=current_user.watchlists
    user_watchlists_list=list(map(lambda x: x.watch_list_serialize(), user_watchlists))

    return jsonify(user_watchlists_list), 200

# TRAE LA INFORMACIÓN DE TODOS LOS STOCK EN UN WATCHLIST
# LOGGED IN
@app.route('/watchlist/<int:watchlist_id>', methods=['GET'])
@token_required
def get_one_watchlist(current_user,watchlist_id):
    watchlist = WatchList.query.get(watchlist_id)
    Watchlist_ID = watchlist.serialize()

    return jsonify(Watchlist_ID["stocks"]), 200


# CREAR UN WATCHLIST
# LOGGED IN
@app.route('/watchlist', methods=['POST'])
@token_required
def create_watchlist(current_user):
    request_watchlist=request.get_json()
    stock_symbol=request_watchlist["stock"]
    
    watchlist1 = WatchList(user_id=current_user.id,name=request_watchlist["name"])
    db.session.add(watchlist1)

    stock1 = Stock.query.filter_by(symbol=stock_symbol).first()
    watchlist1.stocks.append(stock1)
    
    db.session.commit()

    return jsonify("Watchlist: "+ watchlist1.name+", created"), 200

# MODIFICAR UN WATCHLIST (CAMBIAR NOMBRE O AGREGAR STOCKS)
@app.route('/watchlist/<int:watchlist_id>', methods=['PUT'])
@token_required
def update_watchlist(current_user,watchlist_id):
    request_watchlist=request.get_json()
    watchlist1 = WatchList.query.get(watchlist_id)
    if watchlist1 is None:
        raise APIException('Watchlist not found', status_code=404)

    if "name" in request_watchlist:
        watchlist1.name = request_watchlist["name"]
    if "stock" in request_watchlist:
        stock_symbol = request_watchlist["stock"] # STOCK SYMBOL
        stock1 = Stock.query.filter_by(symbol=stock_symbol).first()
        watchlist1.stocks.append(stock1)
    db.session.commit()
    return jsonify("Watchlist Updated"), 200

# ELIMINAR UN WATCHLIST
@app.route('/watchlist/<int:watchlist_id>', methods=['DELETE'])
@token_required
def delete_watchlist(current_user,watchlist_id):
    request_watchList=request.get_json()
    watchList1 = WatchList.query.get(watchlist_id)
    if watchList1 is None:
        raise APIException('Watchlist not found', status_code=404)
    if watchList1.default==False:
        db.session.delete(watchList1)
        db.session.commit()
    db.session.commit()
    return jsonify("Watchlist deleted"), 200

# ELIMINAR UN STOCK DE UN WATCHLIST
@app.route('/watchlist/<int:watchlist_id>/<stock_symbol>', methods=['PUT'])
@token_required
def delete_stock(current_user,watchlist_id,stock_symbol):
    request_watchlist=request.get_json()
    watchlist1 = WatchList.query.get(watchlist_id)
    print(stock_symbol, type(stock_symbol))
    if watchlist1 is None:
        raise APIException('Watchlist not found', status_code=404)

    stock1 = Stock.query.filter_by(symbol=stock_symbol).first()
    watchlist1.stocks.remove(stock1)
    db.session.commit()
    return jsonify("Stock Deleted From Watchlist"), 200

# STOCK CRUD
# STOCK CRUD
# STOCK CRUD

# TRAER STOCK SEGÚN SU SYMBOL
@app.route('/stock/<stock_symbol>', methods=['GET'])
def get_stocks_symbol(stock_symbol):

    stocks = Stock.query.filter_by(symbol=stock_symbol).first()
    if stocks is None:
        raise APIException('Stock not found', status_code=404)
    stock1= stocks.serialize()
    return jsonify(stock1), 200

# TRAER STOCKS QUE EMPIECEN POR...
@app.route('/stocks/<search>', methods=['GET'])
def get_stock_search(search):

    stocks_by_symbol = Stock.query.filter(Stock.symbol.startswith(search))
    stocks_by_name = Stock.query.filter(Stock.name.startswith(search))
    if stocks_by_symbol is None and stocks_by_name is None:
        raise APIException('Stock not found', status_code=404)
    stocks1 =list(map(lambda x: x.serialize(), stocks_by_symbol))
    stocks2 =list(map(lambda x: x.serialize(), stocks_by_symbol))
    print("name",stocks1)
    print("symbol",stocks2)
    #stocks1.append(stocks2)
    return jsonify(stocks1), 200

#TRAERSE TODOS LOS STOCKS (AUTOCOMPLETE?)
@app.route('/stock', methods=['GET'])
def get_stocks():

    stocks = Stock.query.all()
    all_stocks = list(map(lambda x: x.serialize(), stocks))

    return jsonify(all_stocks), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


