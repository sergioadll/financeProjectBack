from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()
#class UserType(enum.Enum):
#    admin = 1
#    trader = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "admin":self.admin
            # do not serialize the password, its a security breach
        }
class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)


    def __repr__(self):
        return '<WatchList %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }    

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    symbol = db.Column(db.String(12))


    def __repr__(self):
        return '<Stock %r>' % self.symbol

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "symbol": self.symbol,
            # do not serialize the password, its a security breach
        }
 
class ElementList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer)
    stock_symbol = db.Column(db.String(12))


    def __repr__(self):
        return '<ElementList %r>' % self.stock_symbol

    def serialize(self):
        return {
            "id": self.id,
            "watchlist_id":self.watchlist_id,
            "stock_symbol": self.stock_symbol,
            # do not serialize the password, its a security breach
        }
