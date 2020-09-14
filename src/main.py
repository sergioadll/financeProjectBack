"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, WatchList, Stock
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

# EXTERNAL DATA LINK
# EXTERNAL DATA LINK
# EXTERNAL DATA LINK

@app.route('/stockdata', methods=['GET'])
def get_external_data():
   ## request_stock_list=request.get_json("https://finnhub.io/api/v1/stock/symbol?exchange=US")
    
   # return (request_stock_list), 200
    url = "https://finnhub.io/api/v1/stock/symbol?exchange=US"
    payload = {}
    headers = {
    'X-Finnhub-Token': 'bsrbhmf48v6tucpg28a0',
    'Cookie': '__cfduid=d93b1db03817fa9f12c3158268b3eba861600100583'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    resp = response.json()
    name1=""
    symbol1=""

    for i in range(len(resp)):
        for c, v in resp[i].items():
            if c == "description" and v != "":
                name1=v
                #print(name1)
            elif c == "symbol" and v != "":
                symbol1=v
                #print(symbol1)
           
        stock1=Stock(name=name1,symbol=symbol1)
        db.session.add(stock1)
    db.session.commit()
    return("oook")

@app.route('/stockdata/', methods=['DELETE'])
def delete_all_stocks():
    db.session.delete.all()
    db.session.commit()

    return jsonify("Everything deleted"), 200


# USER CRUD
# USER CRUD
# USER CRUD#
   


@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    all_people = list(map(lambda x: x.serialize(), users))

    return jsonify(all_people), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):

    user = User.query.get(user_id)
    User_ID = user.serialize()

    return jsonify(User_ID), 200

@app.route('/user', methods=['POST'])
def create_users():
    request_user=request.get_json()
    user1 = User(email=request_user["email"], password=request_user["password"], name=request_user["name"])
    db.session.add(user1)
    db.session.commit()

    return jsonify("User: "+ user1.email+", created"), 200

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


# WATCHLIST CRUD
# WATCHLIST CRUD
# WATCHLIST CRUD
@app.route('/watchlist', methods=['GET'])
def get_watchlists():

    watchLists = WatchList.query.all()
    all_watchLists = list(map(lambda x: x.serialize(), watchLists))

    return jsonify(all_watchLists), 200

@app.route('/watchlist/<int:watchlist_id>', methods=['GET'])
def get_one_watchlist(watchlist_id):

    watchlist = Watchlist.query.get(watchlist_id)
    Watchlist_ID = watchlist.serialize()

    return jsonify(Watchlist_ID), 200

@app.route('/watchlist', methods=['POST'])
def create_watchlist():
    request_watchlist=request.get_json()
    watchlist1 = WatchList(user_id=request_watchlist["user_id"],name=request_watchlist["name"])##cambiar
    db.session.add(watchlist1)
    db.session.commit()

    return jsonify("Watchlist: "+ watchlist1.name+", created"), 200

@app.route('/watchlist/<int:watchlist_id>', methods=['PUT'])
def update_watchlist(watchlist_id):
    request_watchlist=request.get_json()
    watchlist1 = WatchList.query.get(watchlist_id)
    if watchlist1 is None:
        raise APIException('Watchlist not found', status_code=404)

    if "user_id" in request_watchlist:
        watchlist1.user_id = request_watchlist["user_id"]
    if "name" in request_watchlist:
        watchlist1.name = request_watchlist["name"]

    db.session.commit()
    return jsonify("Watchlist Updated"), 200

@app.route('/watchlist/<int:watchlist_id>', methods=['DELETE'])
def delete_watchlist(watchlist_id):
    request_watchList=request.get_json()
    watchList1 = WatchList.query.get(watchlist_id)
    if watchList1 is None:
        raise APIException('Watchlist not found', status_code=404)
    db.session.delete(watchList1)
    db.session.commit()

    db.session.commit()
    return jsonify("Watchlist deleted"), 200

# STOCK CRUD
# STOCK CRUD
# STOCK CRUD

@app.route('/stock', methods=['GET'])
def get_stocks():

    stocks = Stock.query.all()
    all_stocks = list(map(lambda x: x.serialize(), stocks))

    return jsonify(all_stocks), 200

@app.route('/stock/<int:stock_id>', methods=['GET'])
def get_one_stock(stock_id):

    stocks = Stock.query.get(stock_id)
    Stock_Id = stocks.serialize()

    return jsonify(Stock_Id), 200

@app.route('/stock', methods=['POST'])
def create_stock():
    request_stock=request.get_json()
    stock1 = Stock(name=request_stock["name"],symbol=request_stock["symbol"])##cambiar
    db.session.add(stock1)
    db.session.commit()

    return jsonify("Stock: "+ stock1.name+", created. "+ "ID: " + str(stock1.id)), 200

@app.route('/stock/<stock_id>', methods=['PUT'])
def update_stock(stock_id):
    request_stock=request.get_json()
    stock1 = Stock.query.get(stock_id)
    if stock1 is None:
        raise APIException('Stock not found', status_code=404)

    if "symbol" in request_stock:
        stock1.symbol = request_stock["symbol"]
    if "name" in request_stock:
        stock1.name = request_stock["name"]

    db.session.commit()
    return jsonify("Stock Updated"), 200

@app.route('/stock/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    request_stock=request.get_json()
    stock1 = Stock.query.get(stock_id)
    if stock1 is None:
        raise APIException('Stock not found', status_code=404)
    db.session.delete(stock1)
    db.session.commit()

    db.session.commit()
    return jsonify(stock1.name + " deleted"), 200


# WATCHELEMENT CRUD
# WATCHELEMENT CRUD
# WATCHELEMENT CRUD

@app.route('/watchelement', methods=['GET'])
def get_watchelements():

    watchelements = WatchElement.query.all()
    all_watchelements = list(map(lambda x: x.serialize(), watchelements))

    return jsonify(all_watchelements), 200

@app.route('/watchelement/<int:watchelement_id>', methods=['GET'])
def get_one_watchelement(watchelement_id):

    watchelements = WatchElement.query.get(stock_id)
    Watchelement_ID = watchelements.serialize()

    return jsonify(Watchelement_ID), 200

@app.route('/watchelement', methods=['POST'])
def create_watchelement():
    request_watchelement=request.get_json()
    watchelement1 = WatchElement(watchlist_id=request_watchelement["watchlist_id"],stock_symbol=request_watchelement["stock_symbol"])
    db.session.add(watchelement1)
    db.session.commit()

    return jsonify("Watch element from Watchlist: "+ watchelement1.watchlist_id+", created. "+ "ID: " + str(watchelement1.id)), 200

@app.route('/watchelement/<watchelement_id>', methods=['PUT'])
def update_watchelement(watchelement_id):
    request_watchelement=request.get_json()
    watchelement1 = WatchElement.query.get(watchelement_id)
    if watchelement1 is None:
        raise APIException('Watch element not found', status_code=404)

    if "symbol" in request_watchelement:
        watchelement1.symbol = request_watchelement["symbol"]
    if "name" in request_watchelement:
        watchelement1.name = request_watchelement["name"]

    db.session.commit()
    return jsonify("Watch element Updated"), 200

@app.route('/watchelement/<int:watchelement_id>', methods=['DELETE'])
def delete_watchelement(watchelement_id):
    request_watchelement=request.get_json()
    watchelement1 = WatchElement.query.get(watchelement_id)
    if watchelement1 is None:
        raise APIException('Watch element not found', status_code=404)
    db.session.delete(watchelement1)
    db.session.commit()

    db.session.commit()
    return jsonify("Watch element from Watchlist: "+ watchelement1.watchlist_id+ " deleted"), 200





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


