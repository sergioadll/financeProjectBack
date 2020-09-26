# CARGA TODOS LOS STOCKS A NUESTRA API MANUALMENTE
@app.route('/stockdata', methods=['GET'])
def get_external_data():
    #delete the previous table CHECK
    #Stock.query.delete()
    #db.session.commit()
    #get the data from external api
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

@app.route('/stockdata/', methods=['DELETE'])### chequear
def delete_all_stocks():
    Stock.query.delete()
    db.session.commit()

    return jsonify("Everything deleted"), 200
##

@app.route('/watchlist', methods=['GET'])
def get_watchlists():

    watchLists = WatchList.query.all()
    all_watchLists = list(map(lambda x: x.serialize(), watchLists))

    return jsonify(all_watchLists), 200

@app.route('/watchlist/<int:watchlist_id>', methods=['GET'])
def get_one_watchlist_default(watchlist_id):

    watchlist = WatchList.query.get(watchlist_id)
    Watchlist_ID = watchlist.serialize()

    return jsonify(Watchlist_ID), 200

@app.route('/user/<int:user_id>/watchlist', methods=['GET'])
def get_watchlists_from_user_default(user_id):

    user = User.query.get(user_id)
    watchlists_user=user.watchlists
    watchlist_info=list(map(lambda x: x.watch_list_serialize(), watchlists_user))


    return jsonify(watchlist_info), 200


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
