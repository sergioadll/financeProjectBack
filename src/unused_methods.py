@app.route('/watchlist', methods=['GET'])
def get_watchlists():

    watchLists = WatchList.query.all()
    all_watchLists = list(map(lambda x: x.serialize(), watchLists))

    return jsonify(all_watchLists), 200

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
