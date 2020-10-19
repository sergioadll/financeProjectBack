from flask_sqlalchemy import SQLAlchemy
import requests
from flask import request


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    watchlists =  db.relationship('WatchList', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "watchlists": list(map(lambda x: x.serialize(), self.watchlists)),
            "admin":self.admin
            # do not serialize the password, its a security breach
        }

watchelements = db.Table('watchelements',
        db.Column('watchlist_id', db.Integer, db.ForeignKey('watch_list.id'), primary_key=True),
        db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'), primary_key=True)
    )

class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False )
    name = db.Column(db.String(120), unique=False, nullable=False)
    default = db.Column(db.Boolean, unique=False, default=False)

    stocks= db.relationship('Stock',secondary="watchelements", back_populates="watchlists")


    def __repr__(self):
        return '<WatchList %r>' % self.name

    def watch_list_serialize(self):
        return {
            "id": self.id, 
            "name": self.name
        }

    def serialize(self):
        return {
            "stocks" : list(map(lambda x: x.serialize(), self.stocks))
        }   
 

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    symbol = db.Column(db.String(12))

    watchlists= db.relationship('WatchList', secondary="watchelements", back_populates="stocks")

    def __repr__(self):
        return '<Stock %r>' % self.symbol

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "symbol": self.symbol,
        }

class SeedData():
    @staticmethod
    def generate_data():
        #get the data from external api
        url = "https://finnhub.io/api/v1/stock/symbol?exchange=MC"
        payload = {}
        headers = {
        'X-Finnhub-Token': 'bsrbhmf48v6tucpg28a0',
        'Cookie': '__cfduid=d93b1db03817fa9f12c3158268b3eba861600100583'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = response.json()
        name=""
        symbol=""

        for i in range(len(resp)):
            for c, v in resp[i].items():
                if c == "description" and v != "":
                    name=v
                    #print(name1)
                elif c == "symbol" and v != "":
                    symbol=v
                    #print(symbol1)
            if Stock.query.filter_by(symbol=symbol).first() is None:
                print("symbol: ", symbol, "name: ", name )
                stock=Stock(name=name,symbol=symbol)
                db.session.add(stock)
                db.session.commit()
